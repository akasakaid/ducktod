import os
import re
import sys
import json
import time
import random
import requests
from colorama import *
from pathlib import Path
from glob import glob
from urllib.parse import unquote
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import RequestWebViewRequest
from telethon.errors import SessionPasswordNeededError
from bs4 import BeautifulSoup as bs

init(autoreset=True)

merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
putih = Fore.LIGHTWHITE_EX


class GeMod:
    def __init__(self):
        self.xiaomi_page_list = [
            "https://www.gsmarena.com/xiaomi-phones-80.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p2.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p3.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p4.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p5.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p6.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p7.php",
            "https://www.gsmarena.com/xiaomi-phones-f-80-0-p8.php",
        ]
        self.sdk_level_api = {
            "15": "SDK 35",
            "14": "SDK 34",
            "13": "SDK 33",
            "12": "SDK 32",
            "11": "SDK 30",
            "10": "SDK 29",
            "9": "SDK 28",
            "8": "SDK 27",
            "7": "SDK 25",
            "6": "SDK 23",
            "5": "SDK 22",
            "4": "SDK 20",
        }

    def scrape_phone(self, url: str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        }
        res = requests.get(url, headers=headers)
        parser = bs(res.text, "html.parser")
        device_name = parser.find("h1", attrs={"data-spec": "modelname"}).text
        os = parser.find("td", attrs={"data-spec": "os"})
        # print(os)
        if os is None:
            return False
        try:
            _os = re.search(r"\d+", os.text.split(",")[0]).group()
            os = self.sdk_level_api[_os]
            return device_name, os
        except AttributeError:
            return False

    def generate_model(self):
        while True:
            xiaomi_page = random.choice(self.xiaomi_page_list)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            }
            res = requests.get(xiaomi_page, headers=headers)
            parser = bs(res.text, "html.parser")
            makers = parser.find("div", attrs={"class": "makers"})
            list_device = makers.find_all("li")
            choice_device = random.choice(list_device)
            device_url = "https://gsmarena.com/" + choice_device.find("a").get("href")
            res = self.scrape_phone(device_url)
            if res is False:
                continue
            return res


class Config:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash


