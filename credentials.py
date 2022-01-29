import configparser

config_parser = configparser.RawConfigParser()

def save_credentials(dic: dict) -> None:
    config_parser.add_section('credencials')
    for key, val in dic.items():
        config_parser.set('credencials', key, val)
    with open('config.ini', 'w') as setup:
        config_parser.write(setup)

def load_credentials() -> dict :
    config_parser.read('config.ini')
    return dict(config_parser['credentials'].items())
