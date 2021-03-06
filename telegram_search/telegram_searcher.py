from typing import List
from typing import Set
from typing import Union

from PyProfane import isProfane
from profanity import profanity
from profanity_check import profanity_check
from pyrogram import Client
from pyrogram.types import Message

from telegram_search.channel_data import ChannelData

API_ID = 1578213
API_HASH = '94b6e5d761205562494f410c4424c71d'


def is_link_nsfw(link: str):
    link = link.replace('https://t.me/', '').replace("@", '')

    def make_text_readable(text: str) -> str:
        def change_case(my_str: str) -> str:
            lst = []
            prev = False
            for c in my_str:
                if c.isupper() and not prev:
                    lst += f' {c.lower()}'
                    prev = True
                elif c.isupper() and prev:
                    lst += c.lower()
                else:
                    lst += c
                    prev = False

            return ''.join(lst)

        def remove_chars(my_str: str) -> str:
            my_str = my_str.replace('_', ' ')
            my_str = my_str.replace('  ', ' ')
            return my_str.strip()

        return remove_chars(change_case(text))

    def is_text_nsfw(text) -> bool:
        if text is None or text == '':
            return False

        check_of_alt_profanity_check = profanity_check.predict([text])
        if len(check_of_alt_profanity_check) == 1:
            alt_profanity_check_bool = check_of_alt_profanity_check[0] == 1
        else:
            for i in check_of_alt_profanity_check:
                if i == 1:
                    alt_profanity_check_bool = True
                    break
            else:
                alt_profanity_check_bool = False
        profanity_bool = profanity.contains_profanity(text)
        py_profane_bool = isProfane(text)

        return alt_profanity_check_bool or (profanity_bool and py_profane_bool)

    return is_text_nsfw(make_text_readable(link))


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


def print_entities(entities: Union[List[ChannelData], Set[ChannelData]]):
    print(f'Total of {len(entities)} channels found.\n')
    for index, data in enumerate(entities):
        print(f'{index + 1}. {str(data)}', end='\n')


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
                        if entity.type == 'mention':
                            e = 'https://t.me/' + msg.text[entity.offset:entity.offset + entity.length].replace("@", '')
                        elif entity.type == 'url':
                            e = msg.text[entity.offset:entity.offset + entity.length]
                        elif entity.type == 'text_link':
                            e = entity.url
                        else:
                            continue

                        if 'joinchat' in e or not is_link_nsfw(e):
                            entities.add(ChannelData(
                                username=msg.from_user.username,
                                channel=e
                            ))

        print_entities(entities)


if __name__ == '__main__':
    main()
