import discord
from discord.ext import commands
from datahook import yamlhook

class vtroles(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message):
        ydata = yamlhook("config.yaml").load()
        try:
            if message.channel.id in ydata['vtrole']['channel']:
                if message.content != ydata['vtrole'][message.channel.id]:
                    await message.delete()
                else:
                    pass
            else:
                pass
        except discord.NotFound:
            pass

def setup(bot):
    bot.add_cog(vtroles(bot))