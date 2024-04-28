from bs4 import BeautifulSoup
import requests
from __main__ import proxies
import random
from tqdm import tqdm
import json
import re 
from datetime import datetime, timedelta
import queue
import time
from threading import Thread,current_thread

proxy_list = proxies

def scan_all_users_project(user):

    url = f'https://scratch.mit.edu/users/{user}/projects/'
    page = 1
    ids = []

    while True:
        new_url = url+f"?page={page}"
        response = requests.get(new_url,proxies=random.choice(proxy_list))
        if response.status_code == 404:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        span_class = 'title'
        span_tags = soup.find_all('span', class_=span_class)
        for span_tag in span_tags:
            links = span_tag.find_all('a')
            for link in links:
                ids.append(link.get('href').split("/")[2])
        page += 1
    return ids


def request_projects(user, project_list, stats):
    for project_id in project_list:
        try:
            response = requests.get(f"https://api.scratch.mit.edu/projects/{project_id}")
            data = response.json()["stats"]
            stats["favorites"] += data["favorites"]
            stats["loves"] += data["loves"]
            stats["remixes"] += data["remixes"]
            stats["views"] += data["views"]
        except Exception as e:
            print("Error:", e, current_thread().name)

def get_user_stats(user):
    projects = scan_all_users_project(user)
    stats = {
        "favorites": 0,
        "loves": 0,
        "remixes": 0,
        "views": 0,
        "followers": get_followers(user)
    }
    thread = 0
    lists = [[] for _ in range(10)]

    for project_id in projects:
        if thread > 9:
            thread = 0
        lists[thread].append(project_id)
        thread += 1
    print("Dispateched",len(projects),f"projects in 10 threads ({len(lists[0])} each)")
    threads = []
    for i in range(10):
        thread = Thread(target=request_projects, args=(user, lists[i], stats))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return stats

def get_meta_data(user):
    response = requests.get(f"https://api.scratch.mit.edu/users/{user}",proxies=random.choice(proxy_list))
    data = response.json()
    meta = {
        "admin":data["scratchteam"],
        "id":data["id"],
        "joined":data["history"]["joined"],
        "img":data["profile"]["images"],
        "country":data["profile"]["country"]
    }

    return meta
def get_followers(user):
        response = requests.get(f"https://scratch.mit.edu/users/{user}/followers/",proxies=random.choice(proxy_list),headers={"Accept-Language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"})
        soup = BeautifulSoup(response.text, 'html.parser')
        span_tags = soup.find_all('h2')
        pattern = r'\((.*?)\)'
        followers = -1

        for span_tag in span_tags:
            if span_tag.find("a") : 
                followers = re.findall(pattern, span_tag.text)[0]
        return int(followers)


# Scores:
# + 100 Followers: +5 
# + 1000 Followers: +15
# + 10000 Followers: +20
# + 100000 Followers: +35

# + 100 Views: +5
# + 5000 Views: +5
# + 50000 Views: +15
# + 500000 Views: +15
# + 10000000 Views: + 30
# + 100000000 Views: +50

# + 100 Likes: +5
# + 1000 Likes: +5
# + 10000 Likes: +15
# + 100000 Likes: +15

# + 100 Favorites: +10
# + 1000 Favorites: +15
# + 10000 Favorites: +20
# + 100000 Favorites: +25

# + 100 Remixes: +5
# + 500 Remixes: +7
# + 1000 Remixes: +10
# + 10000 Remixes: +15
# + 100000 Remixed: +20

# France:  +5

# Id - 10000000: +5
# Id - 1000000: +10
# Id - 1000: +25
# Id - 100: +100

# 5 years ago: +5
# 10 yeras ago: +20
# 15  years ago: +50

# Admin +50

 # Scores:
scores = {
    "followers": {
        100: 5,
        1000: 15,
        10000: 20,
        100000: 35
    },
    "views": {
        100: 5,
        5000: 5,
        50000: 15,
        500000: 15,
        10000000: 30,
        100000000: 50
    },
    "likes": {
        100: 5,
        1000: 5,
        10000: 15,
        100000: 15
    },
    "favorites": {
        100: 10,
        1000: 15,
        10000: 20,
        100000: 25
    },
    "remixes": {
        100: 5,
        500: 7,
        1000: 10,
        10000: 15,
        100000: 20
    },
    "country": 5,
    "admin": 50,
    "id": {
        100: 100,
        1000: 25,
        1000000: 10,
        10000000: 5
    },
    "join_date": {
        5: 5,
        10: 20,
        15: 50
    }
}



