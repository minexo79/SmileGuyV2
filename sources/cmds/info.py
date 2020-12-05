import discord
from discord.ext import commands
import time,os,psutil

class info(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.command(name='about',help='關於機器人')
    async def about_cmd(self,ctx: commands.Context):
        file = discord.File(".//img/logo.png",filename="logo.png")
        # get locale file
        embed=discord.Embed(title="SmileGuy About Me",color=self.bot.default_colour)
        embed.set_thumbnail(url="attachment://logo.png")
        # bot image
        embed.add_field(name="版本/Version",value="1.5",inline=False)
        embed.add_field(name="作者/Author",value="minexo79\nXiao Xigua\n惡魔柴柴",inline=False)
        embed.add_field(name="簡介",value="哈囉！我是微笑小子。謝謝你加我到伺服器 >O<",inline=False)
        embed.add_field(name="原始碼/Source",value="https://github.com/minexo79/SmileGuyV2",inline=False)
        embed.add_field(name="邀請連結/Invite Link",value="https://reurl.cc/R4NQOz",inline=False)
        embed.set_footer(text=f"👾{str(self.bot.get_time)}")
        await ctx.send(embed=embed, file=file)

    @commands.command(name='userinfo',help='查詢對方資訊') # capture user infomation
    @commands.has_permissions(administrator=True)
    async def userinfo_cmd(self, ctx: commands.Context, member: discord.Member):
        roles = [role for role in member.roles] # count roles
        embed=discord.Embed(color=member.color)
        embed.set_thumbnail(url=member.avatar_url) # user image
        embed.add_field(name="對方名稱",value=member,inline=True) # display user name
        embed.add_field(name="對方暱稱",value=member.display_name,inline=True) # display user nickname in guild
        embed.add_field(name="創建日期",value=member.created_at.strftime("%Y.%m.%d-%H:%M:%S (UTC)"),inline=False)
        # display create user date
        embed.add_field(name="加入日期",value=member.joined_at.strftime("%Y.%m.%d-%H:%M:%S (UTC)"),inline=False)
        # display user join date
        if member.is_on_mobile() == True:
            # if user mobile is online
            embed.add_field(name="對方狀態",value="Moblie Online",inline=True)
        else:
            # otherwise
            embed.add_field(name="對方狀態",value=member.status,inline=True)
        embed.add_field(name="機器人",value=member.bot,inline=True)
        # display user is bot or not
        embed.add_field(name=f"身分組：{len(roles)}",value=" ".join([role.mention for role in roles]),inline=False)
        # display roles
        embed.set_footer(text=f"👾 ID:{member.id}")
        await ctx.send(embed=embed)
        
    @commands.command(name='serverinfo',help='伺服器資訊')
    @commands.has_permissions(administrator=True)
    async def serverinfo_cmd(self, ctx: commands.Context):
        guild = ctx.guild
        embed=discord.Embed(colour=self.bot.default_colour)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.add_field(name="伺服器擁有者",value=guild.owner.name,inline=True)
        embed.add_field(name="伺服器創立時間",value=guild.created_at.strftime("%Y.%m.%d-%H:%M:%S (UTC)"),inline=True)
        embed.add_field(name="伺服器成員數量",value=guild.member_count,inline=True)
        embed.add_field(name="文字頻道數量",value=len(guild.text_channels),inline=True)
        embed.add_field(name="語音頻道數量",value=len(guild.voice_channels),inline=True)
        embed.add_field(name="伺服器身分組數量",value=len(guild.roles),inline=True)
        embed.set_footer(text=f"👾 ID:{guild.id}")
        await ctx.send(embed=embed)

    @commands.command(name='status',help='機器人狀態查詢')
    async def status_cmd(self,ctx: commands.Context):
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.trigger_typing()

        embed=discord.Embed(title="SmileGuy Status",color=self.bot.default_colour)
        process = psutil.Process(os.getpid()).memory_info().rss # get app used ram
        percent = psutil.virtual_memory().percent # get used ram percent
        embed.add_field(name="Used Ram",value=f"```{round(process/1000000)} MB ({percent}%)```",inline=False)
        embed.add_field(name="Bot Ping",value=f"```{round(self.bot.latency*1000)} ms```",inline=True)
        embed.add_field(name="Sys Ping",value=f"```{round((t2-t1)*1000)} ms```",inline=True)
        embed.set_footer(text=f"👾{str(self.bot.get_time)}")
        await ctx.send(embed=embed)

    @commands.command(name='help',help='指令幫助')
    async def help(self,ctx: commands.Context, groupName=None):
        helpCommand = []
        helptext = []
        groupCommand = {}
        if groupName != None:
            for command in self.bot.commands:
                # find group commands
                if command.name == groupName:
                    # dict copy
                    groupCommand = command.all_commands
                    # get group commands > key
                    helpCommand = list(groupCommand.keys())
                    for i in range(len(helpCommand)):
                        # get group commands help
                        # command help is empty
                        if groupCommand[helpCommand[i]].help == None:
                            helptext.append("這主人很懶，沒有留下任何訊息!")
                        else:
                            helptext.append(groupCommand[helpCommand[i]].help)
                    break
        else:
            for command in self.bot.commands:
                helpCommand.append(command.name)
                # command help is empty
                if command.help == None:
                    helptext.append("這主人很懶，沒有留下任何訊息!")
                else:
                    helptext.append(command.help)
        # embed
        helpDisplay = discord.Embed(title="SmileGuy Commands Help",color=self.bot.default_colour)
        for i in range(len(helpCommand)):
            if groupName == None: 
                groupName = ""
                helpDisplay.add_field(name=f"{ctx.prefix}{helpCommand[i]}",value=helptext[i],inline=False)     
            else:
                helpDisplay.add_field(name=f"{ctx.prefix}{groupName} {helpCommand[i]}",value=helptext[i],inline=False)   
        helpDisplay.add_field(name="About",value=f"My prefix is `{ctx.prefix}` | Use `{ctx.prefix}help` to see all commands.",inline=False)
        helpDisplay.set_footer(text=f"👾{str(self.bot.get_time)}")
        await ctx.send(embed = helpDisplay)

def setup(bot):
    bot.add_cog(info(bot))
