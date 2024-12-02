
# File Sharing Service

### Описание
Простое приложение для загрузки и скачивания файлов с использованием FastAPI.

### Установка и запуск

1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

2. Запустите сервер:
   ```
   uvicorn main:app --reload
   ```

3. Загрузка файла:
   - Метод: POST
   - URL: `/upload/`
   - Параметры: Передайте файл как form-data.

4. Скачивание файла:
   - Метод: GET
   - URL: `/download/{file_id}`
# my_uploader
