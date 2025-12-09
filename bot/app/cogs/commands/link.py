from discord.ext import commands
from discord import app_commands, Interaction, Embed

from mclinker.database.handlers import Codes, Link
from mclinker.logging import logger
from mclinker.views import EnterCodeButton


class Linking(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client

    @app_commands.command(name="link", description="Link your account")
    async def link(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)    
        try:
            embed = Embed(
                title="Link Your Minecraft Account",
                description=(
                    "To link your Discord account with your Minecraft account, follow the steps below:\n\n"
                    "> `1.` Launch **Minecraft** and join the server: `mclink.wither.host`\n"
                    "> `2.` You will immediately receive a **6-digit verification code** on join\n"
                    "> `3.` Return here and click the button below\n"
                    "> `4.` Enter your verification code in the popup window\n\n"
                    "Once completed, your accounts will be linked."
                ),
                color=0x5865F2
            )

            await interaction.edit_original_response(embed=embed, view=EnterCodeButton(interaction))

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong while linking. Please try again later."
            )


    @app_commands.command(name="unlink", description="Unlink your account")
    async def unlink(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)  

        try:
            is_linked = Link(interaction.user.id).get_linked_user()
            if not is_linked:
                return await interaction.edit_original_response(
                    embed=Embed(
                        description="You don't have an account linked! Use **/link** to link your account.",
                        color=0xF15249
                    )
                )
        
            Link(interaction.user.id).unlink_user()
            await interaction.edit_original_response(
                embed=Embed(
                    description="You have been successfully unlinked.",
                    color=0x32BA7C
                )
            )

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong while unlinking. Please try again later."
            )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Linking(client))    