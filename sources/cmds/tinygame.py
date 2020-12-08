import discord
from discord.ext import commands

import random as ra
import requests
import time,asyncio,re,copy
from asyncio import gather 
from datahook import yamlhook
emojis = ['✊', '🖐', '✌']

class Sokoban():
    def __init__(self,difficulty):
        if difficulty==None :
            high=10
            width=10
            number=1
        else :
            high=10 + difficulty
            width=10 + difficulty
            number=difficulty
        self.map1=[[]]*high
        self.box=[]
        repeat=[]
        for i in range(high):
            if i == 0 or i == high-1 : self.map1[i] = ["🔲"]*width
            else:
                self.map1[i]=[""]*width
                for x in range(width) :
                    if x == 0 or x == width-1 :self.map1[i][x] = "🔲"
                    else : self.map1[i][x]="⬛"
        while 1 :
            if [ra.randint(1,high-2),ra.randint(1,width-2)] not in repeat :
                repeat.append([ra.randint(2,high-3),ra.randint(2,width-3)])
            if len(repeat)==2+number:
                break

        for i in range(len(repeat)) :
            if i == 0 :
                self.player=repeat[0]
            elif i == 1 :
                self.end=repeat[1]
            else :
                self.box.append(repeat[i])
    def userinput(self,x):
        if x in ["◀","🔼","🔽","▶","⏹"]:
            y={"🔼":self.up,"🔽":self.down,"◀":self.left,"▶":self.right}
            y[x]()
    def up(self):
        if self.map1[self.player[0]-1][self.player[1]] != "🔲" :
            if ([self.player[0]-1,self.player[1]] !=self.end) and ([self.player[0]-1,self.player[1]] not in self.box):#自己移動
                self.player[0]-=1
            elif ([self.player[0]-1,self.player[1]] in self.box) :#推箱子
                box=self.box[self.box.index([self.player[0]-1,self.player[1]])]
                if self.map1[box[0]-1][box[1]] !="🔲" and [box[0]-1,box[1]] not in self.box:
                    if [box[0]-1,box[1]] ==self.end:
                        del self.box[self.box.index([self.player[0]-1,self.player[1]])]
                    else :
                        self.box[self.box.index([self.player[0]-1,self.player[1]])][0]-=1
                    self.player[0]-=1

    def down(self):
        if self.map1[self.player[0]+1][self.player[1]] != "🔲" :
            if ([self.player[0]+1,self.player[1]] !=self.end) and ([self.player[0]+1,self.player[1]] not in self.box):#自己移動
                self.player[0]+=1
            elif ([self.player[0]+1,self.player[1]] in self.box) :#推箱子
                box=self.box[self.box.index([self.player[0]+1,self.player[1]])]
                if self.map1[box[0]+1][box[1]] !="🔲" and [box[0]+1,box[1]] not in self.box:
                    if [box[0]+1,box[1]] ==self.end:
                        del self.box[self.box.index([self.player[0]+1,self.player[1]])]
                    else :
                        self.box[self.box.index([self.player[0]+1,self.player[1]])][0]+=1
                    self.player[0]+=1
    def left(self):
        if self.map1[self.player[0]][self.player[1]-1] != "🔲" :
            if ([self.player[0],self.player[1]-1] !=self.end) and ([self.player[0],self.player[1]-1] not in self.box):#自己移動
                self.player[1]-=1
            elif ([self.player[0],self.player[1]-1] in self.box) :#推箱子
                box=self.box[self.box.index([self.player[0],self.player[1]-1])]
                if self.map1[box[0]][box[1]-1] !="🔲" and [box[0],box[1]-1] not in self.box:
                    if [box[0],box[1]-1] ==self.end:
                        del self.box[self.box.index([self.player[0],self.player[1]-1])]
                    else :
                        self.box[self.box.index([self.player[0],self.player[1]-1])][1]-=1
                    self.player[1]-=1
    def right(self):
        if self.map1[self.player[0]][self.player[1]+1] != "🔲" :
            if ([self.player[0],self.player[1]+1] !=self.end) and ([self.player[0],self.player[1]+1] not in self.box):#自己移動
                self.player[1]+=1
            elif ([self.player[0],self.player[1]+1] in self.box) :#推箱子
                box=self.box[self.box.index([self.player[0],self.player[1]+1])]
                if self.map1[box[0]][box[1]+1] !="🔲" and [box[0],box[1]+1] not in self.box:
                    if [box[0],box[1]+1] ==self.end:
                        del self.box[self.box.index([self.player[0],self.player[1]+1])]
                    else :
                        self.box[self.box.index([self.player[0],self.player[1]+1])][1]+=1
                    self.player[1]+=1
    def mapprint(self):
        map2=copy.deepcopy(self.map1)
        map2[self.player[0]][self.player[1]]="🌝"#人物
        map2[self.end[0]][self.end[1]]="🟨"#終點
        for i in self.box :
            map2[i[0]][i[1]]="🔳"#箱子
        if not len(self.box):return ("\n".join(["".join(i) for i in map2]),True)
        else :return ("\n".join(["".join(i) for i in map2]),False)
        


