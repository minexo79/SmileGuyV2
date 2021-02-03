import yaml
import pymongo
import random as ra

class yamlhook:

    __slots__ = ['filename']
    def __init__(self,filename):
        self.filename = filename

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

    @property
    def guild_config(self) -> dict:
        return {"_id": "0"}

    def user_config(self, uid: str) -> dict:
        return {"_id": uid}

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

    def search_shrimp_player(self, guild_id, author_id:str = "", p_limit:int = 5) -> dict:
        pym = self.dbconnect()

        shrimp_db = pym['smv2_shrimp']

        shrimp_guild_col = shrimp_db[f'{guild_id}']

        if(author_id == ""):
            x = shrimp_guild_col.find().sort("exp", -1).limit(p_limit)
        else:
            x = shrimp_guild_col.find(self.user_config(author_id))
        
        pym.close()
        if(x.count() == 0):
            return None
        else:
            return x

    def search_shrimp_count(self, guild_id) -> dict:
        pym = self.dbconnect()

        shrimp_db = pym['smv2_shrimp']

        shrimp_guild_col = shrimp_db[f'{guild_id}']

        x = shrimp_guild_col.find(self.guild_config)

        pym.close()
        if(x.count() == 0):
            return None
        else:
            return x

    def update_shrimp_data(self, guild_id, author_id, add_exp: float) -> bool:
        try:
            pym = self.dbconnect()

            shrimp_db = pym['smv2_shrimp']

            shrimp_guild_col = shrimp_db[f'{guild_id}']

            guild_data = shrimp_guild_col.find(self.guild_config)[0]

            if(add_exp > 0):
                after_shrimp = guild_data["shrimpcount"] - 1
            else:
                after_shrimp = guild_data["shrimpcount"]

            shrimp_guild_col.update_one(
                self.guild_config,
                {
                    "$set": {
                        "shrimpcount": after_shrimp,
                        "counter": guild_data['counter'] + 1
                    }
                }
            )

            if(add_exp > 0):
                playerdata = shrimp_guild_col.find(self.user_config(author_id))[0]

                exp = playerdata['exp'] + add_exp
                level = int(exp / 25)

                shrimp_guild_col.update_one(
                    self.user_config(author_id),
                    {
                        "$set": {
                            "exp": exp,
                            "level": level
                        }
                    }
                )
            pym.close()
            return True
        except:
            return False

    def reset_shrimp_count(self):
        pym = self.dbconnect()
        shrimp_db = pym['smv2_shrimp']

        for x in shrimp_db.list_collection_names():
            shrimp_db[x].update_one(
                self.guild_config,
                {
                    "$set": {
                        "shrimpcount": ra.randint(30,50),
                        "counter": 0
                    }
                }
            )

        pym.close()