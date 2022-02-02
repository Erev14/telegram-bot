import json
from os import path

RE = "\033[1;31m"
GR = "\033[1;32m"
CY = "\033[1;36m"
CONFIG_FILE_NAME = 'config.ini'
JSON_FILES = 'export'


def store_to_json(file_name, data):
    file_path = f'./{path.join(JSON_FILES, file_name)}.json'
    if _file_exist(file_path):
        with open(file_path, 'r+') as f:
            f.seek(0)
            f.truncate()
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, default=str)


def plus_symbol_text(text: str) -> str:
    return f'{GR} [+] {text}'


def emphasis_format(text: str) -> str:
    return f'{GR} [ {RE} {text} {GR} ] {CY} '


def aks_for_proceed():
    return input(f'{emphasis_format(" + ")} do you want to proceed (y/n): ').lower()


def get_config_path() -> str | None:
    if _is_on_default_path():
        return CONFIG_FILE_NAME

    return _get_location_path()


def _get_location_path() -> str | None:
    if not "y" == input(f'{plus_symbol_text("Do you have a config.ini file? y/n")}'):
        return
    _request_path()


def _request_path():
    i = 0
    while i < 3:
        print('')
        location = input(f'{plus_symbol_text("enter the file location")}')
        real_file = path.join(location, CONFIG_FILE_NAME)
        if _file_exist(real_file): return real_file
        i += 1
    return


def _file_exist(file):
    return path.isfile(file)


def _is_on_default_path():
    return _file_exist('config.ini')
