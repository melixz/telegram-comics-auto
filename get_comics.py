import os
import requests
import argparse
from common import download_image, get_file_extension_from_url
import random


def fetch_xkcd_comic(random_number):
    url = f"https://xkcd.com/{random_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    print(comic_data['alt'])
    image_url = comic_data['img']
    return image_url


def save_xkcd_comic(image_url, folder_name='comics'):
    extension = get_file_extension_from_url(image_url)
    save_path = os.path.join(folder_name, f'xkcd_comic{extension}')
    download_image(image_url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить случайный комикс XKCD')
    parser.add_argument('--max_num', type=int, default=3539, help='Максимальный номер комикса XKCD')
    args = parser.parse_args()

    random_number = random.randint(1, args.max_num)
    image_url = fetch_xkcd_comic(random_number)
    save_xkcd_comic(image_url)


if __name__ == '__main__':
    main()
