# -*- coding: utf-8 -*-

# import required libs
import json
import requests
import time
import urllib

# make random available
from random import randint

# import the database
from db_helper import DBHelper

db = DBHelper()

# connect to the bot
TOKEN = "464368472:AAGfh1lZGi-B7Afty2dY8GWgoS27vKUO1og"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

""" receive the data from the message and convert it to json
would be fast to have the string + json conversion in just one function.
if there's an alternative of send_data calling get_data, apply it:
def get_data(URL)
    response = response.requests.get(URL)
    content_string = response.content.decode("utf8") #make it a string
    js = json.loads(content_string)
    return js
"""

# get link string
def get_data(url):
    response = requests.get(URL)
    content_string = response.content.decode("utf8")
    return content_string

# parse the content_string to the py library:
def get_json_data(url):
    content_string = get_data(URL)
    js_data = json.loads(content_string)
    return js_data

# longpoll it: https://goo.gl/6HrKWZ
def get_updates(offset = None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_data(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# process the input data
def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        # simply resend the chat
        send_message(text, chat)

def get_last_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    print(text) # visually check the result
    return (text)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    get_data(url)

def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
