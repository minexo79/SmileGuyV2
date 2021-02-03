import discord
from discord import Embed
from discord.ext import commands

import random as ra
import requests
import time,asyncio,re

from SmileGuyV2.sources.datahook import yamlhook, mongohook

class shrimp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        # load yaml
        mongo_config = yamlhook("config.yaml").load()['mongo']
        # data = yamlhook("database.yaml").load()
        self.mongodata = mongohook(address = mongo_config['address'], user = mongo_config['username'], password = mongo_config['password'])

        print("-----------------------")
        print("Try to connect with mongoDB...", end='')

        pym_test = self.mongodata.dbconnect()
        if(pym_test != None):
            print(f"OK!!\nMongoDB version: {pym_test.server_info()['version']}")
            pym_test.close()
        else:
            print("Failed!!")
            self.bot.sm_print(3, f"Could't connect to MongoDB!! check your setting if it's correct!!")

        # check if shrimp exists
        async def shrimp_check():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                # reset any guild shrimp count
                self.mongodata.reset_shrimp_count()
                await asyncio.sleep(120) # 2h

        self._shrimp_check = self.bot.loop.create_task(shrimp_check())

    def shrimpEmbed(self,ctx:commands.Context,x:str):
        embed = Embed(title="釣蝦系統",description=x,color=self.bot.default_colour)
        embed.set_footer(text=f"{ctx.author}",icon_url=ctx.author.avatar_url)
        return embed


    @commands.group(name="shrimp",help="釣蝦場")
    async def shrimp(self,ctx:commands.Context):
        pass

    @shrimp.command(name="register", help="註冊釣蝦功能")
    async def register(self,ctx:commands.Context):
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)

        if(self.mongodata.add_shrimp_player(guild_id, author_id)):
            await ctx.send(embed = self.shrimpEmbed(ctx,"註冊成功!!"))
        else:
            await ctx.send(embed = self.shrimpEmbed(ctx,"你已經註冊囉!!"))

    @shrimp.command(name="level", help="查詢等級")
    async def level(self,ctx:commands.Context):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        x = self.mongodata.search_shrimp_player(guild_id, author_id)
        if(x != None):
            x = x[0]
            await ctx.send(embed = self.shrimpEmbed(ctx,
                                            f"玩家：{ctx.author.mention} \n \
                                            你的等級為：`{x['level']} ({x['exp']})`"))
        else:
            await ctx.send(embed = self.shrimpEmbed(ctx,"你尚未註冊喔!!"))

    @shrimp.command(name="exist", help="查詢蝦池內的蝦子數量")
    async def exist(self, ctx: commands.Context):
        guild_id = str(ctx.guild.id)
        x = self.mongodata.search_shrimp_count(guild_id)
        if (x != None):
            x = x[0]
            shrimps = x["shrimpcount"]
            counter = x["counter"]
            embed = self.shrimpEmbed(ctx,f"目前蝦池有`{shrimps}`隻蝦子。\n伺服器內的玩家曾經嘗試釣蝦過`{counter}`次。")
            await ctx.send(embed = embed)
        else:         
            await ctx.send(embed = self.shrimpEmbed(ctx,"你尚未註冊喔!!"))

    @commands.cooldown(5,1,commands.BucketType.guild)
    @shrimp.command(name="play",help="開釣!!!")
    async def play(self,ctx:commands.Context):
        author_id = str(ctx.author.id)
        # get author id
        guild_id = str(ctx.guild.id)
        # get guild id
        x = self.mongodata.search_shrimp_player(guild_id, author_id)
        if(x != None):
                x = x[0]
                fisherfile = discord.File("img//fish.gif", filename="fish.gif")
                fishingEmbed = self.shrimpEmbed(ctx,f"{ctx.author.mention}拋下釣竿，\n坐在椅子上靜靜等待蝦子的到來。")
                fishingEmbed.set_thumbnail(url="attachment://fish.gif")
                waiting_msg = await ctx.send(file = fisherfile, embed = fishingEmbed)
                ra.seed(None)
                k = ra.randint(1,5) # get shrimp or not
                w = ra.randint(1,6) # shrimp level
                await asyncio.sleep(1)
                await waiting_msg.delete()
                y = self.mongodata.search_shrimp_count(guild_id)
                y = y[0]
                if (y["shrimpcount"] > 0):
                    exp = 0
                    if (k > 3):
                        if (w <= 3):
                            exp = 0.5
                        else:
                            exp = 1
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
                    else:
                        resultEmbed = self.shrimpEmbed(ctx,"什麼都沒有釣到...")
                        await ctx.send(embed = resultEmbed)
                    # add counter into database
                    self.mongodata.update_shrimp_data(guild_id, author_id, exp)
                else:
                    # no shrimp in pool
                    noShrimpEmbed = self.shrimpEmbed(ctx,"釣蝦場內沒有蝦子了...\n等待下一次捕貨吧！")
                    await ctx.send(embed = noShrimpEmbed)                       
        # couldn't find author profile
        else:         
            await ctx.send(embed = self.shrimpEmbed(ctx,"你尚未註冊喔!!"))

    @shrimp.command(name='leaderboard', help='觀看前五名排行榜')
    async def leaderboard(self, ctx: commands.Context):
        guild_id = str(ctx.guild.id)
        # get guild id
        leaderboard = self.mongodata.search_shrimp_player(guild_id, p_limit=5)
        leaderboardEmbed = self.shrimpEmbed(ctx, f"🏆️{ctx.guild.name}的釣蝦場前五名排行榜🏆️")

        counter = 1

        prize = ['🥇','🥈','🥉','🏅']
        for x in leaderboard:
            if(x['_id'] != '0'):

                if(counter <= 3):
                    prize_output = f"{prize[counter]}第{counter}名："
                else:
                    prize_output = f"{prize[-1]}第{counter}名："

                leaderboardEmbed.add_field(name=prize_output + str(self.bot.get_user(int(x['_id']))),
                                           value=f"經驗值：`{x['exp']}`\n等級：`{x['level']}`",
                                           inline=False)
                counter += 1

        await ctx.send(embed=leaderboardEmbed)

    @play.error
    async def on_command_error(self,ctx:commands.Context,error:commands.errors):
        if isinstance(error,commands.CommandOnCooldown):
            overRodEmbed = self.shrimpEmbed(ctx,"釣蝦場只能容得下五根釣竿，\n請等待蝦子上鉤之後再拋下釣竿吧!!")
            await ctx.send(embed = overRodEmbed)

def setup(bot):
    bot.add_cog(shrimp(bot))