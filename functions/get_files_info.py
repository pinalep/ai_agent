import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        data_list = []
        iterate_over = os.listdir(target_dir)
        for item in iterate_over:
            file_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            data_str = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            data_list.append(data_str)
        
        joined_list = "\n".join(data_list)        # list --> str
        return joined_list
    except Exception as e:
            return f'Error: {e}'

