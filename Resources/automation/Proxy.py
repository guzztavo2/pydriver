import zipfile, os

class Proxy:    
    proxies = []
    def __init__(self, ip, port, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
    
    def set_ip(self, ip):
        self.ip = ip
        return self
    
    def set_port(self, port):
        self.port = port
        return self
    
    def set_username(self, username):
        if len(username) > 0:
            self.username = username
        return self
    
    def set_password(self, password):
        if len(password) > 0:
            self.password = password
        return self
        
    def get_ip(self):
        return self.ip
    def get_port(self):
        return self.port
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    
    def get_proxy(self):
        return f"{self.ip}:{self.port}"
    
    def get_extension(self):
        proxy_host = self.get_ip()
        proxy_port = self.get_port()
        proxy_user = self.get_username()
        proxy_pass = self.get_password()
        
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy Authentication",
            "description": "Autenticação automática para proxies HTTP",
            "permissions": [
                "proxy",
                "webRequest",
                "webRequestBlocking",
                "<all_urls>"
            ],
            "background": {
                "scripts": ["background.js"],
                "persistent": true
            }
        }"""

        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy_host}",
                    port: {proxy_port}
                }},
                bypassList: ["localhost"]
            }}
        }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        function authHandler(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }};
        }}

        chrome.webRequest.onAuthRequired.addListener(
            authHandler,
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """

        extension = 'proxy_auth_extension.zip'
        with zipfile.ZipFile(extension, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        
        return os.path.abspath(extension) 
    
    def need_extension(self):
        if self.get_username() is not None and self.get_password():
            return True
        return False