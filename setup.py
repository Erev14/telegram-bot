import os
import credentials
from common import GR, RE, plus_symbol_text, emphasis_format, aks_for_proceed, CONFIG_FILE_NAME, _is_on_default_path
from sys import argv

if len(argv) < 2:
    arg = []
else:
    arg = argv # note if import sys, sys.argv[1]. if from sys import argv, argv
INSTALL = ['--install', '-i']
CONFIG = ['--config', '-c']
HELP = ['--help', '-h']
OPTIONS = INSTALL + CONFIG + HELP


def no_setup_error():
    print(f'{emphasis_format("!")} run python3 setup.py first !!\n')
    print(f'{emphasis_format("!")} for help use : ')
    print(f'{GR} $ python3 setup.py -h\n')
    exit(1)


def has_unknown_ags():
    if len(arg) < 2:
        return False
    return not [i for i in arg if i in OPTIONS]


def unknown_arg():
    print(f'\n{emphasis_format("!")} unknown argument : {arg}')
    print(f'{emphasis_format("!")} for help use : ')
    print(f'{GR} $ python3 setup.py -h\n')
    exit(1)


def is_config_need():
    if len(arg) < 2:
        return not _is_on_default_path()
    return [i for i in arg if i in CONFIG]


def run_config():
    if aks_for_proceed() == 'y':
        config_setup()
        print(plus_symbol_text('setup complete !'))
    exit(1)


def config_setup() -> None:
    api_id = input(f'{plus_symbol_text("enter api ID : " + RE)}')
    api_hash = input(f'{plus_symbol_text("enter hash ID : " + RE)}')
    phone = input(f'{plus_symbol_text("enter phone number : " + RE)}')

    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone
    }
    credentials.save_credentials(config)


def is_install_need():
    return [i for i in arg if i in INSTALL]


def run_install() -> None:
    print(plus_symbol_text('Installing requirements ...'))
    install_requirements()
    print(plus_symbol_text('requirements Installed.\n'))


def install_requirements() -> None:
    os.system(
        f'pip3 install -r requirements.txt && python3 -m pip install -r requirements.txt && touch {CONFIG_FILE_NAME}'
    )


def is_help_need():
    return [i for i in arg if i in HELP]


def run_help():
    print("""$ python3 main.py
            ( --config  / -c ) setup api configuration
            ( --install / -i ) install requirements
            ( --help    / -h ) show this msg
            """)
