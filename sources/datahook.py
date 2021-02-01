import yaml
import pymongo

class yamlhook:
    __slots__ = ['filename']
    def __init__(self,filename):
        self.filename = filename

    # load : 純讀取

    def load(self):    
        with open(self.filename,'r',encoding="utf8") as yd:
            return yaml.safe_load(yd)

    
    def Operate(self,dictTopic:str,setting):
        with open(self.filename,'r',encoding="utf8") as yd:
            data = yaml.safe_load(yd)

        data[dictTopic] = setting

        with open(self.filename,'w',encoding="utf8") as yd:
            yaml.safe_dump(data,yd)

class mongohook:
    __slots__ = ['address', 'user', 'password']
    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password

    def dbconnect(self):
        pym = pymongo.MongoClient(f"mongodb+srv://{self.user}:{self.password}@{self.address}/?retryWrites=true&w=majority")
        return pym

    def add_shrimp_player(self, guild_id, author_id) -> bool:
        pym = self.dbconnect()

        fish_db = pym['xobot_fish']

        fish_guild_col = fish_db[f'{guild_id}']

        mydict = {
            "_id" : author_id,
            "exp" : 0,
            "level": 0
        }
        try:
            fish_guild_col.insert_one(mydict)
            return_val = True
        except pymongo.errors.DuplicateKeyError:
            return_val = False
        finally:
            pym.close()
            return return_val

    def search_shrimp_player(self, guild_id, author_id) -> dict:
        pym = self.dbconnect()

        fish_db = pym['xobot_fish']

        fish_guild_col = fish_db[f'{guild_id}']

        x = fish_guild_col.find({}, {"_id" : author_id})
        if(len(x) == 0):
            return None
        else:
            return x