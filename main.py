from common import store_to_json
from scraping_courses_link import get_courses_links, open_links
from setup import is_config_need, has_unknown_ags, unknown_arg, run_config, is_install_need, run_install
from telegram import just_url_formatter
from telegram_view import TelegramView


if __name__ == '__main__':
    if has_unknown_ags():
        unknown_arg()

    if is_conf := is_config_need():
        run_config()

    if is_install_need() or is_conf:
        run_install()
    telegram = TelegramView()

    telegram.chats()
    telegram.filter_chats()
    telegram.select_chat()
    messages = telegram.messages()
    print("End getting the links from telegram page!!")
    print(len(messages))
    formatted_messages = just_url_formatter(messages)

    print(len(formatted_messages))
    print("")
    print("Start saving to json file")
    store_to_json('messages', formatted_messages)
    print("End to save the json file")

    print("")
    print("Star getting the real links: ")
    links = [message['url'] for message in formatted_messages]
    print(len(links))


    courses_links, errors = get_courses_links(links)
    print("End getting the real courses links!!")

    print("")
    print("Start saving to json file")
    store_to_json('courses_links', courses_links)
    print("End to save the json file")

    if errors:
        print("")
        print("Start saving errors to json file")
        store_to_json('error_links', errors)
        print("End to save errors json file")

    print("")
    print("Starting opening urls on browser")
    open_links(courses_links)
    print("End to save the json file")