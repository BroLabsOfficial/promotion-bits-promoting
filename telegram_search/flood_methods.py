import time
from typing import List
from typing import Set
from typing import Union

from googletrans import Translator
from pyrogram import Client
from pyrogram.errors import UsernameInvalid, InviteHashExpired, UsernameNotOccupied, FloodWait

from telegram_search.channel_data import ChannelData


def print_entities_advanced(app: Client, entities: Union[List[ChannelData], Set[ChannelData]]):
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
