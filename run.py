import json
import random
from src.insta_bot import Bot
import clean_usernames

#Load des fichiers
f = open('infos/accounts.json',)
accounts = json.load(f)

with open('infos/usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

with open('infos/messages.txt', 'r') as f:
    messages = [line.strip() for line in f]


#Lecture des accounts pour se log et init la fonction de message
while True:
    if not usernames:
        print('Finished usernames.')
        break

    for account in accounts:
        if not usernames:
            break
        
        insta = Bot(username=account["username"],
                        password=account["password"], headless=False)

        for i in range(50):
            if not usernames:
                break

            username = usernames.pop()
            insta.sendMessage(user=username, message=random.choice(messages))
            with open('infos/users_sended.txt', 'a') as users_sended:
                users_sended.write(f"{username}\n")
            insta.__random_sleep__(20, 40)
        clean_usernames()

        insta.teardown()