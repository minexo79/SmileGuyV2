import discord
from discord import Embed
from discord.ext import commands

import random as ra
import requests
import time,asyncio,re

from datahook import yamlhook

class shrimp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # load yaml
        data = (yamlhook("database.yaml").load())

        print("-----------------------")
        print("Check Database ...")
        if (data == None) or ('shrimp' not in list(data.keys())) or (type(data['shrimp']) is not dict):
            # initialize data
            print("Found new Database! initializing...")
            data['shrimp'] = {}

        self.data = data['shrimp']

        self.dump_yaml = yamlhook("database.yaml").Operate
        # check if shrimp exists
        async def shrimp_check():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                # check shrimp is full or not
                if (self.data != None):
                    for i in list(self.data.keys()):
                        self.data[i]['shrimpcount'] = int(self.data[i]['counter'] * 0.8) + 40
                        self.data[i]['counter'] = 0
                self.dump_yaml(setting=self.data,dictTopic='shrimp')
                await asyncio.sleep(7200) # 2h

        self._shrimp_check = self.bot.loop.create_task(shrimp_check())

    def shrimpEmbed(self,ctx:commands.Context,x:str):
        embed = Embed(title="釣蝦系統",description=x,color=self.bot.default_colour)
        embed.set_footer(text=f"{ctx.author}",icon_url=ctx.author.avatar_url)
        return embed


    @commands.group(name="shrimp",help="釣蝦場")
    async def shrimp(self,ctx:commands.Context):
        pass

    @shrimp.command(name="register",help="註冊釣蝦功能")
    async def register(self,ctx:commands.Context):
        guild_id = str(ctx.guild.id)
        if guild_id not in list(self.data.keys()):
            # create server data
            self.data[guild_id] = {
                'user': [],
                'shrimpcount': ra.randint(30,50),
                'counter': 0
            }
            # self.data[guild_id]['user'] = []
            # self.data[guild_id]['shrimpcount'] = ra.randint(30,50)
            # self.data[guild_id]['counter'] = 0
        author_id = str(ctx.author.id)
        for i in self.data[guild_id]['user']:
            if(author_id in i.keys()):
                await ctx.send(embed=self.shrimpEmbed(ctx,"你已經註冊囉!!"))
                return
        # couldn't find author profile
        self.data[guild_id]['user'].append({author_id : 0})
        self.dump_yaml(setting = self.data,dictTopic='shrimp')
        await ctx.send(embed = self.shrimpEmbed(ctx,"註冊成功!!"))

    @shrimp.command(name="level",help="查詢等級")
    async def level(self,ctx:commands.Context):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if (guild_id in list(self.data.keys())):
            for i in self.data[guild_id]['user']:
                if(author_id in i.keys()):
                    await ctx.send(embed = self.shrimpEmbed(ctx,
                    f"玩家：{ctx.author.mention} \n \
                    你的等級為: `{int(i[author_id]/25)} ({i[author_id]})`"))
                    return
            # couldn't find author profile
            await ctx.send(embed=self.shrimpEmbed(ctx,"你尚未註冊喔!!"))
        else:         
            await ctx.send(embed=self.shrimpEmbed(ctx,"你尚未註冊喔!!"))

    @shrimp.command(name="exist",help="查詢蝦池內的蝦子數量")
    async def exist(self,ctx:commands.Context):
        guild_id = str(ctx.guild.id)
        if (guild_id in list(self.data.keys())):
            shrimps = self.data[guild_id]["shrimpcount"]
            counter = self.data[guild_id]["counter"]
            embed = self.shrimpEmbed(ctx,f"目前蝦池有`{shrimps}`隻蝦子。\n最近有`{counter}`人曾經嘗試釣蝦過。")
            await ctx.send(embed = embed)
        else:         
            await ctx.send(embed = self.shrimpEmbed(ctx,"你尚未註冊喔!!"))

    @commands.cooldown(5,60,commands.BucketType.guild)
    @shrimp.command(name="play",help="開釣!!!")
    async def play(self,ctx:commands.Context):
        author_id = str(ctx.author.id)
        # get author id
        guild_id = str(ctx.guild.id)
        # get guild id
        if str(guild_id) in list(self.data.keys()):
            for i in self.data[guild_id]['user']: 
                # find to avoid same user repeat
                if(author_id in i.keys()):
                    fisherfile = discord.File("img//fish.gif", filename="fish.gif")
                    fishingEmbed = self.shrimpEmbed(ctx,f"{ctx.author.mention}拋下釣竿，\n坐在椅子上靜靜等待蝦子的到來。")
                    fishingEmbed.set_thumbnail(url="attachment://fish.gif")
                    waiting_msg = await ctx.send(file = fisherfile, embed = fishingEmbed)
                    ra.seed(None)
                    k = ra.randint(1,5) # get shrimp or not
                    w = ra.randint(1,6) # shrimp level
                    await asyncio.sleep(60)
                    await waiting_msg.delete()
                    if (self.data[guild_id]["shrimpcount"] > 0):
                        if (k > 3):
                            if (w <= 3):
                                i[str(author_id)] += 0.5
                            else:
                                i[str(author_id)] += 1
                            shrimpfile = discord.File(f"img//shrimp//{w}.png", filename=f"{w}.png")
                            if (w <= 3):
                                # little shrimp
                                resultEmbed = self.shrimpEmbed(ctx,f"{ctx.author.mention}\n你釣到了...**小蝦蝦!!!**")
                                resultEmbed.add_field(name=None,value="經驗值加`0.5`!",inline=True)
                            else:
                                # special shrimp
                                resultEmbed = self.shrimpEmbed(ctx,f"{ctx.author.mention}\n你釣到了...**大蝦蝦!!!**")
                                resultEmbed.add_field(name=None,value="經驗值加`1`!",inline=True)
                            # shrimp image
                            resultEmbed.set_thumbnail(url=f"attachment://{w}.png")
                            await ctx.send(file = shrimpfile, embed = resultEmbed)
                            self.data[guild_id]["shrimpcount"] -= 1
                        else:
                            resultEmbed = self.shrimpEmbed(ctx,"什麼都沒有釣到...")
                            await ctx.send(embed = resultEmbed)
                        # add counter into database
                        self.data[guild_id]["counter"] += 1
                        self.dump_yaml(setting=self.data,dictTopic='shrimp')
                    else:
                        # no shrimp in pool
                        noShrimpEmbed = self.shrimpEmbed(ctx,"釣蝦場內沒有蝦子了...\n等待下一次捕貨吧！")
                        await ctx.send(embed = noShrimpEmbed)                       
                    return
            # couldn't find author profile
            await ctx.send(embed = self.shrimpEmbed(ctx,"你尚未註冊喔!!"))
        else:         
            await ctx.send(embed = self.shrimpEmbed(ctx,"你尚未註冊喔!!"))

    @play.error
    async def on_command_error(self,ctx:commands.Context,error:commands.errors):
        if isinstance(error,commands.CommandOnCooldown):
            overRodEmbed = self.shrimpEmbed(ctx,"釣蝦場只能容得下五根釣竿，\n請等待蝦子上鉤之後再拋下釣竿吧!!")
            await ctx.send(embed = overRodEmbed)

def setup(bot):
    bot.add_cog(shrimp(bot))