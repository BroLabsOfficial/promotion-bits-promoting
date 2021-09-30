from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputPeerChannel

from telethon_sign_in import TelethonSignIn

API_ID = 1578213
API_HASH = '94b6e5d761205562494f410c4424c71d'
PHONE_NUMBER = '+19725979626'

client = TelethonSignIn(API_ID, API_HASH).sign_in_user(PHONE_NUMBER)
# print(dir(client))
# d = filter(c)
# dialogs = client.iter_dialogs()
# for dialog in dialogs:
#     if dialog.is_group:
#         print(dialog.entity.stringify())
#         break

groups = [dialog.entity for dialog in client.iter_dialogs() if dialog.is_group]
for g in groups:
    result = client(SearchRequest(
        InputPeerChannel(g.id, g.access_hash),
        q='#new',
        limit=None,
        filter=None,
        min_date=None,
        max_date=None,
        min_id=1,
        max_id=None,
        hash=0,
        offset_id=None,
        add_offset=0,
    ))
    print(result)

# for _ in client.iter_participants():
#     print(_.stringify())
#     break
# print(d.stringify())
# result = client(SearchRequest(
#     q='#new ',
#     limit=10**5,
# ))
# print(result.stringify())
