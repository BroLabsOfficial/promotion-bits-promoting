from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True)
class MyData:
    username: str
    channel: str

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


a = MyData(username='a', channel='c')
b = MyData(username='a', channel='c')
c = deepcopy(1)
d = deepcopy(1)
print(a == b, a is b)
print(c == d,  c is d)
s = set()
# s.add(c)
# s.add(d)
s.add(a)
s.add(a)
s.add(b)
print(s, len(s))
