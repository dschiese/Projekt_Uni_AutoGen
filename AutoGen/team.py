from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage, ToolCallRequestEvent, ToolCallExecutionEvent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import os
from multi_agent_system_helper.autogen_tools import test_changes_tool, read_dir_structure, read_file_tool, write_file_tool
from multi_agent_system_helper.helper_functions import fix_clone_command, set_working_directory, fetch_problem_statement, create_team_prompt, clone_repository
import subprocess

litellm_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key="REPLACE", base_url="REPLACE")
chatgpt_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key="REPLACE")
max_msg_termination = MaxMessageTermination(max_messages=11) # User Message (1) + Assistants (5) = 6 messages in total for one run // 2 runs == 11 (6+5) as user is not counted 2nd time
BASE_PATH = "PATH_TO_RESULTS"

planning_agent = AssistantAgent(
    name="planning_agent",
    model_client=chatgpt_client,
    system_message="You're part of a team of agents working on a GitHub repository that contains bugs. You, in particular, are responsible for coordinating the other agents to fix the bugs described in the task. To do so, you will read the problem statement and the repository structure, and then assign tasks to the coding agent. Use the tools provided to accomplish the task.",
    reflect_on_tool_use=True,
    tools=[read_file_tool]#, read_dir_structure]
)

read_file_agent = AssistantAgent(
    name="read_file_agent",
    model_client=chatgpt_client,
    system_message="You're a file reading agent. You will read the issued files and return their content. Use the tools provided to accomplish the task.",
    tools=[read_file_tool],
    reflect_on_tool_use=False
)

coding_agent = AssistantAgent(
    name="coding_agent",
    model_client=chatgpt_client,
    #reflect_on_tool_use=True,
    tools=[read_file_tool],
    system_message="You're a coding agent. You will fix the code and return the complete source code with the fix included. Use the tools provided to accomplish the task."
)

implementation_agent = AssistantAgent(
    name="implementation_agent",
    model_client=chatgpt_client,
    system_message="You're an implementation agent. You will apply the changes made by the coding agent to the codebase by writing the code to the file. Use the tools provided to accomplish the task.",
    tools=[write_file_tool],
    reflect_on_tool_use=False
)

verify_agent = AssistantAgent(
    name="verify_agent",
    model_client=chatgpt_client,
    system_message="You're a verification agent. You will verify the test results and the changes made by the prior agents and rate them whether they are acceptable (then you write 'APPROVE') or not. They're not acceptable when at least one test failed or the error code was '0'. When not, summarize your findings and propose them.",
    tools=[read_file_tool],
    reflect_on_tool_use=True
)

test_agent = AssistantAgent(
    name="test_agent",
    model_client=chatgpt_client,
    system_message="You're a testing agent. You will test the changes written to the codebase by the others. To do so, you must use the provided tools. Afterwards, propose the results. If the tests return an exit code only, the test failed.",
    tools=[test_changes_tool],
    reflect_on_tool_use=True
)

team = RoundRobinGroupChat([planning_agent, coding_agent, implementation_agent, test_agent, verify_agent], termination_condition=TextMentionTermination("APPROVE") | max_msg_termination)

async def main():
    for i in range(1, 31): # i is the problem statement index == dir name   
        repository_data = fetch_problem_statement(i) # Fetches the repository data from swe-bench-lite-api
        git_clone_with_index = fix_clone_command(repository_data['git_clone'], i)
        clone_repository(git_clone_with_index)
        prompt = create_team_prompt(repository_data, f"{i}")
        await team.reset()
        #await Console(team.run_stream(task=prompt))
        #subprocess.run(f"rm -r {i}", shell=True, check=True)  # Clean up the repository after the run
        #os.chdir("..") # Back to the parent dir from repositories dir
        result_dir = os.path.join(BASE_PATH, str(i))
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        results_file_path = os.path.join(result_dir, "team_log.txt")
        async for message in team.run_stream(task=prompt):
            if isinstance(message, TaskResult):
                with open(results_file_path, "w") as f:
                    f.write("Stop Reason: " + str(message.stop_reason))
                print("Stop Reason:", message.stop_reason)
                subprocess.run(f"rm -r {i}", shell=True, check=True)  # Clean up the repository after the run
                os.chdir("..") # Back to the parent dir from repositories dir
            else:
                with open(results_file_path, "w") as f:
                    print("\n" + "="*40)
                    f.write("\n" + "="*40 + "\n")
                    if isinstance(message, TextMessage):
                        msg = "Source: " + str(message.source) + "\n" + "Content: " + str(message.content)
                        print(msg)
                        f.write(msg + "\n")
                    if isinstance(message, ToolCallRequestEvent):
                        msg = "Tool Call Request" + "\n" + "Source: " + str(message.source) + "\n" + "Content: " + str(message.content)
                        print(msg)
                        f.write(msg + "\n")
                    if isinstance(message, ToolCallExecutionEvent):
                        msg = "Tool Execution Event" + "\n" + "Source: " + str(message.source) + "\n" + "Content: " + str(message.content)
                        print(msg)
                        f.write(msg + "\n")
                    print("="*40 + "\n")
                    f.write("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(main())


# IDEA: Read Log Files to use for fixing the bug
