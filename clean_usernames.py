with open("infos/usernames.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

uniques = sorted(set(line.strip() for line in lines if line.strip()))

with open("infos/usernames.txt", "w", encoding="utf-8") as f:
    for user in uniques:
        f.write(user + "\n")

print(f"{len(uniques)} utilisateurs uniques conservés.")