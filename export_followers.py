import json
import random
from src.insta_bot import Bot

#Load des fichiers
f = open('infos/accounts.json',)
accounts = json.load(f)

with open('infos/usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

with open('infos/targets.txt', 'r') as f:
    targets = [line.strip() for line in f]

#Lecture des accounts pour se log et init la fonction de message
while True:
    if not targets:
        print('No target.')
        break

    for account in accounts:
        if not targets:
            break

        insta = Bot(username=account["username"],
                        password=account["password"], headless=False)

        for i in range(10):

            if not targets:
                break

            target_user = targets.pop()

            insta.scrapFollowers(
                target_user=target_user)

        insta.teardown()