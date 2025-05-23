# Bot Instagram DM

Bot instagram qui envoie un message à un ou plusieurs utilisateurs

## Installation
1. Git clone le repo avec cette commande --> `git clone https://github.com/Jeremie-pires/insta_bot.git`
2. Installer les dépendances avec cette commande --> `pip install -r requirements.txt`

## Utilisation du scrapper
1. Aller dans le dossier infos et mettre les logs du compte dans accounts.json, les cibles dans targets.txt
2. Lancer avec cette commande --> `python export_followers.py`
3. Pour supprimer les doublons lancer cette commande --> `python clean_usernames.py`

## Utilisation du bot dm
1. Aller dans le dossier infos et mettre le/les message.s à envoyer dans messages.txt et ajouter des comptes si besoin dans accounts.json
2. Lancer avec cette commande --> `python run.py`


