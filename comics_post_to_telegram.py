import os
import argparse
from dotenv import load_dotenv
import telegram
import asyncio


def get_image_files(directory):
    return sorted([os.path.join(directory, file) for file in os.listdir(directory) if
                   os.path.isfile(os.path.join(directory, file))])


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


async def post_images_to_telegram(directory):
    load_dotenv()
    try:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        chat_id = os.environ['TELEGRAM_CHANNEL_ID']
    except KeyError as e:
        raise ValueError(f"Переменная окружения {e} не установлена")

    bot = telegram.Bot(token)

    async with bot:
        images = get_image_files(directory)
        if images:
            image_path = images[0]
            try:
                await send_image(bot, chat_id, image_path)
            except Exception as e:
                print(f"Ошибка при отправке изображения {image_path}: {e}")
        else:
            print("В директории нет изображений для публикации.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Публиковать одно фото из директории в Telegram-канал')
    parser.add_argument('directory', type=str, help='Директория с фотографиями')

    args = parser.parse_args()

    asyncio.run(post_images_to_telegram(args.directory))
