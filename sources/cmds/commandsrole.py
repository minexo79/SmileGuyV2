import discord
from discord.ext import commands

class commandsrole(commands.Cog):
    pass

def setup(bot):
    bot.add_cog(commandsrole(bot))