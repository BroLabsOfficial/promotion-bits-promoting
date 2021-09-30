from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient


def _connect(api_id, api_hash) -> TelegramClient:
    client = TelegramClient('User', api_id, api_hash)
    client.connect()
    return client


def _authorize_client(client: TelegramClient, phone_number):
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        try:
            client.sign_in(
                phone_number,
                input(f'A login code sent to your Telegram account.\nEnter the code: ')
            )
        except SessionPasswordNeededError:
            client.sign_in(password=input('Enter your password: '))


class TelethonSignIn:

    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash

    def sign_in_user(self, phone_number) -> TelegramClient:
        """
        create a telegram userbot
        :return: TelegramClient
        """
        client = _connect(api_id=self.api_id, api_hash=self.api_hash)
        _authorize_client(client=client, phone_number=phone_number)
        return client
