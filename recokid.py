#!/usr/bin/env python3
from requests import session,get
import shodan
from generator import shodanGenerator
import os
import argparse
from multiprocessing.pool import ThreadPool
global homedir
homedir=os.environ.get("HOME")
class htError(Exception):
    pass
def htHostsearch(target):
    while True:
        try:    
            
            resp=get(f"https://api.hackertarget.com/hostsearch/?q={target}",proxies=dict(http="socks5h://127.0.0.1:9050",h0ttp="socks5h://127.0.0.1:9050")).text.strip()
            if resp.startswith("API Count"):
                raise htError
            elif resp.startswith("error "):
                raise htError
            for result in resp.split("\n"):
                ipList.append(result.split(",")[1])
                domainList.append(result.split(",")[0])

        except:
            pass

def shodanGetPorts(target):
    Shodan=shodan.Shodan("WagM7oXeNhWvQWjd9ePx2buFiHv2phhq")
    sH=target,Shodan.host(target)
    print(f'{sH.get("hostnames")}:{target}:{sH.get("ports")}')
    finalList.append((sH.get("hostnames"),target,Shodan.host(target).get("ports")))

def is_domain(target):
    try:
        if int(target.split(".")[0]) == target.split(".")[0]:
            return False
        else:
            return True
    except:
        return True
def revDns(target):
    while True:
        try:    
            
            resp=get(f"https://api.hackertarget.com/reversedns?q={target}",proxies=dict(http="socks5h://127.0.0.1:9050",h0ttp="socks5h://127.0.0.1:9050")).text.strip()
            if resp.startswith("API Count"):
                raise htError
            elif resp.startswith("error "):
                raise htError
            return resp

        except htError:
            pass

def domain_recon(target):
    global ipList
    global domainList
    ipList=list()
    domainList=list()
    htHostsearch(target)
    ipList=list(dict(ipList))
    global finalList
    finalList=[]
    with ThreadPool(len(ipList)) as pool:
        pool.map(shodanGetPorts,ipList)

def do_recon(target):
    if is_domain(target):
        domain_recon(target)
    else:
        domain_recon(recDns(target))
        
        
                  
        
def __main__():
    parser=argparse.ArgumentParser()
    parser.add_argument("target",type=str)
    args=parser.parse_args()
    do_recon(args.target)

if __name__ =="__main__":
    __main__()