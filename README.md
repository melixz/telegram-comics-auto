# telegram-comics-auto


Проект позволяет автоматически скачивать комиксы XKCD и публиковать их в Telegram-канал с заданной периодичностью. 

### Как установить

1. Скачайте репозиторий с проектом:
    ```sh
    git clone https://github.com/melixz/telegram-comics-auto
    ```

2. Создайте файл `.env` в корневой директории проекта и добавьте следующие строки:
    ```env
    TELEGRAM_BOT_TOKEN=ваш_токен_бота_от_Telegram
    TELEGRAM_CHANNEL_ID=ваш_идентификатор_канала_Telegram
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

### Использование

1. Загрузите комиксы XKCD последовательно:
    ```sh
    python get_comics.py --start_num 1 --end_num 3539
    ```

2. Запустите скрипт для публикации комиксов в Telegram-канал:
    ```sh
    python comics_post_to_telegram.py comics --delay 14400
    ```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
