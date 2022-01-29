from common import *
import credentials
import os
import sys

def requirements() -> None:
    print(plus_simbol_text('Installing requierments ...'))
    install_requirements()
    print(plus_simbol_text('requierments Installed.\n'))


def config_setup() -> None:
	
    api_id = input(plus_simbol_text('enter api ID : ' + RE))
    api_hash = input(plus_simbol_text('enter hash ID : ' + RE))
    phone = input(plus_simbol_text('enter phone number : ' + RE))

    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone
    }
    credentials.save_credentials(config)

    print(plus_simbol_text('setup complete !'))


def install_requirements() -> None:
    os.system("""
		pip3 install -r requirements.txt
		python3 -m pip install -r requirements.txt
		touch config.data
		""")

print(sys.argv)
if len(sys.argv) < 2:
    print(emphasis_format('!') +
          'no args given, running default configuration & install')
    print(emphasis_format('!') + 'for help use : ')
    print(emphasis_format('!') +
          'https://github.com/')
    print(GR + '$ python3 setup.py -h' + '\n')
    proced = input(emphasis_format('+') +
                   'do you want to procced (y/n): ').lower()
    if proced == 'y':
        config_setup()
        requirements()
    exit(0)

arg = sys.argv[1]
INSTALL = ['--install', '-i']
CONFIG = ['--config', '-c']
HELP = ['--help', '-h']
OPTIONS = INSTALL + CONFIG + HELP

if not [i for i in arg if i in OPTIONS]:
    print('\n'+emphasis_format('!') + 'unknown argument : ' + arg)
    print(emphasis_format('!') + 'for help use : ')
    print(GR + '$ python3 setup.py -h' + '\n')
    exit(0)

if [i for i in arg if i in CONFIG]:
    print(emphasis_format('+') + 'selected module : ' + RE + arg)
    config_setup()
if [i for i in arg if i in INSTALL]:
    requirements()
if [i for i in arg if i in HELP]:
    print("""$ python3 setup.py
		( --config  / -c ) setup api configration
		( --install / -i ) install requirements
		( --help    / -h ) show this msg 
		""")
