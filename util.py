from json import JSONDecoder, dump
from os import path, makedirs
from typing import Any


def save_json_to_file(json_str: Any, file_path: str, file_name: str):
    """
    Saves a JSON object or JSON string to a specified file with proper indentation. Creates the specified directory
    if it does not already exist.

    :param json_str: The JSON data to save. It can be either a JSON string or an object.
    :param file_path: The directory path where the file will be saved.
    :param file_name: The name of the file including the extension, e.g., `cemilan--biskuit1.json`
    :raises JSONDecodeError: If `json_str` is an invalid JSON string and cannot be decoded.
    """
    save_path = path.join(file_path, file_name)
    if not path.exists(file_path):
        makedirs(file_path)
    with open(save_path, 'w', encoding='utf-8') as f:
        if type(json_str) is str:
            json_str = JSONDecoder().decode(json_str)
        # noinspection PyTypeChecker
        dump(json_str, f, indent=4)


def rupiah_str_to_int(rupiah_str: str) -> int:
    """
    Converts a formatted Rupiah currency string into an integer.

    Example
    -------
    >>> rupiah_str_to_int('Rp 1.000.000')
    1000000
    >>> rupiah_str_to_int('IDR 5.000.000,00')
    5000000

    :param rupiah_str: A string representing Rupiah currency.
    :return: The numeric value of the Rupiah string as an integer.
    """
    rupiah_str = rupiah_str.split(',')
    filtered_string = [x for x in rupiah_str[0] if x.isdigit()]
    return int("".join(filtered_string))
