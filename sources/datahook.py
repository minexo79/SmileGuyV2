import yaml
import pymongo
import random as ra

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
        shrimp_db = pym['smv2_shrimp']
        shrimp_guild_col = shrimp_db[f'{guild_id}']

        x = shrimp_guild_col.find({"_id":"0"})
        if(x.count() == 0):
            firstdict = {
                "_id" : "0",
                "shrimpcount" : ra.randint(30,50),
                "counter": 0
            }
            shrimp_guild_col.insert_one(firstdict)

        mydict = {
            "_id" : author_id,
            "exp" : 0,
            "level": 0
        }
        try:
            shrimp_guild_col.insert_one(mydict)
            return_val = True
        except pymongo.errors.DuplicateKeyError:
            return_val = False
        finally:
            pym.close()
            return return_val

    def search_shrimp_player(self, guild_id, author_id) -> dict:
        pym = self.dbconnect()

        shrimp_db = pym['smv2_shrimp']

        shrimp_guild_col = shrimp_db[f'{guild_id}']

        x = shrimp_guild_col.find({"_id" : author_id})
        
        pym.close()
        if(x.count() == 0):
            return None
        else:
            return x

    def search_shrimp_count(self, guild_id) -> dict:
        pym = self.dbconnect()

        shrimp_db = pym['smv2_shrimp']

        shrimp_guild_col = shrimp_db[f'{guild_id}']

        x = shrimp_guild_col.find({"id": "0"})

        pym.close()
        if(x.count() == 0):
            return None
        else:
            return x

    def update_shrimp_data(self, guild_id, author_id, add_exp: float) -> bool:
        pym = self.dbconnect()

        shrimp_db = pym['smv2_shrimp']

        shrimp_guild_col = shrimp_db[f'{guild_id}']

        guild_data = shrimp_guild_col.find({"id": "0"})[0]

        shrimp_guild_col.update_one(
            {"_id": "0"},
            {
                "shrimpcount": guild_data["shrimpcount"] - 1,
                "counter": guild_data['counter'] - 1
            }
        )

        playerdata = shrimp_guild_col.find({"id": author_id})[0]

        exp = playerdata['exp'] + add_exp
        level = exp / 25

        shrimp_guild_col.update_one(
            {"_id": author_id},
            {
                "exp": exp,
                "level": level
            }
        )

        pym.close()

        