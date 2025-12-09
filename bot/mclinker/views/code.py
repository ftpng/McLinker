from discord import Interaction, ButtonStyle, Embed
from discord.ui import Modal, View, TextInput, Button, button

from bot.mclinker.database.handlers import Codes, Link
from bot.mclinker.logging import logger


class CodeModal(Modal, title="Verification"):
    """
    Modal for entering a 6-digit verification code.
    """

    code = TextInput(
        label="Enter your 6-digit verification code",
        placeholder="123456",
        max_length=6
    )

    def __init__(self, interaction: Interaction):
        """
        Initialize the modal with the calling interaction.

        :param interaction: The interaction that opened the modal.
        """
        super().__init__()
        self._interaction = interaction


    async def on_submit(self, interaction: Interaction):
        """
        Handle submission of the verification code.

        :param interaction: The modal submit interaction.
        :return: A response message depending on validation outcome.
        """
        try:
            code_int = int(self.code.value)
            data = Codes(code_int).get_code()

            if not data:
                return await interaction.response.send_message(
                    embed=Embed(
                        description="That code is incorrect or has expired.",
                        color=0xF15249
                    ),
                    ephemeral=True
                )

            uuid = data[2]
            username = data[1]

            Link(interaction.user.id).link_user(uuid)
            Codes(code_int).delete_code()

            await interaction.response.defer(ephemeral=True)
            return await self._interaction.edit_original_response(
                embed=Embed(
                    description=f"You have been successfully linked to **{username}**.",
                    color=0x32BA7C
                ),
                view=None,
            )

        except ValueError:
            return await interaction.response.send_message(
                embed=Embed(
                    description="Please enter a valid **6-digit** number.",
                    color=0xF15249
                ),
                ephemeral=True
            )

        except Exception as e:
            logger.error(e)
            return await interaction.response.send_message(
                embed=Embed(
                    description="Something went wrong. Try again later.",
                    color=0xF15249
                ),
                ephemeral=True
            )


class EnterCodeButton(View):
    """
    View containing the button for entering a verification code.
    """

    def __init__(self, interaction: Interaction, timeout: int = 300):
        """
        Initialize the view with a timeout and reference interaction.

        :param interaction: The interaction that created the view.
        :param timeout: Time in seconds before expiration.
        """
        super().__init__(timeout=timeout)
        self._interaction = interaction


    @button(label="Enter code", style=ButtonStyle.blurple, emoji="<:code:1447984035971203216>")
    async def enter_code(self, interaction: Interaction, button: Button):
        """
        Open the verification modal when the button is clicked.

        :param interaction: The button click interaction.
        :param button: The button instance that was pressed.
        """
        await interaction.response.send_modal(CodeModal(self._interaction))


    async def on_timeout(self):
        """
        Handle expiration of the linking request.

        :return: Edits the original message to indicate expiration.
        """
        self.clear_items()
        await self._interaction.edit_original_response(
            embed=Embed(
                description="This linking request has expired. Use **/link** again.",
                color=0xF15249
            ),
            view=None
        )