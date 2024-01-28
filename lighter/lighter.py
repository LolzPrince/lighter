from google import search
import requests
from colorama import Fore
import argparse
import time
from art import *
import os
from data import get_useragent
import random

text = "lighter"
ascii_art = text2art(text, font="ghost", chr_ignore=True)
logo = f"\033[36m{ascii_art}\033[0m"

FILTERS = [
    "stackoverflow",
    "twitter",
    "github",
    "linkedin",
    "programming",
    "sololearn",
    "facebook",
    "exploit",
    "hack",
    "dork",
    "www.php.net",
    "youtube",
    "rutube",
    "vk",
    "moodle",
    "ubuntu",
    "linux",
    "debian",
    "google",
    "git"
]

filename = "./results/" + time.strftime("%Y-%m-%d %H-%M") + ".txt"
proxyes = []

def check_proxy(proxy):
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def validate_url(url: str) -> bool:
    for stop_word in FILTERS:
        if stop_word in url:
            return False
    return True


def get_urls(dork: str, sleep_interval: int = 1, count=20, lang="en", user_agent: bool = False, proxy: str = None) -> list[str]:
    urls = []
    try:
        urls = search(dork, sleep_interval=sleep_interval, num_results=count, lang=lang, user_agent=user_agent, proxy=proxy)
    except Exception as error:
        print(f"{Fore.RED}Ошибка получения ссылок для дорка: {dork}. ERROR: [{error}]\033[0m")
    return urls


def check_sql(url: str,  id: int, user_agent: bool = False, timeout: int = 2, write_result: bool = False) -> None:
    if user_agent:
        user_agent = headers = {
            "User-Agent": get_useragent()
        }
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        }
    try:
        time.sleep(1)
        testing_page = requests.get(url=url + "'", timeout=timeout, headers=user_agent)
        if 'SQL' in testing_page.text or 'sql' in testing_page.text or testing_page.text == "":
            print(f"{id}) {url} {Fore.GREEN} [SQL INJECTION]\033[0m")
            if write_result:
                file = open(filename, 'a', encoding='utf-8')
                file.write(url + "\n")
                file.close()
        else:
            print(f"{id}) {url} {Fore.BLUE} [NO SQL]\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"{id}) {url} {Fore.YELLOW}[TIMEOUT]\033[0m")
    except requests.exceptions.RequestException as error_requests:
        print(f"{id}) {url} {Fore.RED}[ERROR]\033[0m")
        print(f"{Fore.RED}{error_requests.args[0]}\033[0m")


def testing(path: str, user_agent: bool, sleep_interval: int, timeout: int, count: int, lang: str, write_result: bool, proxy: str = None) -> None:
    id = 1
    if not proxy is None:
        print("Start checking your proxy...")
        with open(proxy, "r", encoding="utf-8") as proxyes_file:
            for proxy_item in proxyes_file:
                proxy_item = proxy_item.replace("\n", "")
                if check_proxy(proxy_item):
                    proxyes.append(proxy_item)
                    print(f"{proxy_item} {Fore.GREEN}[GOOD]\033[0m")
                else:
                    print(f"{proxy_item} {Fore.RED}[BAD]\033[0m")
        print("finish checking proxy")
        print(f"GOOD: [{len(proxyes)}]")

    if write_result:
        file = open(filename, 'w', encoding='utf-8')
        file.close()
    with open(path, "r", encoding="utf-8") as file_dorks:
        for dork in file_dorks:
            try:
                time.sleep(2)
                test_proxy = None
                if len(proxyes) > 0:
                    test_proxy = random.choice(proxyes)
                urls = get_urls(dork=dork, sleep_interval=sleep_interval, count=count, lang=lang, user_agent=user_agent, proxy=test_proxy)
                for url in urls:
                    if validate_url(url):
                        check_sql(url=url, id=id, user_agent=user_agent, timeout=timeout, write_result=write_result)
                    else:
                        print(f"{id}) {url} {Fore.YELLOW}[NO VALID]\033[0m")
                    id += 1
                if len(proxyes) > 0:
                    if not check_proxy(test_proxy):
                        proxyes.remove(test_proxy)
            except Exception as error:
                 print(f"{Fore.RED}{error}\033[0m")


if __name__ == '__main__':
    print(logo)
    if not os.path.exists("./results/"):
        os.mkdir("./results/")
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file with dorks.")
    parser.add_argument("-r", "--random-agent", action='store_true', help="Use this flag to enable random user-agent.")
    parser.add_argument("-s", "--sleep-interval", default=1, type=int, help="Specify here an integer parameter for the time interval between requests to dorks.")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="Specify here an integer parameter for the time interval between requests to pages.")
    parser.add_argument("-c", "--count", type=int, default=20, help="Specify here an integer parameter for the number of links received in one request to dork. Default: 20.")
    parser.add_argument("-l", "--lang", default="en", help="Select a language to search for Dorks. Example: en. Default: en")
    parser.add_argument("-w", "--write-result", action='store_true', help="Use this flag to write successful url to a file.")
    parser.add_argument("-p", "--proxy-list", default=None, help="Path to the file with proxy[http, https].")
    args = parser.parse_args()
    testing(args.path, args.random_agent, args.sleep_interval, args.timeout, args.count, args.lang, args.write_result, args.proxy_list)