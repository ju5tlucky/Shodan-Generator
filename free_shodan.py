#!/usr/bin/env python3
from shodan.client import Shodan as classicShodan
from shodan.client import *
from generator import shodanGenerator
import requests
from os import path,environ
class newShodan(classicShodan):
    
    #def __init_api_key(self):
        
    
    def __init__(self, proxies=None):
        
        """Initializes the API object.
        :param key: The Shodan API key.(Automatically Generated ;)
        :type key: str
        :param proxies: A proxies array for the requests library, e.g. {'https': 'your proxy'}
        :type proxies: dict
        """
        # Check if $HOME/shodan_api-keys.txt exists
        
        if path.exists(path.join(environ.get("HOME"),"shodan_api-keys.txt")):
            with open(path.join(environ.get("HOME"),"shodan_api-keys.txt"),"r") as keyfile:
                self.api_key_array=keyfile.read().split("\n")
        else:
            pass
        self.api_array_iterator=0
        if len(self.api_key_array) > 0:
            self.api_key=self.api_key_array[self.api_array_iterator]
        else:
            
            self.api_key = shodanGenerator().return_api_key()
        self.base_url = 'https://api.shodan.io'
        self.base_exploits_url = 'https://exploits.shodan.io'
        self.data = self.Data(self)
        self.dns = self.Dns(self)
        self.exploits = self.Exploits(self)
        self.labs = self.Labs(self)
        self.notifier = self.Notifier(self)
        self.org = self.Organization(self)
        self.tools = self.Tools(self)
        self.stream = Stream(key, proxies=proxies)
        self._session = requests.Session()
        self.api_rate_limit = 12  # Requests per second
        self._api_query_time = None
        if proxies:
            self._session.proxies.update(proxies)
            self._session.trust_env = False
        

    

s=newShodan()
s.host(requests.get("https://api.ipify.me").text)