from discord.ext import commands
from discord import app_commands, Interaction, Embed, Member
from mcfetch import Player

from mclinker.database.handlers import Link
from mclinker.logging import logger


class Who(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client


    @app_commands.command(name="who", description="View link information about a user")
    async def who(self, interaction: Interaction, member: Member=None):
        await interaction.response.defer(ephemeral=True)  
        try:
            if not member:
                member = interaction.user

            is_linked = Link(member.id).get_linked_user()
            if not is_linked:
                return await interaction.edit_original_response(
                    embed=Embed(
                        description=f"**{member.name}** is currently not linked.",
                        color=0xF15249
                    )
                )
            
            uuid: str = is_linked[1] 
            linked_at: int = is_linked[2]
            username: str = Player(player=uuid).name
            
            embed = Embed(
                title=f"{member.name}'s link information", color=0x5865F2,
                description=(
                    f"**Minecraft username**\n> `{username}`\n"
                    f"**Dashed UUID**\n> `{uuid}`\n"
                    f"**Undashed UUID**\n> `{uuid.replace("-", "")}`\n"
                    f"**Linked their account**\n> <t:{linked_at}:R>\n"
                )
            )
            embed.set_footer(text=f'Discord ID: {member.id}')

            return await interaction.edit_original_response(
                embed=embed
            )
        
        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong. Please try again later."
            )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Who(client))    