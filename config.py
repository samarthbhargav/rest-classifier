
_conf = {
    "dstore" : "data.tsv",
    "auth" : {
        "username": "abc",
        "password": ""
    }
}



class Config(object):
    
    @property
    def dstore(self):
        return _conf["dstore"]
        
    @property
    def auth_username(self):
        return _conf["auth"]["username"]
    
    @property
    def auth_password(self):
        return _conf["auth"]["password"]

conf = Config()

if __name__ == "__main__":
    print conf.auth_password
    print conf.auth_username
    print conf.dstore
