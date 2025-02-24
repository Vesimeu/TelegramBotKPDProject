import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime, timedelta
import aiohttp
import json
import logging
from config import BOT_TOKEN, API_TOKEN, API_ENDPOINT, PROMOCODE_TYPE_ID, DISCOUNT_PERCENT, BLOCK_STATUS, SIZE

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# DTO для запроса
def create_promocode_dto():
    now = datetime.now()
    return {
        "promocodetypeId": PROMOCODE_TYPE_ID,
        "promocodeDateBeg": now.isoformat(),
        "promocodeDateEnd": (now + timedelta(days=365)).isoformat(),
        "promocodeDiscountPercent": DISCOUNT_PERCENT,
        "promocodeBlock": BLOCK_STATUS,
        "size": SIZE,
    }

# Функция для запроса к API
async def get_promocode():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        try:
            logger.info("Отправка запроса к API для получения промокода")
            async with session.post(API_ENDPOINT, json=create_promocode_dto(), headers=headers) as response:
                if response.status == 200:
                    data = await response.text()
                    result = json.loads(data)
                    promocode = result["code"].split(",")[0]
                    logger.info(f"Успешно получен промокод: {promocode}")
                    return promocode
                else:
                    error_msg = f"Ошибка API: {response.status}"
                    logger.error(error_msg)
                    return error_msg
        except Exception as e:
            error_msg = f"Ошибка при запросе к API: {str(e)}"
            logger.error(error_msg)
            return error_msg

# Обработчик команды /дай
@dp.message_handler(commands=['дай'])
async def handle_give_command(message: types.Message):
    logger.info(f"Получена команда /дай от пользователя {message.from_user.id}")
    promocode = await get_promocode()
    await message.answer(f"Ваш промокод: {promocode}")
    logger.info(f"Ответ отправлен пользователю {message.from_user.id}")

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    await message.answer("Используй команду /дай чтобы получить промокод.")

# Запуск бота
if __name__ == '__main__':
    logger.info("Запускаем ОНО")
    executor.start_polling(dp, skip_updates=True)