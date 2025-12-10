import os
import discord
from mclinker import logger
from discord.ext import commands
from mclinker.database.handlers import Codes

intents = discord.Intents.all()
intents.message_content = True


class Client(commands.AutoShardedBot):
    def __init__(self, *, intents: discord.Intents = intents):

        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or('m%')
        )

    async def setup_hook(self):
        for folder in os.listdir("app/cogs"):
            for cog in os.listdir(f"app/cogs/{folder}"):
                if cog.endswith(".py"):
                    try:
                        await self.load_extension(name=f"app.cogs.{folder}.{cog[:-3]}")
                        logger.info(f"Loaded: {cog[:-3]} cog")

                    except commands.errors.ExtensionNotFound:
                        logger.warning(f"Failed to load {cog[:-3]}")

    async def on_ready(self):
        await self.loop.create_task(Codes.cleanup_codes())
        
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')