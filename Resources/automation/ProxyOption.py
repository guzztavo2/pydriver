import random
from Resources.automation.Proxy import Proxy

class ProxyOption:    
    proxies = []
    
    @classmethod
    def add_proxy(cls, ip, port, username=None, password=None):
        proxy = Proxy(ip, port, username, password)
        cls.proxies.append(proxy)
        return cls
    
    @staticmethod
    def array_to_proxies(ips = [], ports = [], usernames = [], passwords = []):
        haveUserNames = True
        if len(usernames) > 0 and len(passwords) > 0:
            if len(ips) != len(ports) or len(ips) != len(usernames) or len(ips) != len(passwords):
                raise ValueError("All proxyes lists must have the same length")
        else:
            haveUserNames = False
            if len(ips) != len(ports):
                raise ValueError("All proxyes lists must have the same length")
            
        for i in range(len(ips)):
            if haveUserNames:
                ProxyOption.add_proxy(ips[i], ports[i], usernames[i], passwords[i])
            else: 
                ProxyOption.add_proxy(ips[i], ports[i])
        return ProxyOption

    @classmethod
    def prepare_random_proxy(cls):
        if len(cls.proxies) == 0:
            return False
        return cls.proxies[random.randint(0, len(cls.proxies) - 1)]
    
    @classmethod
    def get_proxy(cls):
        proxy = cls.prepare_random_proxy()
        if proxy is False:
            return False
        
        return proxy