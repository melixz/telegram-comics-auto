import os
import requests
import argparse
from common import download_image, get_file_extension_from_url


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


def main():
    parser = argparse.ArgumentParser(description='Загрузить комиксы XKCD последовательно')
    parser.add_argument('--start_num', type=int, default=1, help='Начальный номер комикса XKCD')
    parser.add_argument('--end_num', type=int, default=3539, help='Последний номер комикса XKCD')
    args = parser.parse_args()

    os.makedirs('comics', exist_ok=True)

    for comic_number in range(args.start_num, args.end_num + 1):
        alt_text, image_url = fetch_xkcd_comic(comic_number)
        print(alt_text)
        saved_path = save_xkcd_comic(image_url, comic_number)
        print(f"Комикс сохранен как {saved_path}")


if __name__ == '__main__':
    main()