# Define rewards with unique IDs
rewards = {
    1: "100 Followers",
    2: "1000 Followers",
    3: "10000 Followers",
    4: "100000 Followers",
    5: "100 Views",
    6: "5000 Views",
    7: "50000 Views",
    8: "500000 Views",
    9: "10000000 Views",
    10: "100000000 Views",
    11: "100 Likes",
    12: "1000 Likes",
    13: "10000 Likes",
    14: "100000 Likes",
    15: "100 Favorites",
    16: "1000 Favorites",
    17: "10000 Favorites",
    18: "100000 Favorites",
    19: "100 Remixes",
    20: "500 Remixes",
    21: "1000 Remixes",
    22: "10000 Remixes",
    23: "100000 Remixes",
    24: "France",
    25: "ID - 10000000",
    26: "ID - 1000000",
    27: "ID - 1000",
    28: "ID - 100",
    29: "5 years ago",
    30: "10 years ago",
    31: "15 years ago",
    32: "Admin"
}

# Function to get score
def get_score(user):
    stats = get_user_stats(user)
    
    meta_data = get_meta_data(user)
    score = 0
    rewarded_texts = []  # List to store rewarded texts
    
    # Function to reward points
    def reward_points(points, reward_text):
        nonlocal score
        
        score += points
        rewarded_texts.append(reward_text)

    # Calculate score based on followers
    s = 1
    
    for threshold, points in scores["followers"].items():
        if stats["followers"] >= threshold:
            reward_points(points, s)
        s+=1

    # Calculate score based on views
    for threshold, points in scores["views"].items():
        if stats["views"] >= threshold:
            reward_points(points, s)
        s+=1
    # Calculate score based on likes
    for threshold, points in scores["likes"].items():
        if stats["favorites"] >= threshold:
            reward_points(points, s)
        s+=1
    # Calculate score based on favorites
    for threshold, points in scores["favorites"].items():
        if stats["favorites"] >= threshold:
             reward_points(points, s)
        s+=1
    # Calculate score based on remixes
    for threshold, points in scores["remixes"].items():
        if stats["remixes"] >= threshold:
            reward_points(points, s)
        s+=1
    # Add country-specific score
    if meta_data["country"] == "France":
        reward_points(scores["country"], 24)

    # Add admin score
    if meta_data["admin"]:
        reward_points(scores["admin"], 32)

    # Additional scoring based on project IDs and join date
    
    
    if meta_data["id"] >= 10000000:
            reward_points(scores["id"][10000000], 25)
    elif meta_data["id"] >= 1000000:
            reward_points(scores["id"][1000000], 26)
    elif meta_data["id"] >= 1000:
            reward_points(scores["id"][1000], 27)
    elif meta_data["id"] >= 100:
            reward_points(scores["id"][100], 28)
    
    join_date = datetime.strptime(meta_data["joined"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if join_date <= (datetime.now() - timedelta(days=5*365)):
            reward_points(scores["join_date"][5], 29)
    elif join_date <= (datetime.now() - timedelta(days=10*365)):
            reward_points(scores["join_date"][10], 30)
    elif join_date <= (datetime.now() - timedelta(days=15*365)):
            reward_points(scores["join_date"][15], 31)
    
    
    return score, rewarded_texts

def get_rank(score):
    if score >= 200:
        return "S"
    elif score >= 150:
        return "A"
    elif score >= 100:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 20:
        return "D"
    elif score >= 0:
        return "F"
    else:
        return "Beyond"

class Score():
    def __init__(self,user,score,rank,texts):
        self.user = user
        self.score = score
        self.rank = rank
        self.texts = texts

class User():
    def __init__(self,user):
        self.user = user

    def get_score(self):
        self.score, self.rewarded_texts = get_score(self.user)
        self.rank = get_rank(self.score)
        return Score(self.user,self.score,self.rank,self.rewarded_texts)
    
    def get_meta(self):
        return get_meta_data(self.user)