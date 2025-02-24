from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ENDPOINT = os.getenv("URL")
API_TOKEN = os.getenv("API_ADMIN_TOKEN")

# Константы для DTO
PROMOCODE_TYPE_ID = 80242
DISCOUNT_PERCENT = 100
BLOCK_STATUS = 0
SIZE = 1