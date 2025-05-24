print("Lancement du bot")

#Libraries
import json
from random import randint, uniform
import logging
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time

DEFAULT_IMPLICIT_WAIT = 1


#Define de la classe Bot
class Bot(object):
    def __init__(self, username, password, headless=True, workspace=None, profile_dir=None):
        #Selecteurs de la page instagram
        self.selectors = {
            "accept_cookies": "//button[text()='Autoriser toutes les cookies']",
            "deny_cookies": "//button[text()='Refuser les cookies optionnels']",
            "login_button": "//button[@type='submit']",
            "notifs": "//button[text()='Plus tard']",
            "open_search": "//div[text()='Envoyer un message']",
            "search_user": "//input[@placeholder='Recherchez...']",
            "next_button": '//div[@role="button" and text()="Discuter"]',
            "textarea": "//div[@role='textbox']",
            "send": '//div[@role="button" and text()="Send"]'
        }

        #Options selenium
        options = webdriver.ChromeOptions()

        if profile_dir:
            options.add_argument("user-data-dir=profiles/" + profile_dir)

        if headless:
            options.add_argument("--headless")

        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        #Initialisation de la base de données
        self.workspace = workspace
        self.conn = None
        self.cursor = None
        if self.workspace is not None:
            self.conn = sqlite3.connect(
                self.workspace + "Insta_bot/db/instapy.db")
            self.cursor = self.conn.cursor()

            cursor = self.conn.execute("""
                SELECT count(*)
                FROM sqlite_master
                WHERE type='table'
                AND name='message';
            """)
            count = cursor.fetchone()[0]

            if count == 0:
                self.conn.execute("""
                    CREATE TABLE "message" (
                        "username"    TEXT NOT NULL UNIQUE,
                        "message"    TEXT DEFAULT NULL,
                        "sent_message_at"    TIMESTAMP
                    );
                """)

        try:
            self.login(username, password)
        except Exception as e:
            logging.error(e)
            print(str(e))

    #Connexion à Instagram
    def login(self, username, password):
        self.driver.get('https://www.instagram.com')
        self.__random_sleep__(3,5)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(By.XPATH, self.selectors["deny_cookies"])
            ).click()
            self.__random_sleep__(3,5)
        except Exception:
            pass
            
        logging.info(f'Login with {username}')
        WebDriverWait(self.driver, 5).until(
            lambda d: d.find_element(By.NAME, 'username')
        ).send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, self.selectors["login_button"]).click()
        self.__random_sleep__(3,5)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(By.XPATH, self.selectors["notifs"])
            ).click()
            self.__random_sleep__(3,5)
        except Exception:
            pass

    #Envoi du message
    def typeMessage(self, message):
        self.driver.find_element(By.XPATH, self.selectors['textarea']).send_keys(message)
        self.__random_sleep__(5, 10)
        self.driver.find_element(By.XPATH, self.selectors['send']).click()
        self.__random_sleep__(1, 2)

    #Sélection de la cible
    def sendMessage(self, user, message):
        logging.info(f'Send message to {user}')
        print(f'Send message to {user}')
        self.driver.get('https://www.instagram.com/direct/new/?hl=fr')
        self.__random_sleep__(2, 4)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(By.XPATH, self.selectors["notifs"])
            ).click()
            self.__random_sleep__(3,5)
        except Exception:
            pass

        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(By.XPATH, self.selectors['open_search'])
            ).click()
            self.__random_sleep__(2, 4)
            self.driver.find_element(By.XPATH, self.selectors['search_user']).send_keys(user)
            self.__random_sleep__(1, 2)
        except Exception:
            print(f'Impossible de trouver {user}')

        select_user_xpath = f'//span[text()="{user}"]/ancestor::div[@role="button"]'
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(By.XPATH, select_user_xpath)
            ).click()
            self.__random_sleep__(1, 2)
        except Exception:
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.find_element(By.XPATH, '(//div[@role="dialog"]//div[@role="button"])[2]')
                ).click()
                self.__random_sleep__(1, 2)
            except Exception:
                print(f'Impossible de trouver {user}')
            
        self.driver.find_element(By.XPATH, self.selectors['next_button']).click()
        self.__random_sleep__(1, 2)
        self.typeMessage(message)


    def scrapFollowers(self, target_user):
        logging.info(f'Scrap followers of {target_user}')
        self.driver.get(f"https://www.instagram.com/{target_user}/")
        self.__random_sleep__(2, 4)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers").click()
        self.__random_sleep__(2, 4)
        followers_popup = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        for _ in range(5):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
            self.__random_sleep__(1, 2)
        followers = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//a[contains(@href, '/')]")
        with open("infos/usernames.txt", "a") as f:
            for user in followers:
                username = user.text.strip()
                if username:
                    f.write(username + "\n")



    #Timeout
    def __random_sleep__(self, minimum=1, maximum=60):
        t = randint(minimum, maximum)
        logging.info(f'Wait {t} seconds')
        sleep(t)

    #Fermeture du bot
    def teardown(self):
        self.driver.close()
        self.driver.quit()

