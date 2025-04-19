import os
import logging
import psycopg2
from psycopg2.extras import DictCursor
from config import PG_CONNECTION_PARAMS, TABLE_NAME

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        """
        Инициализация параметров подключения к базе данных
        """
        self.connection_params = PG_CONNECTION_PARAMS
        self.table_name = TABLE_NAME
        self.conn = None

    def connect(self):
        """
        Устанавливает соединение с PostgreSQL
        
        Returns:
            bool: True если подключение успешно, False в противном случае
        """
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к PostgreSQL: {str(e)}")
            return False

    def ensure_table_schema(self):
        """
        Создает таблицу если она не существует
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        path TEXT PRIMARY KEY,
                        is_nude BOOLEAN,
                        has_face BOOLEAN,
                        hash_sha256 TEXT,
                        clip_nude_score REAL,
                        nsfw_score REAL,
                        is_small BOOLEAN,
                        status TEXT,
                        phash TEXT,
                        shooting_date TIMESTAMP,
                        modification_date TIMESTAMP
                    )
                """)
                self.conn.commit()
                logger.info("✅ Схема таблицы проверена/создана")
        except Exception as e:
            logger.error(f"❌ Ошибка при создании схемы: {str(e)}")
            self.conn.rollback()

    def insert_or_update_photo(self, photo_data):
        """
        Вставляет или обновляет информацию о фото
        
        Args:
            photo_data (dict): Данные о фото
            
        Returns:
            bool: True если операция успешна, False в противном случае
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO {self.table_name} (
                        path, is_nude, has_face, hash_sha256,
                        clip_nude_score, nsfw_score, is_small,
                        status, phash, shooting_date, modification_date
                    ) VALUES (
                        %(path)s, %(is_nude)s, %(has_face)s, %(hash_sha256)s,
                        %(clip_nude_score)s, %(nsfw_score)s, %(is_small)s,
                        %(status)s, %(phash)s, %(shooting_date)s, %(modification_date)s
                    )
                    ON CONFLICT (path) DO UPDATE SET
                        is_nude = EXCLUDED.is_nude,
                        has_face = EXCLUDED.has_face,
                        hash_sha256 = EXCLUDED.hash_sha256,
                        clip_nude_score = EXCLUDED.clip_nude_score,
                        nsfw_score = EXCLUDED.nsfw_score,
                        is_small = EXCLUDED.is_small,
                        status = EXCLUDED.status,
                        phash = EXCLUDED.phash,
                        shooting_date = EXCLUDED.shooting_date,
                        modification_date = EXCLUDED.modification_date
                """, photo_data)
                self.conn.commit()
                return True
        except Exception as e:
            logger.error(f"❌ Ошибка при вставке/обновлении фото: {str(e)}")
            self.conn.rollback()
            return False

    def get_photo_by_path(self, path):
        """
        Получает информацию о фото по пути
        
        Args:
            path (str): Путь к файлу
            
        Returns:
            dict: Данные о фото или None если фото не найдено
        """
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(f"""
                    SELECT * FROM {self.table_name}
                    WHERE path = %s
                """, (path,))
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"❌ Ошибка при получении фото: {str(e)}")
            return None

    def get_all_photos(self):
        """
        Получение всех фото из базы данных
        
        Returns:
            list: список словарей с данными о фото
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            
            if rows:
                # Получаем имена колонок
                columns = [desc[0] for desc in cursor.description]
                # Создаем список словарей с данными
                return [dict(zip(columns, row)) for row in rows]
            return []
            
        except Exception as e:
            logger.error(f"❌ Ошибка при получении списка фото: {str(e)}")
            return []

    def close(self):
        """
        Закрывает соединение с базой данных
        """
        if self.conn:
            self.conn.close()
            self.conn = None 