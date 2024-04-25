import random

string = ""

with open("accounts.txt","r") as file:
    string = file.read()

accounts = string.split(";")

print("User List Lenght:",len(accounts))

def random_user():
    return random.choice(accounts)