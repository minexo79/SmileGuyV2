import discord
from discord.ext import commands

class event(commands.Cog):

    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self,ctx:commands.Context): # 印出使用者動作
        await ctx.message.delete()
        member = ctx.author.name # user name
        discriminator = ctx.author.discriminator # user discriminator
        content = ctx.command # user commands
        self.bot.sm_print(1,f"[{member}#{discriminator}]: issue a command: {content}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:commands.CommandError): # 指令錯誤
        try:
            if isinstance(error,commands.CommandOnCooldown):
                pass
            else: # send to error_process
                await self.bot.error_process(ctx,error)
        except AttributeError:
            pass

def setup(bot):
    bot.add_cog(event(bot))