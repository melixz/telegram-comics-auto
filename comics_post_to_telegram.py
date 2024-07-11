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
            raise ValueError("Тестовое исключение для проверки удаления файла")
    finally:
        delete_file(image_path)


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Файл {file_path} был успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")


async def post_images_to_telegram(directory, delay):
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")

    if not token:
        raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена")

    if not chat_id:
        raise ValueError("Переменная окружения TELEGRAM_CHANNEL_ID не установлена")

    bot = telegram.Bot(token)

    async with bot:
        while True:
            images = get_image_files(directory)

            for image_path in images:
                await send_image(bot, chat_id, image_path)
                await asyncio.sleep(delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Публиковать фотографии в Telegram-канал с заданной периодичностью')
    parser.add_argument('directory', type=str, help='Директория с фотографиями')
    parser.add_argument('--delay', type=int, default=14400,
                        help='Задержка между публикациями в секундах (по умолчанию 4 часа)')

    args = parser.parse_args()

    asyncio.run(post_images_to_telegram(args.directory, args.delay))
