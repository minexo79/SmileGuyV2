import discord
from discord.ext import commands
from discord.utils import get

import asyncio

from datahook import yamlhook

ydata = yamlhook("config.yaml")

class commandsrole(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.rolesdata = ydata.load()
        self.dataOperate = ydata.Operate

        if("commandrole" not in dict(self.rolesdata).keys()):
            self.dataOperate(dictTopic="commandrole", setting={})
            # reload rolesdata
            self.rolesdata = ydata.load()

    def dataReload(self):
        self.rolesdata = ydata.load()

    @commands.Cog.listener()
    async def on_message(self,msg:discord.Message):
        if(msg.channel.id in dict(self.rolesdata)["commandrole"].keys()):
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
                    self.bot.sm_print(3,"Add roles Error Found! Check your role exists or not in backend.")

    @commands.command(name='addcm', help="新增指令身分組 `指令` `身分組`")
    @commands.has_permissions(administrator=True,manage_roles=True)
    async def add_command_role(self, ctx:commands.Context, cmds, * , role:discord.Role):

        split_cmd = str(cmds).split(',')
        if(ctx.channel.id not in dict(self.rolesdata["commandrole"]).keys()):
            newData = {
                ctx.channel.id : {
                    "command" : split_cmd,
                    "role" : role.id
                }
            }
            self.dataOperate(dictTopic="commandrole", setting=newData)
            # update role data
            self.rolesdata = ydata.load()
            # create successful embed message
            successEmbed = discord.Embed(title="成功!",description="已成功在此頻道新增關鍵字偵測",colour=self.bot.default_colour)
            successEmbed.add_field(name="使用指令", value=str(cmds).replace(',','/'), inline=False)
            successEmbed.add_field(name="獲取身分", value=role.mention,inline=False)
            msgOut = await ctx.send(embed=successEmbed)

            await asyncio.sleep(5)

            await msgOut.delete()

            await ctx.send("```md\n- 請觀看規則之後輸入相關指令獲取身分組喔!\n```")

def setup(bot):
    bot.add_cog(commandsrole(bot))