# Photo Admin

Веб-приложение для управления фотографиями с возможностью классификации и модерации.

## Возможности

- Просмотр структуры директорий с фотографиями
- Классификация фотографий (наличие лиц, NSFW контент)
- Модерация фотографий (одобрение/отклонение)
- Публикация фотографий
- Сортировка и фильтрация
- Предпросмотр фотографий

## Технологии

- Backend: Python, Flask
- Frontend: React
- База данных: PostgreSQL
- Обработка изображений: Pillow

## Установка

1. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
cd photo-admin
```

2. Установите зависимости Python:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Установите зависимости Node.js:
```bash
npm install
```

4. Создайте файл .env и настройте переменные окружения:
```env
PHOTO_DIR=/path/to/photos
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
```

## Запуск

1. Запустите сервер Flask:
```bash
python app.py
```

2. В отдельном терминале запустите сборку фронтенда:
```bash
npm run build
```

3. Откройте http://localhost:5000 в браузере

## Разработка

Для разработки используйте:
```bash
npm run dev
```

## Лицензия

MIT 