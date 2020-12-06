import random, discord
from discord.ext import commands
class Ultimate_password():
    def __init__(self,ctx:commands.Context):
        self.password=random.randint(1,100)
        self.low=1
        self.high=100
        self.author=ctx.author
    def userinput(self,number:int):
        if number == self.password :
            return True
        elif number < self.password :
            self.low=number
        elif number > self.password :
            self.high=number
        return False
    def range(self):
        return {"low":self.low,"high":self.high}
    def embed(self,text):
        embed=discord.Embed(title="終極密碼",description=text)
        embed.set_footer(text=str(self.author),icon_url=self.author.avatar_url)
        return embed