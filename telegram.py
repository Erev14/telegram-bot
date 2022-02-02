from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, GetHistoryRequest
from telethon.tl.types import InputPeerEmpty, Chat, Channel
from telethon.tl.types import (
    PeerChannel
)

import credentials
from common import RE, plus_symbol_text


def just_url_formatter(data):
    new_data = []
    for message in data:
        if message['reply_markup']:
            if 'rows' in message['reply_markup']:
                for row in message['reply_markup']['rows']:
                    for button in row['buttons']:
                        if button['text'] == "Ir al Curso":
                            new_data.append(
                                {"id": message['id'], "message": message['message'], "url": button['url']}
                            )
                            break
    return new_data


class Telegram:
    def __init__(self):
        self.entity = None
        credential = credentials.load_credentials()
        self.api_id = credential['api_id']
        self.api_hash = credential['api_hash']
        self.phone = credential['phone']

        # Create the client and connect
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        self.client.start()

        self.chats = []
        self.target_group = None
        self.CHAT_TYPES = ['Channel', 'Chat', 'Mega Group']

    def connect(self):
        self.client.connect()

    def sign_in(self):
        self.client.send_code_request(self.phone)
        self.client.sign_in(self.phone, input(f'{plus_symbol_text("Enter the code: ")} {RE}'))

    def sign_in_retry(self, password):
        self.client.sign_in(password=password)

    def get_me(self):
        self.client.get_me()

    # Get just channels
    def get_chats(self, last_day=None, chunk_size=200):
        chats = []
        result = self.client(GetDialogsRequest(
            offset_date=last_day,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        self.chats = chats
        return self.chats

    # Get selected channel types
    # | Channel 0 | Chat 1 | Megagroup 2 | All 3 |
    def filter_chats(self, chat_type_selected):
        chats = self.chats
        self.chats = []
        if chat_type_selected == 3:
            self.chats.extend(chats)
        elif chat_type_selected == 2:
            self.chats.extend(chat for chat in self.chats if type(chat) is Channel and chat.megagroup)
        elif chat_type_selected == 1:
            self.chats.extend(filter(lambda chat: type(chat) is Chat, chats))
        elif chat_type_selected == 0:
            self.chats.extend(filter(lambda chat: type(chat) is Channel, chats))

    def select_entity(self, channel=None):
        if self.target_group is None:
            if channel is None:
                raise Exception("if not target group selected, need to send a channel")
            if channel.isdigit():
                entity = PeerChannel(channel)
            else:
                entity = channel
        else:
            entity = PeerChannel(self.target_group.id)
        self.entity = self.client.get_entity(entity)

    def messages(self, offset_id=0, offset_date=None, limit=100, all_messages=[], total_messages=0,
                     add_offset=0, max_id=0, min_id=0):
        history = self.client(GetHistoryRequest(
            peer=self.entity,
            offset_id=offset_id,
            offset_date=offset_date,
            add_offset=add_offset,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            hash=0
        ))
        return history.messages
    # def get_messages(self):
    #     if self.target_group is None:
    #         user_input_channel = input("enter entity(telegram URL or entity id):")
    #         if user_input_channel.isdigit():
    #             entity = PeerChannel(int(user_input_channel))
    #         else:
    #             entity = user_input_channel
    #     else:
    #         entity = PeerChannel(self.target_group.id)
    #
    #     my_channel = self.client.get_entity(entity)
    #
    #     offset_id = 7524
    #     limit = 100
    #     all_messages = []
    #     total_messages = 0
    #     total_count_limit = 10
    #
    #     while True:
    #         print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    #         history = self.client(GetHistoryRequest(
    #             peer=my_channel,
    #             offset_id=offset_id,
    #             offset_date=None,
    #             add_offset=0,
    #             limit=limit,
    #             max_id=0,
    #             min_id=0,
    #             hash=0
    #         ))
    #         if not history.messages:
    #             break
    #         messages = history.messages
    #         for message in messages:
    #             all_messages.append(message.to_dict())
    #         offset_id = messages[len(messages) - 1].id
    #         total_messages = len(all_messages)
    #         if total_count_limit != 0 and total_messages >= total_count_limit:
    #             break
    #     return all_messages


    # def get_chats(self):
    #     chats = []
    #     LAST_DATE = None
    #     CHUNK_SIZE = 200
    #     chat_types = ['Channel', 'Chat', 'Mega Group']
    #     result = self.client(GetDialogsRequest(
    #         offset_date=LAST_DATE,
    #         offset_id=0,
    #         offset_peer=InputPeerEmpty(),
    #         limit=CHUNK_SIZE,
    #         hash=0
    #     ))
    #     # Get just channels
    #     chats.extend(result.chats)
    #
    #     # Select chat type
    #     print(f'{plus_symbol_text("Choose a group to scrape :")} {RE}')
    #
    #     for i, chat_type in enumerate(chat_types):
    #         print(f'{emphasis_format(str(i))} - {chat_type}')
    #
    #     print(f'{emphasis_format(str(i + 1))} - All')
    #     print('')
    #     chat_type_selected = int(input(f'{plus_symbol_text("Enter a Number : ")} {RE}'))
    #
    #     # get selected channel types
    #     # | Channel 0 | Chat 1 | Megagroup 2 | All 3 |
    #     if chat_type_selected == 3:
    #         self.groups.extend(chats)
    #     elif chat_type_selected == 2:
    #         self.groups.extend([chat for chat in chats if type(chat) is Channel and chat.megagroup])
    #     elif chat_type_selected == 1:
    #         self.groups.extend(filter(lambda chat: type(chat) is Chat, chats))
    #     elif chat_type_selected == 0:
    #         self.groups.extend(filter(lambda chat: type(chat) is Channel, chats))
    #
    #     print('')
    #     # Select the channel/group
    #     print(f'{plus_symbol_text("Choose a group to scrape :")} {RE}')
    #
    #     for i, group in enumerate(self.groups):
    #         print(f'{emphasis_format(str(i))} - {group.title}')
    #
    #     print('')
    #     group_index_selected = input(f'{plus_symbol_text("Enter a Number : ")} {RE}')
    #
    #     self.target_group = self.groups[int(group_index_selected)]
    #
    #
    #
