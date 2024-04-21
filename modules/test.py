import json
import requests
import re
import websocket


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    "x-csrftoken": "a",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://scratch.mit.edu",
}
data = json.dumps({"username": "herasium", "password": "Victor2020!"})
_headers = headers
_headers["Cookie"] = "scratchcsrftoken=a;scratchlanguage=en;"
request = requests.post(
            "https://scratch.mit.edu/login/", data=data, headers=_headers
        )
session_id = str(re.search('"(.*)"', request.headers["Set-Cookie"]).group())
session_id = str(session_id)
print(session_id)

conn = websocket.WebSocket()
conn.connect(
                "wss://clouddata.scratch.mit.edu",
                cookie="scratchsessionsid=" + session_id + ";",
                origin="https://scratch.mit.edu",
                enable_multithread=True,
                timeout=3
)

conn.send(json.dumps({"method": "handshake", "user": "herasium", "project_id": 1003965733}) + "\n")

while True:
    print(conn.connected)
    print(conn.recv())