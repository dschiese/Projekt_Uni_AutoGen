# Uni Leipzig ASE AutoGen

Projekt der Universität Leipzig im Modul **Automated Software Engineering**. 

# Usage

## Set up swe-bench-lite-*

### Set up swe-bench-lite-api

```
sudo docker run -d \
-p 8081:8080 \
--name swe-bench-lite-api \
paulroewer/swe-bench-lite-api
```

### Set up swe-bench-lite-tester

```
sudo docker run -d \
-p 8082:8080 \
--name swe-bench-lite-tester \
-v REPLACE_WITH_PWD_TO_REPOSITORIES:/repos \
-v /var/run/docker.sock:/var/run/docker.sock \
paulroewer/swe-bench-lite-tester
```

Here, replace the volume mapping of "/repos" to the `repositories` directory in this repository.

## Replace BASE_PATH  `team.py` and `autogen_tools.py`

In the `team.py` and `multi_agent_system_helper/autogen_tools.py` replace the BASE_PATH with the absolute path to the results folder in this repository.

For example: `BASE_PATH = "/home/user/AutoGen/results"`

## Set LLM 

### LiteLLM

Replace the base_url property for the litellm_client as well as the key.

### OpenAI

Replace the OpenAI API key.

## Run

Run the team script from the AutoGen directory with `python -m AutoGen.team`

# Known problems

## No permissions

Run the script as sudo since the repositories are deleted at the end of each iteration and files are written to the results directory.




