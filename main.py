from common import *
import credentials
from tokenize import group
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
import sys

try:
    credential = credentials.load_credentials()
    api_id = credential['id']
    api_hash = credential['hash']
    phone = credential['phone']
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
except KeyError:
    os.system('clear')

    print(emphasis_format('[!]') + 'run python3 setup.py first !!\n')
    sys.exit(1)

if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')

    client.sign_in(phone, input(plus_simbol_text('Enter the code: ') + RE))

os.system('clear')

chats = []
last_date = None
chunk_size = 200
groups = []
result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(plus_simbol_text('Choose a group to scrape members :') + RE)

for i, group in enumerate(groups):
    print(emphasis_format(i) + ' - ' + group.title)

print('')
g_index = input(plus_simbol_text('[+] Enter a Number : ') + RE)
target_group = groups[int(g_index)]