class BebekTod:
    def __init__(self):
        self.cookie = None
        self.peer = "FirstDuck_bot"
        self.DEFAULT_APIID = 6
        self.DEFAULT_APIHASH = 'eb06d4abfb49dc3eeb1aeb98ae0f581e'
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "https://tgames-duck.bcsocial.net",
            "x-requested-with": "org.telegram.messenger",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://tgames-duck.bcsocial.net/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-US;q=0.9",
        }

    def telegram_login(self, phone, config: Config, return_data=False):
        gemod = GeMod()
        session_path = "session"
        if not os.path.exists(session_path):
            os.makedirs(session_path)
        model, system_version = gemod.generate_model()
        client = TelegramClient(
            f"{session_path}/{phone}",
            api_id=config.api_id,
            api_hash=config.api_hash,
            device_model=model,
            app_version="10.12.0 (4710)",
            system_lang_code="en-US",
            system_version=system_version,
            lang_code="us",
        )
        client.connect()
        if not client.is_user_authorized():
            try:
                res = client.send_code_request(phone)
                code = input("input login code : ")
                client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password_2fa = input("input password 2fa : ")
                client.sign_in(password=password_2fa)

        me = client.get_me()
        first_name = me.first_name
        last_name = me.last_name
        if return_data is False:
            self.log(f"{hijau}login as {putih}{first_name} {last_name}")
        res = None
        if return_data:
            _res = client(
                RequestWebViewRequest(
                    peer=self.peer,
                    bot=self.peer,
                    from_bot_menu=False,
                    url="https://tgames-duck.bcsocial.net",
                    platform="Android",
                )
            )
            res = _res.url.split("#tgWebAppData=")[1]
        if client.is_connected():
            client.disconnect()
        return res if res is not None else None

    def gen_data_login(self, data_parser):
        data_user = json.loads(data_parser["user"])
        data = {
            "externalId": int(data_user["id"]),
            "firstName": data_user["first_name"],
            "gameId": 3,
            "initData": {
                "auth_date": data_parser["auth_date"],
                "hash": data_parser["hash"],
                "query_id": data_parser["query_id"],
                "user": data_parser["user"],
            },
            "language": "en",
            "lastName": data_user["last_name"],
            "refId": "",
            "username": data_user["username"],
        }
        return data

    def main(self):
        banner = f"""
    {hijau}AUTO TAP-TAP FOR {putih}BEBEKTOD {hijau}/ {putih}FirstDuck_bot
    
    {hijau}By: {putih}t.me/AkasakaID
    {hijau}Github: {putih}@AkasakaID
        """
        while True:
            arg = sys.argv
            if "noclear" not in arg:
                os.system("cls" if os.name == "nt" else "clear")
            print(banner)
            config = json.loads(open("config.json", "r").read())
            cfg = Config(config["api_id"], config["api_hash"])
            if len(cfg.api_id) == 0:
                cfg.api_id = self.DEFAULT_APIID
            if len(cfg.api_hash) == 0:
                cfg.api_hash = self.DEFAULT_APIHASH
            print(
                """
    1. Create Session
    2. Start Bot
                """
            )
            choice = input("input number : ")
            if not choice:
                self.log(f"{merah}you must input number !")
                sys.exit()

            if choice == "1":
                phone = input("input telegram phone number : ")
                self.telegram_login(phone,cfg)
                input("press enter to continue")
                continue

            if choice == "2":
                while True:
                    list_countdown = []

                    sessions = glob("session/*.session")
                    if len(sessions) <= 0:
                        self.log(f"{kuning}0 account detected !")
                        self.log(
                            f"{kuning}add account first or copy your available session to session folder"
                        )
                        sys.exit()
                    total_account = len(sessions)
                    self.log(f'{hijau}account detected : {total_account} ')
                    start = int(time.time())
                    for no, session in enumerate(sessions):
                        self.cookie = None
                        print("~" * 50)
                        self.log(f"{hijau}account number : {putih}{no + 1}")
                        data_telegram = self.telegram_login(
                            phone=Path(session).stem, config=cfg, return_data=True
                        )
                        res_parser = self.data_parsing(data_telegram)
                        data_login = self.gen_data_login(res_parser)
                        res_login = self.login(data_login)
                        res_me = self.get_me()
                        while True:
                            res_claim = self.claim()
                            if res_claim is False:
                                break

                            res_me = self.get_me()
                            if res_claim is False:
                                break
                            if res_me > 30:
                                list_countdown.append(res_me)
                                break

                            self.countdown(res_me)
                    end = int(time.time())
                    if len(list_countdown) > 1:
                        min_countdown = min(list_countdown)
                        total = (end - start) - min_countdown
                        if total <= 0:
                            continue

                        self.countdown(min_countdown)
                        continue

                    self.countdown(list_countdown[0])

    def get_me(self):
        url = "https://tgames-duck.bcsocial.net/panel/users/getUser"
        headers = self.base_headers.copy()
        headers["cookie"] = self.cookie
        data = json.dumps({})
        headers["content-length"] = str(len(data))
        res = self.http(url, headers, data)
        if "please login" in res.text:
            return False

        balance = res.json()["data"]["balance"]
        next_claim = res.json()["data"]["nextClaimTime"]
        level = res.json()["data"]["level"]
        self.log(
            f"{putih}level : {hijau}{level} {biru}| {putih}balance : {hijau}{balance}"
        )
        if next_claim != 0:
            if next_claim > 30:
                return next_claim
            return random.randint(20, 30)

        return random.randint(20, 30)

    def claim(self):
        url = "https://tgames-duck.bcsocial.net/panel/games/claim"
        amount = random.randint(60, 80)
        data = json.dumps(
            {
                "amount": amount,
            }
        )
        headers = self.base_headers.copy()
        headers["cookie"] = self.cookie
        headers["content-length"] = str(len(data))
        res = self.http(url, headers, data)
        if "please login" in res.text:
            return False

        return True

    def bypas_captcha(self, data_captcha):
        captcha = data_captcha.replace("=", "")
        result = eval(captcha)
        url = "https://tgames-duck.bcsocial.net/panel/users/verifyCapcha"
        headers = self.base_headers.copy()
        headers["cookie"] = self.cookie
        data = json.dumps(
            {
                "code": result,
            }
        )
        headers["content-length"] = str(len(data))
        res = self.http(url, headers, data)
        if "ok" in res.text:
            self.log(f"{hijau}success bypass captcha !")

    def login(self, data):
        url = "https://tgames-duck.bcsocial.net/panel/users/login"
        _headers = self.base_headers.copy()
        data = json.dumps(data, separators=(",", ":"))
        res = self.http(url, _headers, data)
        if "Please try again later" in res.text:
            self.log(f"{kuning}need the latest data to log in,")
            self.log(
                f"{kuning}please retrieve the latest data and update the data file"
            )
            sys.exit()

        string_cookie = ""
        for cookie in res.cookies.get_dict().items():
            key, value = cookie
            string_cookie += f"{key}={value}; "

        self.cookie = string_cookie
        balance = res.json()["data"]["balance"]
        next_claim = res.json()["data"]["nextClaimTime"]
        first_name = res.json()["data"]["firstName"]
        last_name = res.json()["data"]["lastName"]
        level = res.json()["data"]["level"]
        self.log(f"{hijau}login as : {putih}{first_name} {last_name}")
        if "capcha" in res.json()["data"].keys():
            if res.json()["data"]["capcha"] != "":
                self.log(f"{kuning}captcha detected")
                self.bypas_captcha(res.json()["data"]["capcha"])

    def log(self, message):
        year, mon, day, hour, minute, second, a, b, c = time.localtime()
        mon = str(mon).zfill(2)
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)
        print(f"{hitam}[{year}-{mon}-{day} {hour}:{minute}:{second}] {message}")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def data_parsing(self, data):
        res = unquote(data)
        data = {}
        for i in res.split("&"):
            j = unquote(i)
            y, z = j.split("=")
            data[y] = z

        return data

    def http(self, url: str, headers: dict, data=None):
        while True:
            try:
                if data is None:
                    headers["Content-Length"] = "0"
                    res = requests.get(url, headers=headers)
                    open(".http_request.log", "a").write(res.text + "\n")
                    return res

                headers["Content-Length"] = str(len(json.dumps(data)))
                res = requests.post(url, headers=headers, data=data)
                open(".http_request.log", "a").write(res.text + "\n")
                return res
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
            ):
                self.log(f"{merah}connection error / connection timeout !")
                continue


if __name__ == "__main__":
    try:
        app = BebekTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
