import discord
from discord import Embed
from discord.ext import commands
from datahook import yamlhook

class blacklist(commands.Cog):

    def __init__(self,bot:commands.Bot):
        # initialize setting
        self.bot = bot

        ydata = yamlhook("database.yaml").load()
        
        if(ydata == None or type(ydata['blacklist']) is not list):
            ydata['blacklist'] = []

        yamlhook("database.yaml").Operate('blacklist',ydata['blacklist'])

    @commands.Cog.listener()
    async def on_member_join(self,member:discord.User):
        # 被動Ban掉黑名單內的指定用戶
        ydata = yamlhook("database.yaml").load()
        if member.id in ydata['blacklist']:
            await member.kick(reason=None)
            self.bot.sm_print(2,f"Detected {member}! has been kicked!")

    @commands.group(name='bl',help='防踢功能')
    async def blacklist(self,ctx):
        pass

    @blacklist.command(name='list',help='瀏覽黑名單')
    @commands.has_permissions(administrator=True)
    async def black_list(self,ctx:commands.Context):
        ydata = yamlhook("database.yaml").load()
        blacklist = [bm for bm in ydata['blacklist']]
        # embed
        embedout = Embed(color=self.bot.default_colour)
        embedout.add_field(name='目前黑名單內的ID',value = f"{blacklist}",inline=False)
        await ctx.send(embed = embedout)

    @blacklist.command(name='add',help='增加至黑名單 <對方id>')
    @commands.has_permissions(administrator=True)
    async def black_add(self,ctx:commands.Context,member:discord.User):
        ydata = yamlhook("database.yaml").load()
        # open blacklist
        if member.id not in ydata['blacklist']:         
            # 檢查一次，防止有兩個同樣的ID存在
            ydata['blacklist'].append(member.id)        
            # blacklist add content
            yamlhook("database.yaml").Operate('blacklist',ydata['blacklist'])
            # 輸出增加成功
            embedout = Embed(colour=self.bot.default_colour)
            embedout.add_field(name='✅ 成功',value = f"`{member}`已增加到黑名單！",inline=False)
            await ctx.send(embed = embedout)
        else:
            embedout = Embed(colour=self.bot.default_colour)
            embedout.add_field(name='❌ 失敗',value = f"`{member}`已在黑名單內！",inline=False)
            await ctx.send(embed = embedout)

    @blacklist.command(name='re',help='從黑名單移除 <對方id>')
    @commands.has_permissions(administrator=True)
    async def black_remove(self,ctx:commands.Context,member:discord.User):
        ydata = yamlhook("database.yaml").load()
        # open blacklist
        try:
            ydata['blacklist'].remove(member.id)        
            # blacklist remove content
            yamlhook("database.yaml").Operate('blacklist',ydata['blacklist'])
            # 輸出移除成功
            embedout = Embed(colour=self.bot.default_colour)
            embedout.add_field(name='✅ 成功',value = f"`{member}`已從黑名單移除！",inline=False)
            await ctx.send(embed = embedout)
        except ValueError: # 找不到ID
            embedout = Embed(colour=self.bot.default_colour)
            embedout.add_field(name='❌ 失敗',value = f"找不到`{member}`的資料。",inline=False)
            await ctx.send(embed = embedout)

def setup(bot):
    bot.add_cog(blacklist(bot))