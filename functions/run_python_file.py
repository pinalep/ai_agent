import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "It runs a .py file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command-line arguments to pass to the python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    
    
        
        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args:
            command.extend(args)
        final_result = []
        completedproccess_object = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)
        if completedproccess_object.returncode != 0:
            final_result.append(f'Process exited with code {completedproccess_object.returncode}')
        if not completedproccess_object.stdout and not completedproccess_object.stderr:
            final_result.append(f'No output produced')
        if len(completedproccess_object.stdout) > 0:
            final_result.append(f"STDOUT: {completedproccess_object.stdout}")
        if len(completedproccess_object.stderr) > 0:
            final_result.append(f"STDERR: {completedproccess_object.stderr}")

        return "\n".join(final_result)
    except Exception as e:
        return f'Error: executing Python file: {e}'



