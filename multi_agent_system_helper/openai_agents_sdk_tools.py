from agents import function_tool
import requests
import os
from .helper_functions import resolve_file_path
import subprocess

ollama = "http://localhost:11434/api/generate"

@function_tool
def read_dir_structure():
    """
    Reads the directory structure of the current working directory and returns only .py files and their directories as a string.
    Returns:
        str: The filtered directory structure.
    """
    try:
        result = subprocess.run(
            "tree -P \"*.py\" -fi .",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"An error occurred while reading the directory structure: {e}")

@function_tool
def write_file_tool(path:str, content:str):
    """
    Writes the passed content to a file at the specified path.
    This will overwrite the entire content of the file.
    """
    try:
        print(f"Writing to file: {path}")
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

@function_tool
def get_repository_structure():
    """
    Fetches the structure of the repository from the given directory
    Args:
        repository (str): The directory name of the repository.
    Returns:
        str: The structure of the repository.
    """
    return subprocess.run(
        f"tree -P \"*.py\" -fi .",
        shell=True,
        check=True,
        capture_output=True,
        text=True
    ).stdout.strip()

@function_tool
def find_correct_path_for_passed_file(file:str):
    """
    Finds the correct path for a given file in the current working directory by prompting it to the local ollama instance.
    Args:
        file (str): The name of the file to find.
    Returns:
        str: The resolved path of the file.
    """
    try:
        payload = {
            "model": "phi3",
            "prompt": f"Find the correct path for the file '{file}' in the following directory structure:\n{get_repository_structure()}. Only return the path",
            "stream": False
        }
        response = requests.post(ollama, json=payload)
        return response.text.strip()
    except requests.RequestException as e:
        raise Exception(f"An error occurred while finding the file path: {e}")

@function_tool
def read_file_tool(path:str):
    """
    Reads a file from the given path and returns its content.
    """
    try:
        resolved_path = resolve_file_path(path)
        with open(resolved_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise Exception(f"File not found: {path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
@function_tool
def test_changes_tool():
    """
    Placeholder for a tool that tests changes made to the codebase.
    This function should be implemented with actual testing logic.
    """
    raise NotImplementedError("This tool is not yet implemented.")

def set_working_directory(directory_path:str):
    """
    Changes the current working directory to the specified path.
    Args:
        directory_path (str): The directory path to change to.
    Returns:
        str: The new working directory path.
    """
    try:
        os.chdir(directory_path)
        return f"Working directory changed to: {os.getcwd()}"
    except FileNotFoundError:
        raise Exception(f"Directory not found: {directory_path}")
    except Exception as e:
        raise Exception(f"An error occurred while changing the working directory: {e}")