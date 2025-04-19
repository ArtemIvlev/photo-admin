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
- Контейнеризация: Docker

## Установка

### Локальная установка

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

### Установка с использованием Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose

2. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
cd photo-admin
```

3. Создайте директорию для фотографий:
```bash
mkdir photos
```

4. Запустите приложение:
```bash
docker-compose up -d
```

## Запуск

### Локальный запуск

1. Запустите сервер Flask:
```bash
python app.py
```

2. В отдельном терминале запустите сборку фронтенда:
```bash
npm run build
```

3. Откройте http://localhost:5000 в браузере

### Запуск в Docker

1. Приложение будет доступно по адресу http://localhost:5000

2. Для просмотра логов:
```bash
docker-compose logs -f
```

3. Для остановки:
```bash
docker-compose down
```

## Разработка

### Локальная разработка

Для разработки используйте:
```bash
npm run dev
```

### Разработка в Docker

1. Запустите в режиме разработки:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

2. Для пересборки после изменений:
```bash
docker-compose build web
docker-compose up -d web
```

## Лицензия

MIT 