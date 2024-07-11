import os
import requests
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


def main():
    url = "http://example.com/image.jpg"
    save_path = "downloads/image.jpg"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    saved_path = download_image(url, save_path)
    print(f"Изображение сохранено как {saved_path}")


if __name__ == "__main__":
    main()
