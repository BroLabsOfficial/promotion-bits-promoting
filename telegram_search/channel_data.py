class ChannelData:
    def __init__(self, username, channel):
        self.username = username
        self.channel = channel

    def __str__(self):
        if 'https://t.me/' in self.channel:
            return f'Channel: {self.channel}, User: https://t.me/{self.username}'
        else:
            return f'Channel: https://t.me/{self.channel.replace("@", "")}   User: https://t.me/{self.username}'

    def __eq__(self, other):
        if isinstance(other, ChannelData):
            return self.channel == other.channel and self.username == other.username
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.channel + self.username)
