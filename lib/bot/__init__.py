from datetime import datetime
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "+"
OWNER_IDS = [963358996994097202]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()


        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),

        )

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Someting went wrong.")

        channel = self.get_channel(966019947241308292)
        await channel.send("An error occured.")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(742767786635296810)
            print("bot ready")

            channel = self.get_channel(966019947241308292)
            await channel.send("Now online!")

            embed = Embed(title="Now online!", description="Sequence is now online.",
                          colour=0xFF0000, timestamp=datetime.utcnow())
            fields = [("Name","Value", True),
                      ("Another fields", "This field is next to the other one.", True),
                      ("A non-inline field", "This Field will appear on it's own row.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Sequence Tutorials", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer")
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)

            await channel.send(file=File("./data/images/profile.png"))




        else:
            print("bot reconnected")


    async def on_message(self, message):
        pass


bot = Bot()