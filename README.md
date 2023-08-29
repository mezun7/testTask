# Тестовое задание
## Деплой проекта
1. Необходим python версии 3.11
2. Необходимо установить poetry при помощи pip
    ```bash
    pip install poetry
    ```
3. Необходимо установить все зависимости при помощи poetry
    ```bash
    poetry install
    ```
4. Необходимо скопировать dist.env в .env
    ```bash
    cp dist.env .env 
    ```
5. В .env прописать настройки подключения к бд

## Перед первым запуском
Перед первым запуском нужно запустить `import_data.py` в консоли спросит путь до файла json для импорта данных

## Запуск проекта
Запускаем `main.py` в консоли спросит идентификатор сотрудника и выведет необходимые данные 