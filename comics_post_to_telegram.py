import os
import requests
import asyncio
from dotenv import load_dotenv
import telegram
import random


def fetch_xkcd_comic():
    comic_number = random.randint(1, 2957)
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    image_url = comic_data['img']
    return comic_data['alt'], image_url


async def send_image(bot, chat_id, image_url, caption):
    await bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption)


async def post_images_to_telegram(bot, chat_id):
    alt_text, image_url = fetch_xkcd_comic()
    print(alt_text)
    await send_image(bot, chat_id, image_url, alt_text)


def main():
    load_dotenv()
    try:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        chat_id = os.environ['TELEGRAM_CHANNEL_ID']
    except KeyError as e:
        raise ValueError(f"Переменная окружения {e} не установлена")

    bot = telegram.Bot(token)

    try:
        asyncio.run(post_images_to_telegram(bot, chat_id))
    except Exception as e:
        print(f"Ошибка при отправке изображения: {e}")
        exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Ошибка в main: {e}")
        exit(1)
