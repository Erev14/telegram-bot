import configparser

config_parser = configparser.RawConfigParser()


def save_credentials(dic: dict) -> None:
    config_parser.add_section('credentials')
    for key, val in dic.items():
        config_parser.set('credentials', key, val)
    with open('config.ini', 'w', encoding='UTF-8') as setup:
        config_parser.write(setup)


def load_credentials() -> dict:
    config_parser.read('config.ini')
    return dict(config_parser['credentials'].items())
