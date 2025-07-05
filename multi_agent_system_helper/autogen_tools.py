# Defining the tools used in the AutoGen project

import os
import json
from .helper_functions import send_test, resolve_file_path
BASE_PATH = "/home/dennisschiese/Projekte/Master/2. Semester/Automated Software Engineering/Projekt/results"

def read_file_tool(path:str):
    """
    Reads a file from the given path and returns its content.
    Call this tool with the file name only, not the full path.
    """
    try:
        resolved_path = resolve_file_path(path)
        with open(resolved_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise Exception(f"File not found: {path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")

def read_dir_structure(directory_path:str="."):
    """
    Reads the directory structure relative from the given directory path.
    Returns:
        dict: A dictionary representing the directory structure.
    """
    dir_structure = {}
    try:
        for root, dirs, files in os.walk(directory_path):
            relative_path = os.path.relpath(root, directory_path)
            dir_structure[relative_path] = {
                "directories": dirs,
                "files": files
            }
        return dir_structure
    except Exception as e:
        raise Exception(f"An error occurred while reading the directory structure: {e}")

def write_file_tool(path:str, content:str):
    """
    Writes the passed content to a file at the specified path.
    This will overwrite the entire content of the file.
    """
    try:
        resolved_path = resolve_file_path(path)
        # Create directory if it doesn't exist
        directory = os.path.dirname(resolved_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(resolved_path, "w") as file:
            file.write(content)
        return f"Successfully wrote to {resolved_path}"
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")

def test_changes_tool(instance_id:str, FAIL_TO_PASS:list[str], PASS_TO_PASS:list[str], repoDir:int):
    """
    This tool tests the changes made in the repository using an external testing service.
    This service return either a JSON object with the succeeded and failed tests, or an exit code only.
    Always call this tool with all FAIL_TO_PASS and PASS_TO_PASS tests, never with a subset of them.
    """
    request_data = {
        "instance_id": instance_id,
        "repoDir": "/repos/" + str(repoDir),
        "FAIL_TO_PASS": FAIL_TO_PASS,
        "PASS_TO_PASS": PASS_TO_PASS,
    }
    results = send_test(request_data)
    # Write the results to a file in the BASE_PATH directory
    # Create a new dir with the repoDir name in the BASE_PATH directory and write the results to a file named "test_results.json" without changing the
    # working directory
    
    # Create the directory path for this repository
    repo_results_dir = os.path.join(BASE_PATH, str(repoDir))
    
    # Create the directory if it doesn't exist
    if not os.path.exists(repo_results_dir):
        os.makedirs(repo_results_dir)
    
    # Write the results to test_results.json
    results_file_path = os.path.join(repo_results_dir, "test_results.json")
    with open(results_file_path, "w") as f:
        json.dump(results, f, indent=2)
    
    return results