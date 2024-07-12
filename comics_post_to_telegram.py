import os
import requests
import argparse
import asyncio
from dotenv import load_dotenv
import telegram
from urllib.parse import urlsplit, unquote


def download_image(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)
    return save_path


def get_file_extension_from_url(url):
    path = urlsplit(url).path
    filename = os.path.basename(unquote(path))
    _, extension = os.path.splitext(filename)
    return extension


def fetch_xkcd_comic(comic_number):
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    image_url = comic_data['img']
    return comic_data['alt'], image_url


def save_xkcd_comic(image_url, comic_number, folder_name='comics'):
    extension = get_file_extension_from_url(image_url)
    save_path = os.path.join(folder_name, f'xkcd_comic_{comic_number}{extension}')
    download_image(image_url, save_path)
    return save_path


async def send_image(bot, chat_id, image_path):
    try:
        with open(image_path, 'rb') as f:
            await bot.send_photo(chat_id=chat_id, photo=f)
    finally:
        delete_file(image_path)


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Файл {file_path} был успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")


async def post_images_to_telegram(image_path):
    load_dotenv()
    try:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        chat_id = os.environ['TELEGRAM_CHANNEL_ID']
    except KeyError as e:
        raise ValueError(f"Переменная окружения {e} не установлена")

    bot = telegram.Bot(token)

    async with bot:
        try:
            await send_image(bot, chat_id, image_path)
        except Exception as e:
            print(f"Ошибка при отправке изображения {image_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Загрузить и опубликовать комикс XKCD')
    parser.add_argument('comic_number', type=int, help='Номер комикса XKCD')
    args = parser.parse_args()

    os.makedirs('comics', exist_ok=True)

    comic_number = args.comic_number
    alt_text, image_url = fetch_xkcd_comic(comic_number)
    print(alt_text)
    saved_path = save_xkcd_comic(image_url, comic_number)
    print(f"Комикс сохранен как {saved_path}")

    asyncio.run(post_images_to_telegram(saved_path))


if __name__ == '__main__':
    main()
