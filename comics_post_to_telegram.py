import os
import requests
from dotenv import load_dotenv
import telebot
import random
from requests.exceptions import HTTPError, RequestException

MIN_COMIC_NUMBER = 1
MAX_COMIC_NUMBER = 2957


def fetch_xkcd_comic():
    comic_number = random.randint(MIN_COMIC_NUMBER, MAX_COMIC_NUMBER)
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as e:
        print(f"HTTP ошибка при получении данных с {url}: {e}")
        return None, None
    except RequestException as e:
        print(f"Ошибка запроса при получении данных с {url}: {e}")
        return None, None

    comic_data = response.json()
    image_url = comic_data['img']
    return comic_data['alt'], image_url


def send_image(bot, chat_id, image_url, caption):
    try:
        bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption)
    except telebot.apihelper.ApiException as e:
        print(f"Ошибка при отправке изображения {image_url}: {e}")


def post_images_to_telegram(bot, chat_id):
    alt_text, image_url = fetch_xkcd_comic()
    if image_url is None:
        print("Не удалось получить данные комикса")
        return
    send_image(bot, chat_id, image_url, alt_text)


def main():
    load_dotenv()
    try:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        chat_id = os.environ['TELEGRAM_CHANNEL_ID']
    except KeyError as e:
        raise ValueError(f"Переменная окружения {e} не установлена")

    bot = telebot.TeleBot(token)
    post_images_to_telegram(bot, chat_id)


if __name__ == '__main__':
    main()
