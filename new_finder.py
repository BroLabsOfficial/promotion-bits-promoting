import os
import time
from typing import List, Union, Set

from dotenv import load_dotenv
from googletrans import Translator
from pyrogram import Client
from pyrogram.errors import UsernameInvalid, InviteHashExpired, UsernameNotOccupied, FloodWait
from pyrogram.types import Message

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


class MyData:
    def __init__(self, username, channel):
        self.username = username
        self.channel = channel

    def __str__(self):
        if 'https://t.me/' in self.channel:
            return f'Channel: {self.channel}, User: https://t.me/{self.username}'
        else:
            return f'Channel: https://t.me/{self.channel.replace("@", "")}   User: https://t.me/{self.username}'

    def __eq__(self, other):
        if isinstance(other, MyData):
            return self.channel == other.channel and self.username == other.username
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)


# deprecated
def search_all(client: Client, query: str, limit: int = 0):

    entities = []
    for msg in client.search_global(query, limit=limit):
        try:
            if not (
                    msg.from_user.is_deleted and
                    msg.from_user.is_bot and
                    msg.from_user.is_scam and
                    msg.from_user.is_fake
            ) and (
                    msg.from_user.status == 'recently'
            ):
                if msg.from_user.username:
                    for entity in msg.entities:
                        if entity.type == 'mention' or entity.type == 'url':
                            entities.append(MyData(
                                username=msg.from_user.username,
                                channel=msg.text[entity.offset:entity.offset + entity.length]
                            ))
                        elif entity.type == 'text_link':
                            entities.append(MyData(
                                username=msg.from_user.username,
                                channel=entity.url
                            ))

        except AttributeError:
            continue

    return entities


def print_entities_advanced(app: Client, entities: Union[List[MyData], Set[MyData]]):
    print(f'Total of {len(entities)} channels found.\n')
    counter = 0
    for e in entities:
        try:
            v = verify_channel(client=app, link=e.channel)
        except FloodWait as error:
            print(f'Flood error - sleeping for {error.x}')
            time.sleep(error.x)
            v = verify_channel(client=app, link=e.channel)
        if v:
            counter += 1
            print(f'{counter}. {str(e)}', end='\n')


def print_entities(entities: Union[List[MyData], Set[MyData]]):
    print(f'Total of {len(entities)} channels found.\n')
    for index, data in enumerate(entities):
        print(f'{index + 1}. {str(data)}', end='\n')


def is_message_fit(msg: Message):
    return \
        not (
                not msg.from_user.is_self and
                msg.from_user.is_deleted and
                msg.from_user.is_bot and
                msg.from_user.is_scam and
                msg.from_user.is_fake
        ) and (
                msg.from_user.status == 'online' or
                msg.from_user.status == 'recently' or
                msg.from_user.status == 'offline' or
                msg.from_user.status == 'within_week'
        ) and msg.from_user.username is not None


def verify_channel(client: Client, link: str):
    def is_english(text):
        return Translator().detect(text).lang == 'en'

    try:
        c = client.get_chat(link)
        if c.type == 'channel' and is_english(c.description):
            return True
        else:
            return False

    except UsernameInvalid:
        c = client.get_chat(link.replace('https://t.me/', '@'))
        if c.type == 'channel' and is_english(c.description):
            return True
        else:
            return False
    except (InviteHashExpired, UsernameNotOccupied):
        return False
    except AttributeError:
        return True


def main():
    with Client("my_account", API_ID, API_HASH) as app:

        dialogs = [d for d in app.get_dialogs() if d.chat.type == 'supergroup']
        entities = set()

        for d in dialogs:
            results = app.search_messages(
                chat_id=d.chat.id,
                query='#new'
            )
            for msg in results:
                if is_message_fit(msg):
                    for entity in msg.entities:
                        if entity.type == 'mention' or entity.type == 'url':
                            entities.add(MyData(
                                username=msg.from_user.username,
                                channel=msg.text[entity.offset:entity.offset + entity.length]
                            ))
                        elif entity.type == 'text_link':
                            entities.add(MyData(
                                username=msg.from_user.username,
                                channel=entity.url
                            ))

        print_entities(entities)


if __name__ == '__main__':
    main()
    # for index, channel in entities:
    #     app.
    # print()
    # print(entities)
    # print(len(results))
    # for message in app.search_global("#new"):
    #     print('Ok')
    #     print(message.text)
