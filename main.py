import os
import requests
import argparse
from common import download_image, get_file_extension_from_url


def fetch_xkcd_comic(comic_num):
    url = f"https://xkcd.com/{comic_num}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    image_url = comic_data['img']
    return image_url


def save_xkcd_comic(image_url, folder_name='comics'):
    extension = get_file_extension_from_url(image_url)
    save_path = os.path.join(folder_name, f'xkcd_comic{extension}')
    download_image(image_url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить комикс XKCD по номеру')
    parser.add_argument('--comic_num', type=int, default=353, help='Номер комикса XKCD')
    args = parser.parse_args()

    image_url = fetch_xkcd_comic(args.comic_num)
    save_xkcd_comic(image_url)


if __name__ == '__main__':
    main()
