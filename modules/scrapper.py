import requests
from bs4 import BeautifulSoup
import requests
import random
from tqdm import tqdm
import json
import re 
import firebase_admin
from firebase_admin import credentials, db
import threading
from proxy import ProxyScraper
from flask import Flask
from tqdm import tqdm
file_path = "accounts.txt"
count = 0
with open(file_path, 'r') as file:
    count = len(file.read().split(";"))
buffer = ["griffpatch"]
already = []

print("FETCHING PROXYS")
proxy_list = ProxyScraper().Scraper()
print("PROXY LIST")


def scan_user_followers(user,count):
    url = f'https://scratch.mit.edu/users/{user}/followers/'
    page = 1
    ids = [user]
    buffer.pop(0)
    already.append(user)
    sc = count
    count += 1

    while True:
            new_url = url+f"?page={page}"
            response = requests.get(new_url,timeout=5)
            if response.status_code == 404:
                break
        
            soup = BeautifulSoup(response.text, 'html.parser')
            span_class = 'title'
            span_tags = soup.find_all('span', class_=span_class)
            for span_tag in span_tags:
                links = span_tag.find_all('a')
                for link in links:
                    new_user = link.get('href').split("/")[2]
                    count+=1
                    if not new_user in buffer and not new_user in already:
                        buffer.append(new_user)
                    ids.append(new_user)
            page += 1
    with open(file_path, 'a') as file:
        for id in ids:
            file.write(id+";")
    print(f"Added user {user}, new count: {count} (+{count-sc})")
    return count

def run_loop(count):
    while True:
        try:
            count = scan_user_followers(buffer[0],count)
        except Exception as e:
           print(e)
            
run_loop(count)

while True:
    pass