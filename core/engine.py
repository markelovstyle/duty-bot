import os

from vkbottle.user import User
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

print(os.getenv("ONLY_CHAT"))