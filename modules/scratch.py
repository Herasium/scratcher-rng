import requests
import random
import time
from cachetools import TTLCache
import hashlib
import math
import datetime
import websocket
import json
import re 
from .exceptions import *
import scratchattach
from __main__ import proxies as proxy_list

chars = [
    '','','','','','','','','','',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', ';', ':', '!', '?', '.', '/', '&',
    '"',"'", '#', '[', '(', ')', ']', '=', '+', '*', '-', '_', ',', '{', '}',"\\"
]


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    "x-csrftoken": "a",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://scratch.mit.edu",
}

class Account():
    def __init__(self,username,password):
        self.proxies = proxy_list

        data = json.dumps({"username": username, "password": password})
        _headers = headers
        _headers["Cookie"] = "scratchcsrftoken=a;scratchlanguage=en;"
        request = requests.post(
            "https://scratch.mit.edu/login/", data=data, headers=_headers, proxies=random.choice(self.proxies)
        )
        session_id = str(re.search('"(.*)"', request.headers["Set-Cookie"]).group())
        self.session_id = str(session_id)
        self.username = username
        self.headers = headers
        self.cookies = {
            "scratchsessionsid" : self.session_id,
            "scratchcsrftoken" : "a",
            "scratchlanguage" : "en",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            self._headers.pop("Cookie")
        except Exception: pass
        self.get_csrftoken()

    def get_csrftoken(self):
        r = requests.get("https://scratch.mit.edu/csrf_token/").headers
        csrftoken = r["Set-Cookie"].split("scratchcsrftoken=")[1].split(";")[0]
        self.headers["x-csrftoken"] = csrftoken
        self.cookies["scratchcsrftoken"] = csrftoken

class Request():
    def __init__(self,data,project):
        self.project = project
        self.data = data["value"]
        self.timestamp = data["timestamp"]
        self.user = data["user"]
        self.var = data["name"].split("☁")[1]
        self.type = data["verb"]

class Encoder():
    def encode(self,string):
        string = str.lower(string)
        result = ""
        for char in string: result += str(chars.index(char))
        return result
    def decode(self, string):
        count = 0
        string = str(string)
        result = [""]
        for count in range(0, len(string), 2):
            current = string[count:count+2]  
            id = chars[int(current)]
            if id == "\\":
                result.append("") 
            else:
                result[-1] += id 
        return result



class ScratchProject():
    def __init__(self,project_id,account: Account):
        self.project_id = project_id
        self.account = account
        self.username = account.username
        self.session_id = account.session_id
        self.acc = scratchattach.Session(session_id=self.session_id,username=self.username)
        self.request_cache = TTLCache(maxsize=128, ttl=600)
        self.proxies = proxy_list

    def on_event(self,function):
        self.on_event_func = function

    def start(self):
        while True:
            try:
                data = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit=128&offset=0",proxies=random.choice(self.proxies),timeout=10)
                for request in data.json():
                    if time.time() - request["timestamp"]/1000 <= 60:
                        hash = hashlib.sha1(str.encode(str(request["user"])+str(request["value"])+request["name"])).hexdigest()
                        if not hash in self.request_cache:
                            new = Request(request,self.project_id)
                            self.request_cache[hash] = True
                            self.on_event_func(new)
            except Exception as e:
                print(e)

            time.sleep(0.15)
    def send(self,var,data):
        self.conn = self.acc.connect_cloud(self.project_id)
        self.conn.set_var(var,int(data))
        self.conn.disconnect()

