# USAGE

Create a export folder into the root path

Made a copy from config.example.ini as config.ini

Change the values in config.ini, see [this](##to get an api id and hash)
section about how to get the api id and hash


Alternatively run main.py -c -i or just run main.py
If no config.ini file is found will create it for you, asking for the values
on the command line


The -i option call pip to install all dependencies


I'm working with to create new features, for now:

- Stablish a connection with telegram API.
- Gets your chats.
- Start scraping the messages from the selected chat.
- And for personal usage 


https://t.me/UCupones group send daily courses with CODES that make 100% free
so for personal usage I scrap that group and process the data to get the
real link from the course and open on new tabs all the links

## to get an api id and hash

- https://my.telegram.org/apps

# API DOC:

- https://core.telegram.org/schema

# base on:

- https://betterprogramming.pub/how-to-get-data-from-telegram-82af55268a4b

- https://github.com/th3unkn0n/TeleGram-Scraper
