import os
import functools
import pymysql
from dotenv import load_dotenv
from pymysql.cursors import Cursor

load_dotenv()


def _get_database_credentials(db_key: str) -> tuple[str, str, str, str]:
    """
    Load database credentials depending on which database is requested.

    :param db_key: "codes" or "discord"
    :return: (username, password, database, endpoint)
    """

    db_key = db_key.upper()

    user = os.getenv(f"{db_key}_DBUSER")
    password = os.getenv(f"{db_key}_DBPASS")
    db_name = os.getenv(f"{db_key}_DBNAME")
    endpoint = os.getenv(f"{db_key}_DBENDPOINT")

    if not all([user, password, db_name, endpoint]):
        raise ValueError(f"Missing environment variables for DB key '{db_key}'")

    return user, password, db_name, endpoint


def db_connect(db: str = "discord"):
    """ 
    Connect to the selected database.

    :param db: "codes" (default) or "discord"
    :return: pymysql connection object
    """
    user, password, db_name, endpoint = _get_database_credentials(db)

    return pymysql.connect(
        host=endpoint,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        autocommit=True
    )


def ensure_cursor(db: str = "discord"):
    """
    Decorator: ensures a database cursor for a sync function.

    :param db: which database to use ("codes" or "discord")
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if "cursor" in kwargs and kwargs["cursor"]:
                return func(*args, **kwargs)

            with db_connect(db) as conn:
                cursor = conn.cursor()
                kwargs["cursor"] = cursor
                return func(*args, **kwargs)

        return wrapper
    return decorator


def async_ensure_cursor(db: str = "discord"):
    """
    Decorator: ensures a database cursor for an async coroutine.

    :param db: which database to use ("codes" or "discord")
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if "cursor" in kwargs and kwargs["cursor"]:
                return await func(*args, **kwargs)

            with db_connect(db) as conn:
                cursor = conn.cursor()
                kwargs["cursor"] = cursor
                return await func(*args, **kwargs)

        return wrapper
    return decorator