import os
import requests
import argparse


def fetch_xkcd_comic(comic_num):
    url = f"https://xkcd.com/{comic_num}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    image_url = comic_data['img']
    return image_url


def save_xkcd_comic(image_url, folder_name='comics'):
    os.makedirs(folder_name, exist_ok=True)
    response = requests.get(image_url)
    with open(os.path.join(folder_name, 'xkcd_comic.jpg'), 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(description='Загрузить комикс XKCD по номеру')
    parser.add_argument('--comic_num', type=int, default=353, help='Номер комикса XKCD')
    args = parser.parse_args()

    image_url = fetch_xkcd_comic(args.comic_num)
    save_xkcd_comic(image_url)


if __name__ == '__main__':
    main()
