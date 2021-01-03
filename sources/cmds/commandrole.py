import discord
from discord.ext import commands
from discord.utils import get

import asyncio

from datahook import yamlhook

ydata = yamlhook("config.yaml")

class commandrole(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.rolesdata = ydata.load()
        self.dataOperate = ydata.Operate

        if("commandrole" not in dict(self.rolesdata).keys()):
            self.dataOperate(dictTopic="commandrole", setting={})
            # upload rolesdata
            self.rolesdata = ydata.load()

    # reload data
    # ------------------------------------------------------------------------------------------
    
    def dataReload(self):
        self.rolesdata = ydata.load()

    # embed message send
    # ------------------------------------------------------------------------------------------

    async def embedSend(self,ctx:commands.Context, sendEmbed = discord.Embed):
        msgOut = await ctx.send(embed=sendEmbed)
        # wait 5 seconds
        await asyncio.sleep(5)
        # delete message
        await msgOut.delete()

    @commands.Cog.listener()
    async def on_message(self,msg:discord.Message):
        if(msg.channel.id in dict(self.rolesdata)["commandrole"].keys()):
            user_permissions = msg.author.guild_permissions
            # if message sender is bot or admin   
            if(msg.author.bot == False) and (user_permissions.manage_roles == False):
                await msg.delete()
            _channel = self.rolesdata["commandrole"][msg.channel.id]
            if(msg.content in _channel["command"]):
                try:  
                    target_role = get(msg.author.guild.roles, id=_channel["role"])
                    await msg.author.add_roles(target_role)
                    member = msg.author.name # user name
                    discriminator = msg.author.discriminator # user discriminator
                    self.bot.sm_print(1, f"[{member}#{discriminator}] input correct command [{msg.content}], add role [{target_role.name}] to it.")
                except:
                    self.bot.sm_print(3,"Add roles Error Found! Check your role has exists or not in backend.")  

    # command group
    # ------------------------------------------------------------------------------------------
    @commands.group(name='cm',help='指令身分組')
    @commands.has_permissions(administrator=True,manage_roles=True)
    async def commandroleGroup(self,ctx):
        pass

    # command group error
    # ------------------------------------------------------------------------------------------
    @commandroleGroup.error
    async def on_error(self,ctx:commands.Context,error:discord.errors):
        pass
    
    # add command role
    # ------------------------------------------------------------------------------------------

    @commandroleGroup.command(name='add', help="新增指令身分組 `指令` `身分組`")
    async def add_command_role(self, ctx:commands.Context, cmds:str , role:discord.Role):
        # split keyword
        split_cmd = str(cmds).split(',')
        if(ctx.channel.id not in dict(self.rolesdata["commandrole"]).keys()):
            newData = {
                ctx.channel.id : {
                    "command" : split_cmd,
                    "role" : role.id
                }
            }
            self.dataOperate(dictTopic="commandrole", setting=newData)
            # create successful embed message
            successEmbed = discord.Embed(title="成功!",description="已成功在此頻道新增指令身分組。",colour=self.bot.default_colour)
            successEmbed.add_field(name="使用指令", value=str(cmds).replace(',','/'), inline=False)
            successEmbed.add_field(name="獲取身分", value=role.mention,inline=False)
            await self.embedSend(ctx, successEmbed)

            await ctx.send("```md\n- 請觀看規則之後輸入相關指令獲取身分組喔!\n```")
            # reload data
            self.dataReload()
        else:
            existEmbed = discord.Embed(title="提醒!",description="每個頻道只能有一個指令而已喔。",colour=self.bot.default_colour)
            # send embed message
            await self.embedSend(ctx, existEmbed)


    # check command role
    # ------------------------------------------------------------------------------------------

    @commandroleGroup.command(name='check', help="檢查頻道內是否存在指令身分組")
    async def check_command_role(self, ctx:commands.Context):
        # check channel id has in data or not
        if(ctx.channel.id not in dict(self.rolesdata["commandrole"]).keys()): 
            # create embed message
            notFoundEmbed = discord.Embed(title="抱歉", description="我找不到這個頻道內存在的指令喔!!",colour=self.bot.default_colour)
            # send embed message
            await self.embedSend(ctx, notFoundEmbed)
        else:
            # create embed message
            existEmbed = discord.Embed(title="指令查詢",description="以下是這個頻道內被觸發的指令",colour=self.bot.default_colour)
            # get commandrole info in this channel 
            _channel = self.rolesdata["commandrole"][ctx.channel.id]
            target_role = get(ctx.author.guild.roles, id=_channel["role"])
            existEmbed.add_field(name="使用指令", value=''.join(_channel["command"]), inline=False)
            existEmbed.add_field(name="獲取身分", value=target_role.mention,inline=False)
            # send embed message
            await self.embedSend(ctx, existEmbed)
    
    # remove command role
    # ------------------------------------------------------------------------------------------

    @commandroleGroup.command(name='rm', help="刪除頻道內的身分組指令")
    async def remove_command_role(self, ctx:commands.Context):
        if(ctx.channel.id not in dict(self.rolesdata["commandrole"]).keys()): 
            # create embed message
            notFoundEmbed = discord.Embed(title="抱歉", description="我找不到這個頻道內存在的指令喔!!",colour=self.bot.default_colour)
            # send embed message
            await self.embedSend(ctx, notFoundEmbed)
        else:
            # remove data
            _role = self.rolesdata["commandrole"]
            del _role[ctx.channel.id]
            self.dataOperate(dictTopic="commandrole", setting=_role)
            # create successful embed message
            successEmbed = discord.Embed(title="成功!",description="已成功在此頻道移除指令身分組。",colour=self.bot.default_colour)
            # send embed message
            await self.embedSend(ctx, successEmbed)
        # reload data
        self.dataReload()

    # rename command role
    # ------------------------------------------------------------------------------------------

    @commandroleGroup.command(name='rename', help='更改獲取指令')
    async def rename_command_role(self, ctx:commands.Context, cmds:str):
        # split keyword
        split_cmd = str(cmds).split(',')
        # check data has exist or not
        if(ctx.channel.id in dict(self.rolesdata["commandrole"]).keys()):
            # get commandrole info in this channel 
            _channel = self.rolesdata["commandrole"][ctx.channel.id]
            newData = {
                ctx.channel.id : {
                    "command" : split_cmd,
                    "role" : _channel["role"]          
                }
            }

            self.dataOperate(dictTopic="commandrole", setting=newData)
            # create successful embed message
            successEmbed = discord.Embed(title="成功!",description="已成功在此頻道更改指令或者身分組。",colour=self.bot.default_colour)
            successEmbed.add_field(name="更改後使用指令", value=str(cmds).replace(',','/'), inline=False)
            # delete message
            await ctx.message.delete()
            # send embed message
            await self.embedSend(ctx, successEmbed)
            # reload data
            self.dataReload()  

        else:
            # create embed message
            notFoundEmbed = discord.Embed(title="抱歉", description="我找不到這個頻道內存在的指令喔!!",colour=self.bot.default_colour)
            # send embed message
            await self.embedSend(ctx, notFoundEmbed)

    # rerole command role
    # ------------------------------------------------------------------------------------------

    @commandroleGroup.command(name='rerole', help='更改指派之身分組')
    async def rerole_command_role(self, ctx:commands.Context, role:discord.Role):
        # check data has exist or not
        if(ctx.channel.id in dict(self.rolesdata["commandrole"]).keys()):
            # get commandrole info in this channel 
            _channel = self.rolesdata["commandrole"][ctx.channel.id]
            # input command and role
            newData = {
                ctx.channel.id : {
                        "command" : _channel["command"],
                        "role" : role.id     
                }
            }

            self.dataOperate(dictTopic="commandrole", setting=newData)
            # create successful embed message
            successEmbed = discord.Embed(title="成功!",description="已成功在此頻道更改身分組。",colour=self.bot.default_colour)
            successEmbed.add_field(name="更改後指派身分組", value=role.mention, inline=False)
            # delete message
            await ctx.message.delete()
            # send embed message
            await self.embedSend(ctx, successEmbed)
            # reload data
            self.dataReload()  
        else:
            # create embed message
            notFoundEmbed = discord.Embed(title="抱歉", description="我找不到這個頻道內存在的指令喔!!",colour=self.bot.default_colour)
            # send embed message
            await self.embedSend(ctx, notFoundEmbed)

def setup(bot):
    bot.add_cog(commandrole(bot))