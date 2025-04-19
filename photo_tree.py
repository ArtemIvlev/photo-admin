import os
from collections import defaultdict
from typing import Dict, List, Optional
from database import Database

class PhotoTree:
    def __init__(self, db: Database, base_path: str = ""):
        """
        Инициализация дерева фотографий
        
        Args:
            db (Database): Экземпляр класса Database для работы с БД
            base_path (str): Базовый путь, который будет пропущен при построении дерева
        """
        self.db = db
        self.base_path = os.path.normpath(base_path) if base_path else ""
        self.tree: Dict[str, Dict] = {"files": [], "dirs": {}}
        
    def _split_path(self, path: str) -> List[str]:
        """
        Разбивает путь на компоненты, пропуская базовый путь
        
        Args:
            path (str): Путь к файлу
            
        Returns:
            List[str]: Список компонентов пути
        """
        # Нормализуем путь и разбиваем на компоненты
        normalized_path = os.path.normpath(path)
        
        # Если есть базовый путь, убираем его из начала
        if self.base_path and normalized_path.startswith(self.base_path):
            normalized_path = normalized_path[len(self.base_path):].lstrip(os.sep)
            
        parts = normalized_path.split(os.sep)
        # Убираем пустые компоненты и точку в начале пути
        return [p for p in parts if p and p != '.']
        
    def build_tree(self) -> Dict:
        """
        Строит дерево путей из базы данных
        
        Returns:
            Dict: Дерево путей
        """
        # Получаем все фото из базы
        photos = self.db.get_all_photos()
        
        # Очищаем текущее дерево
        self.tree = {"files": [], "dirs": {}}
        
        # Строим дерево
        for photo in photos:
            path = photo['path']
            parts = self._split_path(path)
            
            # Текущий узел дерева
            current = self.tree
            
            # Проходим по всем компонентам пути
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # Это файл
                    current['files'].append({
                        'path': path,
                        'is_nude': photo['is_nude'],
                        'has_face': photo['has_face'],
                        'status': photo['status'],
                        'nsfw_score': photo['nsfw_score']
                    })
                else:
                    # Это директория
                    if part not in current['dirs']:
                        current['dirs'][part] = {"files": [], "dirs": {}}
                    current = current['dirs'][part]
        
        return self.tree
    
    def get_directory_contents(self, path: str) -> Optional[Dict]:
        """
        Получает содержимое указанной директории
        
        Args:
            path (str): Путь к директории
            
        Returns:
            Optional[Dict]: Содержимое директории или None если директория не найдена
        """
        parts = self._split_path(path)
        current = self.tree
        
        # Проходим по дереву до нужной директории
        for part in parts:
            if part not in current['dirs']:
                return None
            current = current['dirs'][part]
            
        return {
            'files': current['files'],
            'directories': list(current['dirs'].keys())
        }
    
    def get_file_info(self, path: str) -> Optional[Dict]:
        """
        Получает информацию о файле
        
        Args:
            path (str): Путь к файлу
            
        Returns:
            Optional[Dict]: Информация о файле или None если файл не найден
        """
        parts = self._split_path(path)
        if not parts:
            return None
            
        # Получаем директорию, содержащую файл
        dir_path = os.path.dirname(path)
        dir_contents = self.get_directory_contents(dir_path)
        
        if not dir_contents:
            return None
            
        # Ищем файл в списке файлов директории
        filename = os.path.basename(path)
        for file_info in dir_contents['files']:
            if os.path.basename(file_info['path']) == filename:
                return file_info
                
        return None
    
    def get_statistics(self) -> Dict:
        """
        Получает статистику по дереву
        
        Returns:
            Dict: Статистика
        """
        def count_recursive(node: Dict) -> Dict:
            stats = {
                'total_files': len(node['files']),
                'nude_files': sum(1 for f in node['files'] if f['is_nude']),
                'face_files': sum(1 for f in node['files'] if f['has_face']),
                'by_status': defaultdict(int),
                'directories': 0
            }
            
            # Считаем файлы по статусам
            for file_info in node['files']:
                stats['by_status'][file_info['status']] += 1
                
            # Рекурсивно обрабатываем поддиректории
            for dir_name, dir_node in node['dirs'].items():
                dir_stats = count_recursive(dir_node)
                stats['total_files'] += dir_stats['total_files']
                stats['nude_files'] += dir_stats['nude_files']
                stats['face_files'] += dir_stats['face_files']
                stats['directories'] += 1 + dir_stats['directories']
                
                # Объединяем статистику по статусам
                for status, count in dir_stats['by_status'].items():
                    stats['by_status'][status] += count
                    
            return stats
            
        return count_recursive(self.tree) 