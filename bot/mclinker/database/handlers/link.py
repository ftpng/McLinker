import time
from mclinker.logging import logger
from mclinker.database import ensure_cursor, Cursor


class Link:
    """
    Handle linking and unlinking of Discord users to UUIDs.
    """

    def __init__(self, discord_id: int) -> None:
        """
        Initialize the Link handler for a Discord user.

        :param discord_id: The Discord user's ID.
        """
        self._discord_id: int = discord_id


    @ensure_cursor(db='discord')
    def get_linked_user(self, *, cursor: Cursor = None) -> dict | None:
        """
        Retrieve the linked user entry for this Discord ID.

        :param cursor: Optional database cursor provided by decorator.
        :return: A dict of user data if found, otherwise None.
        """
        cursor.execute(
            "SELECT * FROM linked_users WHERE discord_id = %s",
            (self._discord_id,),
        )
        data = cursor.fetchone()
        return data if data else None


    @ensure_cursor(db='discord')
    def link_user(self, uuid: str, *, cursor: Cursor = None) -> None:
        """
        Link a Discord user to a UUID, inserting or updating the record.

        :param uuid: The UUID to link to the Discord user.
        :param cursor: Optional database cursor provided by decorator.
        :return: None
        """
        cursor.execute(
            "SELECT * FROM linked_users WHERE discord_id = %s",
            (self._discord_id,),
        )

        data = cursor.fetchone()
        linked_at = int(time.time())

        if not data:
            cursor.execute(
                "INSERT INTO linked_users (discord_id, uuid, linked_at) "
                "VALUES (%s, %s, %s)",
                (self._discord_id, uuid, linked_at),
            )
        else:
            cursor.execute(
                "UPDATE linked_users SET uuid=%s, linked_at=%s WHERE discord_id=%s",
                (uuid, linked_at, self._discord_id),
            )


    @ensure_cursor(db='discord')
    def unlink_user(self, *, cursor: Cursor = None) -> None:
        """
        Remove the linked user entry for this Discord ID.

        :param cursor: Optional database cursor provided by decorator.
        :return: None
        """
        cursor.execute(
            "DELETE FROM linked_users WHERE discord_id=%s",
            (self._discord_id,),
        )