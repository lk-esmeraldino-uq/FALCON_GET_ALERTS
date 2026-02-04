"""
This module provides utility functions for saving and loading data to and from files.
"""

import os
import json
import time
import re


def save_json(data, filename, buffer_size=4096):
    """
    Saves the given data to a JSON file.

    Args:
        data (any): The data to be saved, which must be serializable to JSON.
        filename (str): The path to the file where the data will be saved.

    """
    try:
        with open(filename, mode="w", encoding="utf-8", buffering=buffer_size) as f:
            json.dump(data, f, indent=4)

        return "[*] File saved successfully"
    except Exception as e:
        return "[!] Error saving file: " + str(e)


def save_csv(data, filename):
    """
    Saves the given data to a CSV file.

    Args:
        data (any): The data to be saved, which must be a string.
        filename (str): The path to the file where the data will be saved.
    """
    try:
        with open(filename, mode="w", encoding="utf-8") as f:
            f.write(data)
        return "[*] File saved successfully"
    except Exception as e:
        return "[!] Error saving file: " + str(e)


def expanded_numbers(data: list) -> list:
    """
    Expands a list of numbers to include all possible minor versions.
    """
    expanded = []
    for item in data:
        if ".x" in item:
            major = item.replace(".x", "")
            for minor in range(10):
                expanded.append(major + "." + str(minor))
        else:
            expanded.append(item)

    return expanded


def split_text_num(data: str) -> list:
    """Split a string into two parts: the first part is a string and the second part is a number."""

    pattern = r"(.+?)\s+([0-9]+(?:\.[0-9]+)*)\s*$"
    match = re.match(pattern, data)

    if match:
        return [match.group(1), str(match.group(2))]
    return [data]


def load_json(filename) -> dict:
    """
    Loads JSON data from a file and returns it as a Python object.

    Args:
        filename (str): The path to the file that contains the JSON data to be loaded.

    Returns:
        any: The loaded data, which is a Python object decoded from the JSON data.
    """
    try:
        if os.path.exists(filename) == 0:
            save_json({}, filename)
        with open(filename, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        return {e.msg: e.pos}


def list_path(path_) -> list:
    folders = []
    for folder in os.listdir(path_):
        if os.path.isdir(f"{path_}/{folder}"):
            folders.append(folder)
    return folders


def load_csv(filename):
    """
    Loads a CSV file and returns its contents as a string.

    Args:
        filename (str): The path to the file that contains the CSV data to be loaded.

    Returns:
        str: The loaded data, which is a string containing the contents of the file.
    """
    with open(filename, mode="r", encoding="utf-8") as f:
        return f.read()


def create_folders(folder_list):
    """
    Creates a list of folders.

    Args:
        folder_list (list): A list of paths to folders that will be created if they do not exist.
    """
    if isinstance(folder_list, list):
        for folder in folder_list:
            if not os.path.exists(folder):
                os.makedirs(folder)
    if isinstance(folder_list, str):
        if not os.path.exists(folder_list):
            os.makedirs(folder_list)


def check_lifetime(file_path, max_timeout=60 * 25):  # 25 minutes
    """
    Checks the age of a file and returns True if it is older than the maximum timeout.

    Args:
        file_path (str): The path to the file to check.
        max_timeout (int): The maximum timeout in seconds. Default is 25 minutes.

    Returns:
        bool: True if the file is older than the maximum timeout, False otherwise.
    """

    if os.path.exists(file_path):
        timeout = os.path.getmtime(file_path) < time.time() - max_timeout
        if timeout:
            print(f"[!] {file_path} timeout expired")
            return False
        else:
            print(
                f"[*] {file_path} is valid for {show_lifetime(file_path,timeout=max_timeout)[0]} hours and {show_lifetime(file_path,timeout=max_timeout)[1]} minutes"
            )
            return True
    else:
        print(f"[!] {file_path} file not found")
        return False


def show_lifetime(file_path, timeout=60 * 60 * 24) -> list:
    """
    Returns the age of a file in hours.
    """
    if os.path.exists(file_path):

        t = time.time()
        file = os.path.getmtime(file_path)

        raw = timeout - (t - file)

        if raw > 0:
            raw = int(raw)
            hours = raw // 3600
            minutes = (raw % 3600) // 60
            return [hours, minutes]
        else:
            return [-1, -1]
    else:
        return [0, 0]


def split_group(_list: dict, size=5):
    """
    Splits the hosts ID into batches of size.
    """
    for i in range(0, len(_list), size):
        yield _list[i : i + size]


def get_column_len(json_content, column_name):
    return len(json_content[column_name])