class tinygame(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        # load yaml
        data = (yamlhook("database.yaml").load())

        if (data == None) or ('shrimp' not in list(data.keys())) or (type(data['shrimp']) is not dict):
            # initialize data
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

    # This Embed is for Shrimp
    # Do not make any changes!!!!!!
    # By Tsai XO 2020.12.4
    def shrimpEmbed(self,ctx:commands.Context,x:str):
        embed=discord.Embed(title="釣蝦系統",description=x,color=self.bot.default_colour)
        embed.set_footer(text=f"{ctx.author}",icon_url=ctx.author.avatar_url)
        return embed

    #
    # ----------------------------------------------------------------------------------------------
    #
    @commands.group(name='tinygame',help='機器人小遊戲')
    async def tinygame(self,ctx:commands.Context):
        pass


    # sokoban 
    # made by: xiao xigua#8597
    # 109.12.5
    @tinygame.command(name='sokoban',help="推箱子。(感謝 xiao xigua#8597 撰寫)")
    async def sokoban(self,ctx:commands.Context,level:int=None):

        ww = Sokoban(level)
        text,_ = ww.mapprint()
        embed = discord.Embed(title=f"sokoban 推箱子\n玩家: {ctx.author}",description=f"```\n{text}\n```",colour=self.bot.default_colour)
        message = await ctx.send(embed=embed)
        await message.add_reaction("◀")
        await message.add_reaction("🔼")
        await message.add_reaction("🔽")
        await message.add_reaction("▶")
        await message.add_reaction("⏹")
        def check(reaction, user):
            return user == ctx.author and reaction.message == message 
        while(1):
            reaction, user = await self.bot.wait_for("reaction_add",timeout=60.0,check=check)
            await message.remove_reaction(reaction,user)
            # stop this game
            if (str(reaction) == "⏹"):
                await message.delete()
                break
            ww.userinput(str(reaction))
            text,t = ww.mapprint()
            embed = discord.Embed(title=f"sokoban 推箱子\n玩家: {ctx.author}",description=f"```\n{text}\n```",colour=self.bot.default_colour)
            await message.edit(embed=embed)
            if (t):
                await message.delete()
                successfulEmbed = discord.Embed(colour=self.bot.default_colour)
                successfulEmbed.add_field(name="sokoban 推箱子",value=f"恭喜 {ctx.author} 過關!!!",inline=False)
                await ctx.send(embed=successfulEmbed)
                break

    @tinygame.command(name='pick',help='自訂抽籤，選項之間可用`，`,`空格`,`/`,`|`連結(不要混用!)。')
    async def pick_cmd(self,ctx:commands.Context,*user_input):
        try:
            # initialize random seed 
            ra.seed(a=time.localtime().tm_sec)
            # define new list
            data = []
            # define a list contained Delimiter
            delimiter = [',','，','/','|']
            # check if there is ',' and '，'
            input = list(user_input)
            for i in range(len(input)):
                pt = -1
                for j in range(len(delimiter)):
                    if delimiter[j] in input[i]:
                        commalist = input[i].split(delimiter[j])
                        data += commalist
                        pt = i
                        break
                if pt != i:
                    data.append(input[i])
            # use random to pick up a selection
            selection = ra.choice(data)
            # show message
            await ctx.send(":confused: 我選擇: " + selection)
        except IndexError:
            await ctx.send("> 找不到選項，請勿只輸入空格。")

    @tinygame.command(name='draw',help='神社抽籤，在指令後面輸入問題')
    async def draw_cmd(self,ctx:commands.Context,question:str):
        await ctx.trigger_typing()
        # embed
        begin = discord.Embed(color=self.bot.default_colour)
        begin.add_field(name="問題",value=question,inline=False)
        begin.add_field(name="發問者",value=ctx.author.mention,inline=False)
        begin.set_footer(text=f"👾{str(self.bot.get_time)}")
        # send to user
        await ctx.send(embed=begin)
        await asyncio.sleep(1)
        await ctx.trigger_typing()
        # initialize random seed 
        ra.seed(a=time.localtime().tm_sec)
        choose_img = ra.randint(1,7)
        # call local image
        try:
            file = discord.File(f".//img/shoumin_picks/{choose_img}.png",filename=f"{choose_img}.png")
            # embed
            resultEmbed = discord.Embed(title='抽籤結果',color=self.bot.shoumin_colour)
            resultEmbed.set_image(url=f"attachment://{choose_img}.png")
            resultEmbed.set_footer(text=f"👾圖片繪師：Vtuber 雙命裂\nhttps://www.youtube.com/user/jokeherogjo")
            # send to user
            await ctx.send(embed=resultEmbed,file=file)

        except FileNotFoundError:
            raise FileNotFoundError("Can't found the image in image folder.")

    
    async def rps_dm_helper(self,player: discord.User, opponent: discord.User):
        if player.bot:
            return random.choice(emojis)

        message = await player.send(f" {opponent}邀請您跟他PK剪刀、石頭、布. 請做出你的選擇.")

        for e in emojis:
            await message.add_reaction(e)

        try:
            reaction, _ = await self.bot.wait_for('reaction_add',check=lambda r, u: r.emoji in emojis and r.message.id == message.id and u == player,timeout=60)
        except asyncio.TimeoutError:
            return None

        return reaction.emoji



    @tinygame.command(name='rps',help='猜拳@對戰玩家 None跟機器人對戰')
    async def rps(self,ctx, opponent: discord.User = None):


      if opponent is None:
          opponent = self.bot.user
      author_helper = tinygame.rps_dm_helper(self,ctx.author, opponent)  
      opponent_helper = tinygame.rps_dm_helper(self,opponent, ctx.author)
      author_emoji, opponent_emoji = await gather(author_helper, opponent_helper)

      if author_emoji is None:
          await ctx.send(f"```diff\n- RPS: {ctx.author} 未在時間內出拳\n```")
          return

      if opponent_emoji is None:
          await ctx.send(f"```diff\n- RPS: {opponent} 未在時間內出拳\n```")
          return

      author_idx = emojis.index(author_emoji)
      opponent_idx = emojis.index(opponent_emoji)

      if author_idx == opponent_idx:
          winner = None
      elif author_idx == (opponent_idx + 1) % 3:
          winner = ctx.author
      else:
          winner = opponent

   
      #await ctx.send([f'【{ctx.author}出{author_emoji}】你的對手【{opponent}出{opponent_emoji}】贏家:{winner} !',f'【{ctx.author}出{author_emoji}】【{opponent}出{opponent_emoji}】 平手'][winner is None])
      text=[]
      text.append([f'你:【{ctx.author}出了{author_emoji}】你的對手:【{opponent}出了{opponent_emoji}】\n**贏家:{winner}!**',f'你:【{ctx.author}出{author_emoji}】你的對手:【{opponent}出了{opponent_emoji}】\n **平手**'][winner is None])    
      embed =discord.Embed(title="猜拳結果",color=0X00ff40,description="".join(text))
      await ctx.send(embed=embed)
    #
    # ----------------------------------------------------------------------------------------------
    #
    @commands.group(name="shrimp",help="釣蝦場")
    async def shrimp(self,ctx:commands.Context):
        pass

    @shrimp.command(name="register",help="註冊釣蝦功能")
    async def register(self,ctx:commands.Context):
        guild_id = str(ctx.guild.id)
        if guild_id not in list(self.data.keys()):
            self.data[guild_id] = {}
            self.data[guild_id]['user'] = []
            self.data[guild_id]['shrimpcount'] = ra.randint(30,50)
            self.data[guild_id]['counter'] = 0
        author_id = str(ctx.author.id)
        for i in self.data[guild_id]['user']:
            if(author_id in i.keys()):
                await ctx.send(embed=self.shrimpEmbed(ctx,"你已經註冊囉!!"))
                return
        # couldn't find author profile
        self.data[guild_id]['user'].append({author_id : 0})
        self.dump_yaml(setting = self.data,dictTopic='shrimp')
        await ctx.send(embed = self.shrimpEmbed(ctx,"註冊成功!!"))

    @shrimp.command(name="xp",help="查詢經驗值")
    async def xp(self,ctx:commands.Context):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if (guild_id in list(self.data.keys())):
            for i in self.data[guild_id]['user']:
                if(author_id in i.keys()):
                    await ctx.send(embed = self.shrimpEmbed(ctx,f"{ctx.author.mention} 你的經驗值為: `{i[author_id]}`"))
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
                                resultEmbed.add_field(name=None,value=f"經驗值加`0.5`!",inline=True)
                            else:
                                # special shrimp
                                resultEmbed = self.shrimpEmbed(ctx,f"{ctx.author.mention}\n你釣到了...**大蝦蝦!!!**")
                                resultEmbed.add_field(name=None,value=f"經驗值加`1`!",inline=True)
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
    bot.add_cog(tinygame(bot))