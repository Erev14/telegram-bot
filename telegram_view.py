from telethon.errors import SessionPasswordNeededError

from common import emphasis_format, plus_symbol_text, RE
from telegram import Telegram

def _digit_input(text):
    response = input(f'{plus_symbol_text(text)}')
    if response.isdigit():
        return int(response)
    return response


def _new_value_input(text, current_value):
    new_val =input(f'{plus_symbol_text(text)} (Current value: {current_value}). New Value: ')
    if new_val:
        return int(new_val)
    return current_value


def _change_message(text):
    return input(f'{emphasis_format("!")}{text} y/n: ') == "y"


class TelegramView:

    def __init__(self):
        self.telegram = Telegram()
        print("Client Created")

        # Ensure you're authorized
        if not self.telegram.client.is_connected():
            try:
                self.telegram.connect()
            except KeyError:
                print(f'{emphasis_format("!")} run python3 main.py -c first !!\n')
                exit(1)

        if not self.telegram.client.is_user_authorized():
            try:
                self.telegram.sign_in()
            except SessionPasswordNeededError:
                self.telegram.sign_in_retry(input(f'{plus_symbol_text("Password: ")} {RE}'))

    def chats(self):
        last_day = None
        chunk_size = 200
        if _change_message("Change default values?"):
            last_day = _new_value_input("Last Day", last_day)
            chunk_size = _new_value_input("Chunk Size", chunk_size)
        return self.telegram.get_chats(last_day=last_day, chunk_size=chunk_size)

    def filter_chats(self):
        if _change_message("Filter chats by type?"):
            print(f'{plus_symbol_text("Choose a group to scrape :")} {RE}')
            for i, chat_type in enumerate(self.telegram.CHAT_TYPES):
                print(f'{emphasis_format(str(i))} - {chat_type}')
            print(f'{emphasis_format(str(i + 1))} - All')
            print('')
            chat_type_selected = _digit_input("Enter a Number : ")
            self.telegram.filter_chats(chat_type_selected)

    # Select the channel/group
    def select_chat(self):
        print('')
        print(f'{plus_symbol_text("Choose a chat to scrape :")} {RE}')

        for i, chat in enumerate(self.telegram.chats):
            print(f'{emphasis_format(str(i))} - {chat.title}')

        print('')
        group_index_selected = _digit_input("Enter a Number : ")
        self.telegram.target_group = self.telegram.chats[group_index_selected]

    def messages(self):
        # offset_id = 0
        offset_id = 7594
        offset_date = None
        limit = 11
        all_messages = []
        total_messages = 0
        add_offset = 0
        max_id = 0
        min_id = 0
        total_count_limit = 11
        if _change_message("Change default values?"):
            offset_id = _new_value_input("Offset Id", offset_id)
            offset_date = _new_value_input("Offset Date", offset_date)
            limit = _new_value_input("Limit", limit)
            all_messages = _new_value_input("All Messages", all_messages)
            total_messages = _new_value_input("Total Messages", total_messages)
            add_offset = _new_value_input("Add Offset", add_offset)
            max_id = _new_value_input("Max Id", max_id)
            min_id = _new_value_input("Min Id", min_id)
            total_count_limit = _new_value_input("Total Count Limit", total_count_limit)

        entity = None
        if self.telegram.target_group is None:
            entity = _digit_input("enter entity(telegram URL or entity id):")
        self.telegram.select_entity(entity)

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            if messages := self.telegram.messages(
                    offset_id, offset_date, limit, all_messages, total_messages, add_offset, max_id, min_id):
                for message in messages:
                    all_messages.append(message.to_dict())

                offset_id = messages[len(messages) - 1].id
                total_messages = len(all_messages)

            else:
                break

            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        return all_messages

