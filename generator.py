#!/usr/bin/python3
from multiprocessing.pool import ThreadPool

#from bs4 import BeautifulSoup as suppe
from time import sleep
import requests
import re
import json
import names #
import random
from random_user_agent.user_agent import UserAgent
import argparse
from os import path,environ

global userAgent
userAgent=UserAgent().get_random_user_agent()

class torException(Exception()):
    "raised if mailer cant connect through tor"
    pass
class mailer:
    def __init__(self):
        self.session = requests.session()
        self.session.proxies=dict(http="socks5h://127.0.0.1:9050",https="socks5h://127.0.0.1:9050")
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": userAgent
        }
        #self.session.proxies=dict(http="socks5h://127.0.0.1:9050",https="socks5h://127.0.0.1:9050")
        #torTestSuppe=suppe(self.session.get("https://check.torproject.org/").text,features="lxml")
       # print("Testing Mailers Tor Connection")
       
    def create(self, minLen=8, maxLen=32):
        self.session.get("https://temp-mail.io/en")
        #domains = json.loads(self.session.get("https://api.internal.temp-mail.io/api/v2/domains").text)['domains']
        #print("Current Domains are " + domains)
        data = {
            "min_name_length": str(minLen),
            "max_name_length": str(maxLen)
        }
        self.email = json.loads(self.session.post(
            "https://api.internal.temp-mail.io/api/v2/email/new", data=data).text)["email"]
        return self.email

    def readMessages(self):
        return requests.get("https://api.internal.temp-mail.io/api/v2/email/" + self.email + "/messages").content.decode("utf-8")

class shodanGenerator:
    def createAccount(self, user, passwd="123456789"):
        self.user = user
        self.passwd = passwd
        self.mail.create()
        while True:
            try:
                sleep(random.randint(0,6))
                page = self.session.get("https://account.shodan.io/register")
                token = re.search(r'csrf_token.*="(\w*)"',
                            page.content.decode("utf-8")).group(1)
                            
                data = {
                    "username": user,
                    "password": passwd,
                    "password_confirm": passwd,
                    "email": self.mail.email,
                    "csrf_token": token
                }
                response = self.session.post(
                    "https://account.shodan.io/register", data=data).text
                if response.find("Please check the form and fix any errors") == -1:
                    self.session.get("https://account.shodan.io/")
                    return self.mail.email
                return None
            except:
                sleep(random.randint(0,120))
                pass

    def activateAccount(self):
        # print(self.mail.readMessages())
        retries = 15
        retry = 0
        while retry < retries:
            try:
                activation = re.search(
                    r'(https://account.shodan.io/activate/\w*)', self.mail.readMessages()).group(1)
            except KeyboardInterrupt:
                return None
            except:
                retry = retry + 1
                sleep(0.666)
                continue
            else:
                break
        if retry == retries:
            return None
        self.session.get(activation)
    def fetch_key(self):
        sleep(random.randint(0,15))
        while True:
            try:
                        
                    
                token = re.search(r'csrf_token.*="(\w*)"', self.session.get(
                    "https://account.shodan.io/login").text).group(1)
                data = {
                    "username": self.user,
                    "password": self.passwd,
                    "grant_type": "password",
                    "continue": "https://account.shodan.io/",
                    "csrf_token": token,
                    "login_submit": "Login",
                }
                self.session.post("https://account.shodan.io/login",
                                data=data).content.decode('utf-8')
                res = self.session.get("https://account.shodan.io/").text
                
        #        resuppe=suppe(res,features="lxml")
                #resuppe.findAll("td").text.split("<")[0]
                self.api = re.search(r'<td>(\w*)<br /><br />', res).group(1)
                break
            except:
                sleepTime=random.randint(0,120)
                sleep(sleepTime)
                pass

    def __init__(self):
        self.mail = mailer()
        self.session = requests.session()
        self.session.headers = {
            "origin": "https://account.shodan.io",
            "referer": "https://account.shodan.io/register",
            "user-agent": userAgent,
        }
        #self.session.proxies=self.getProxy()
        self.createAccount(f'{names.get_full_name().lower().replace(" ","-")}{random.randint(-690000,7500000)}')
        self.activateAccount()
        self.fetch_key()
    def return_creds(self):
        return f'{self.user}:{self.passwd}'
    def return_api_key(self):
        return str(self.api)


def threadedGenerator(l):
    acc=shodanGenerator()
    home=environ.get("HOME")
    with open(path.join(home,"shodan_credentials.txt"),"a") as creds_file:creds_file.write(f'{acc.return_creds()}\n') 
    with open(path.join(home,"shodan_api-keys.txt"),"a") as key_file:key_file.write(f'{acc.return_api_key()}\n')
    print(acc.return_api_key())
    

def __main__():
    parser = argparse.ArgumentParser()
    #parser.add_argument("-c","--creds",help="Display credentials",type=bool,default=False)
    parser.add_argument("accounts", help="Number of Accounts to Generate. Default May take about half an hour.",type=int,default=5)
    args = parser.parse_args()
    l=[""]*args.accounts
    threads=[]
    with ThreadPool(args.accounts) as pool:
        pool.map(threadedGenerator,l)
  


if __name__ == "__main__":
    __main__()
