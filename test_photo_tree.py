import os
import logging
from database import Database
from photo_tree import PhotoTree

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_photo_tree():
    """
    Тестирование класса PhotoTree
    """
    # Создаем экземпляр базы данных
    db = Database()
    
    # Подключаемся к базе данных
    if not db.connect():
        logger.error("❌ Не удалось подключиться к базе данных")
        return
        
    try:
        # Получаем все фото из базы для отладки
        photos = db.get_all_photos()
        logger.info(f"📸 Получено фотографий из базы: {len(photos)}")
        if photos:
            logger.info("Пример первой записи:")
            logger.info(photos[0])
        
        # Создаем экземпляр дерева
        tree = PhotoTree(db, base_path="/mnt/smb/OneDrive/Pictures/!Фотосессии")
        
        # Строим дерево
        logger.info("🔄 Строим дерево путей...")
        tree.build_tree()
        
        # Получаем статистику
        logger.info("📊 Получаем статистику...")
        stats = tree.get_statistics()
        logger.info(f"Статистика: {stats}")
        
        # Выводим структуру дерева
        def print_tree(node, level=0):
            indent = "  " * level
            for dir_name, dir_node in sorted(node['dirs'].items()):
                logger.info(f"{indent}📁 {dir_name}/")
                print_tree(dir_node, level + 1)
        
        logger.info("\nСтруктура дерева:")
        print_tree(tree.tree)
        
        # Проверяем получение содержимого директории
        if stats['directories'] > 0:
            # Берем первую директорию из дерева
            first_dir = next(iter(tree.tree['dirs'].keys()))
            logger.info(f"\n📂 Содержимое директории '{first_dir}':")
            contents = tree.get_directory_contents(first_dir)
            if contents:
                logger.info(f"Файлы: {len(contents['files'])}")
                logger.info(f"Поддиректории: {contents['directories']}")
        
        # Проверяем получение информации о файле
        if stats['total_files'] > 0:
            # Берем первый файл из дерева
            first_file = tree.tree['files'][0]['path'] if tree.tree['files'] else None
            if first_file:
                logger.info(f"\n📄 Информация о файле '{os.path.basename(first_file)}':")
                file_info = tree.get_file_info(first_file)
                if file_info:
                    logger.info(f"Путь: {file_info['path']}")
                    logger.info(f"Обнаженное содержание: {file_info['is_nude']}")
                    logger.info(f"Есть лица: {file_info['has_face']}")
                    logger.info(f"Статус: {file_info['status']}")
                    logger.info(f"NSFW score: {file_info['nsfw_score']}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при тестировании: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # Закрываем соединение
        db.close()
        logger.info("✅ Тестирование завершено")

if __name__ == "__main__":
    test_photo_tree() 