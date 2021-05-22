from discord import Intents, Game
from discord.ext import commands

from os import listdir, system
from datetime import datetime

from datahook import confighook

# TODO [] 多機架構
# TODO [] MongoDB / SQL 儲存
# TODO [] 遊戲: 幾A幾B
# TODO [] 自動化 Banner
# TODO [] 自動化 Voice Channel


class Bot(commands.Bot):
    def __init__(self,
                 prefix: str,
                 version: str):
        super(Bot, self).__init__(command_prefix=prefix,
                                  help_command=None,
                                  intents=Intents().all())
        self.prefix = prefix
        self.version = version
        self.default_colour = 0x3576E8
        self.shoumin_colour = 0xb322ab
        self.error_colour = 0xf0291a

    @property
    def currentVersion(self) -> str:
        return self.version

    @property
    def currentTime(self) -> str:
        nowtime = datetime.now() # get localtime
        return nowtime.strftime("%Y/%m/%d %H:%M:%S")

    def sm_print(self, func: int, out: str):
        msgOut = ""
        if(func == 1):      # infomation
            msgOut = f"\033[36m{self.currentTime}: I>\033[0m\n{out}"
        elif(func == 2):    # warning
            msgOut = f"\033[33m{self.currentTime}: W>\033[0m\n{out}"
        elif(func == 3):    # error
            msgOut = f"\033[31m{self.currentTime}: E>\033[0m\n{out}"
        print(msgOut)

    async def on_connect(self):
        self.sm_print(1, "Connecting...")
        
    async def on_ready(self):
        await self.change_presence(activity=Game(name=f"[{self.prefix} help] Smileguy is Running!!"))
        self.sm_print(1, f"{self.user.name} is on!")

    async def error_process(self, ctx:commands.Context, error:commands.CommandError):
        member = ctx.author.name
        # user discriminator
        discriminator = ctx.author.discriminator 
        # print to console
        self.sm_print(3, f"[{member}#{discriminator}]: {error}")


# get config from ini
bot_config = confighook(filename='config.ini')

bot = Bot(prefix=bot_config.botPrefix,
          version=bot_config.botVersion)


# Load Cog
def loadCog():
    system("cls")
    for filename in listdir('./cmds'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cmds.{filename[:-3]}')
                bot.sm_print(1, f"load [{filename[:-3]}] complete.")
            except Exception as e:
                pass
    bot.sm_print(1, "All extensions are loaded.")


if __name__ == "__main__":
    loadCog()
    bot.sm_print(1, f"Using Prefix: {bot.prefix}")
    # 抓取 bot token
    # 運行
    bot.run(bot_config.botToken, bot=True)
