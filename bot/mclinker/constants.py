from os import getenv
from typing import Text
from dotenv import load_dotenv

load_dotenv()


TOKEN: Text = getenv('TOKEN')

