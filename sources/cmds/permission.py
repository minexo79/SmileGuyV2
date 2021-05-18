import discord
from discord.ext import commands


class permission(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def embed(self, message: str):
        return discord.Embed(title='SmileGuy Cog Reload',
                             description=message,
                             colour=self.bot.default_colour)

    @commands.group(name='owner', help='此功能僅限機器人擁有者使用')
    async def owner(self, ctx):
        pass

    @owner.command(name='reload', help='Cog mod重新載入')
    @commands.is_owner()
    async def reload_cmd(self, ctx: commands.Context, extension: str):
        self.bot.reload_extension(f"cmds.{extension}")
        # console message
        self.bot.sm_print(1, f"[{extension}] has reloaded.")
        await ctx.send(embed=self.embed(f"`{extension}`已重新載入。"))

    @owner.command(name='load', help='Cog mod裝入')
    @commands.is_owner()
    async def load_cmd(self, ctx: commands.Context, extension: str):
        self.bot.load_extension(f"cmds.{extension}")
        # console message
        self.bot.sm_print(1, f"[{extension}] has loaded.")
        await ctx.send(embed=self.embed(f"{extension}`已載入。"))

    @owner.command(name='unload', help='Cog mod移除')
    @commands.is_owner()
    async def unload_cmd(self, ctx: commands.Context, extension: str):
        self.bot.unload_extension(f"cmds.{extension}")
        # console message
        self.bot.sm_print(1, f"[{extension}] has unloaded.")
        await ctx.send(embed=self.embed(f"`{extension}`已移除。"))

    @owner.command(name='bye', help='關閉機器人')
    @commands.is_owner()
    async def bye_cmd(self, ctx: commands.Context):
        await ctx.send(embed=self.embed("正在關閉機器人..."))
        # console message
        self.bot.sm_print(1, "Bot closed.")
        await self.bot.close()


def setup(bot):
    bot.add_cog(permission(bot))
