import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Пути к файлам и директориям
PHOTO_DIR = os.getenv('PHOTO_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), "photos")))
REVIEW_DIR = os.getenv('REVIEW_DIR', "review")
LOG_DIR = os.getenv('LOG_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), "logs")))

# Параметры PostgreSQL
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'DB')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Passw0rd')

# Параметры базы данных
TABLE_NAME = os.getenv('TABLE_NAME', "photos_ok")

# Пороговые значения для классификации
NSFW_THRESHOLD = float(os.getenv('NSFW_THRESHOLD', "0.8"))
CLIP_THRESHOLD = float(os.getenv('CLIP_THRESHOLD', "0.8"))
MIN_IMAGE_SIZE = int(os.getenv('MIN_IMAGE_SIZE', "1500"))  # минимальный размер изображения (ширина или высота)
MAX_IMAGE_SIZE = int(os.getenv('MAX_IMAGE_SIZE', "10000"))  # максимальный размер изображения (ширина или высота)

# Параметры многопоточности
MAX_WORKERS = min(4, os.cpu_count())  # Ограничиваем количество процессов

# Статусы фотографий
STATUS_REVIEW = "review"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_PUBLISHED = "published"

# Параметры подключения к PostgreSQL в виде словаря
PG_CONNECTION_PARAMS = {
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT,
    'database': POSTGRES_DB,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD
} 