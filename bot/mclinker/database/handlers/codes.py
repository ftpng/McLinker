import asyncio
from mclinker.logging import logger
from mclinker.database import ensure_cursor, Cursor


class Codes:
    """
    Manage verification codes stored in the database.
    """

    def __init__(self, code: int) -> None:
        """
        Initialize a verification code handler.

        :param code: The verification code to operate on.
        """
        self._code: int = code


    @ensure_cursor(db='codes')
    def get_code(self, *, cursor: Cursor = None) -> int | None:
        """
        Retrieve the verification code entry.

        :param cursor: Optional database cursor provided by decorator.
        :return: The code record if found, otherwise None.
        """
        cursor.execute(
            "SELECT * FROM verify_codes WHERE code=%s",
            (self._code,),
        )
        data = cursor.fetchone()
        return data if data else None


    @ensure_cursor(db='codes')
    def delete_code(self, *, cursor: Cursor = None) -> None:
        """
        Delete the verification code entry.

        :param cursor: Optional database cursor provided by decorator.
        :return: None
        """
        cursor.execute(
            "DELETE FROM verify_codes WHERE code=%s",
            (self._code,),
        )


    @staticmethod
    @ensure_cursor(db='codes')
    def cleanup_expired_codes(*, cursor: Cursor = None) -> None:
        """
        Remove verification codes older than 5 minutes.

        :param cursor: Optional database cursor provided by decorator.
        :return: None
        """
        cursor.execute(
            "DELETE FROM verify_codes WHERE created_at < NOW() - INTERVAL 5 MINUTE"
        )


    @staticmethod
    async def cleanup_codes():
        """
        Periodically clean up expired verification codes every 60 seconds.

        :return: None
        """
        while True:
            try:
                Codes.cleanup_expired_codes()
            except Exception as e:
                logger.warning(e)

            await asyncio.sleep(60)