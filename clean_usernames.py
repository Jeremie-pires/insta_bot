with open("infos/usernames.txt", "r", encoding="utf-8") as f:
    usernames = set(line.strip() for line in f if line.strip())

with open("infos/users_sended.txt", "r", encoding="utf-8") as f:
    users_sended = set(line.strip() for line in f if line.strip())

cleaned_usernames = sorted(usernames - users_sended)

with open("infos/usernames.txt", "w", encoding="utf-8") as f:
    for user in cleaned_usernames:
        f.write(user + "\n")

print(f"{len(cleaned_usernames)} utilisateurs uniques conservés (hors déjà envoyés).")