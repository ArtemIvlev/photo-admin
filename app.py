from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS
from database import Database
from photo_tree import PhotoTree
from config import TABLE_NAME
import json
import requests
import os
import io
import logging
from PIL import Image
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Включаем режим отладки Flask
app.debug = True

# Настраиваем логирование Flask
if not app.debug:
    file_handler = logging.FileHandler('flask.log')
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

# Загружаем версию из package.json
with open('package.json', 'r') as f:
    package_data = json.load(f)
    version = package_data.get('version', '1.0.0')

# Создаем таблицу photos, если она не существует
def create_photos_table():
    db = Database()
    if db.connect():
        try:
            db.ensure_table_schema()  # Используем метод из класса Database
            print("✅ Таблица успешно создана или уже существует")
        except Exception as e:
            print(f"❌ Ошибка при создании таблицы: {str(e)}")
        finally:
            db.close()
    else:
        print("❌ Ошибка подключения к базе данных при создании таблицы")

# Создаем таблицу при запуске приложения
create_photos_table()

@app.route('/')
def index():
    return render_template('index.html', version=version)

@app.route('/api/tree')
def get_tree():
    logger.debug("Получен запрос на получение дерева")
    db = Database()
    if not db.connect():
        logger.error("Ошибка подключения к базе данных")
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
    try:
        tree = PhotoTree(db)
        tree.build_tree()
        logger.debug("Дерево успешно построено")
        return jsonify(tree.tree)
    except Exception as e:
        logger.error(f"Ошибка при построении дерева: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/thumbnail/<path:photo_path>')
def get_thumbnail(photo_path):
    # Обрабатываем путь, чтобы получить миниатюру
    # Ищем позицию "Pictures/!Фотосессии" в пути
    target_prefix = "Pictures/!Фотосессии"
    processed_path = photo_path
    
    # Удаляем префикс /mnt/smb/OneDrive из пути
    if photo_path.startswith('/mnt/smb/OneDrive/'):
        processed_path = photo_path[len('/mnt/smb/OneDrive/'):]
    elif photo_path.startswith('mnt/smb/OneDrive/'):
        processed_path = photo_path[len('mnt/smb/OneDrive/'):]
    
    # Находим позицию "Pictures/!Фотосессии" в обработанном пути
    target_index = processed_path.find(target_prefix)
    
    # Если нашли, откусываем путь до "Pictures/!Фотосессии"
    if target_index != -1:
        processed_path = processed_path[target_index:]
    
    # Формируем URL для запроса к pigallery2
    thumbnail_url = f"https://gallery.homoludens.photos/pgapi/gallery/content/{processed_path}/thumbnail/480"
    
    # Добавляем заголовки авторизации, если они нужны
    headers = {
        'Authorization': 'Bearer your-auth-token',  # Замените на реальный токен
        'User-Agent': 'PhotoAdmin/1.0'
    }
    
    try:
        # Делаем запрос к pigallery2
        response = requests.get(thumbnail_url, headers=headers, stream=True)
        
        # Проверяем статус ответа
        if response.status_code == 200:
            # Возвращаем изображение
            return send_file(
                response.raw,
                mimetype=response.headers.get('Content-Type', 'image/jpeg')
            )
        else:
            # Если запрос не удался, возвращаем ошибку
            return jsonify({
                'error': f'Ошибка получения миниатюры: {response.status_code}',
                'url': thumbnail_url
            }), response.status_code
    except Exception as e:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        return jsonify({
            'error': f'Ошибка при запросе к pigallery2: {str(e)}',
            'url': thumbnail_url
        }), 500

@app.route('/api/photo/<path:photo_path>')
def get_photo(photo_path):
    logger.debug(f"Получен запрос на получение фото: {photo_path}")
    
    # Декодируем путь и добавляем начальный слеш, если его нет
    photo_path = request.view_args['photo_path']
    if not photo_path.startswith('/'):
        photo_path = '/' + photo_path
    logger.debug(f"Декодированный путь: {photo_path}")
    
    # Проверяем, существует ли файл
    if not os.path.exists(photo_path):
        logger.warning(f"Файл не найден на диске: {photo_path}")
        return jsonify({
            'error': f'Файл не найден: {photo_path}',
            'path': photo_path
        }), 404
    
    # Отдаем файл
    try:
        logger.debug(f"Отправляем файл: {photo_path}")
        
        # Открываем изображение с помощью Pillow
        with Image.open(photo_path) as img:
            # Получаем размеры изображения
            width, height = img.size
            
            # Вычисляем новые размеры (уменьшаем на треть)
            new_width = width // 3
            new_height = height // 3
            
            # Изменяем размер изображения
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Сохраняем в буфер с качеством 85%
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=85, optimize=True)
            output_buffer.seek(0)
            
            logger.debug(f"Изображение уменьшено с {width}x{height} до {new_width}x{new_height}")
            
            # Отправляем файл клиенту
            return send_file(
                output_buffer,
                mimetype='image/jpeg',
                as_attachment=False
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        return jsonify({
            'error': f'Ошибка при отправке файла: {str(e)}',
            'path': photo_path
        }), 500

@app.route('/api/update_statuses', methods=['POST'])
def update_statuses():
    print("\n=== НАЧАЛО ОБНОВЛЕНИЯ СТАТУСОВ ===")
    print(f"Время: {datetime.now()}")
    
    try:
        data = request.json
        print(f"\nПолученные данные:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if not data or 'updates' not in data:
            print("ОШИБКА: Неверный формат данных - отсутствует ключ 'updates'")
            return jsonify({'error': 'Неверный формат данных'}), 400
        
        updates = data['updates']
        print(f"\nКоличество обновлений: {len(updates)}")
        
        if not isinstance(updates, list):
            print(f"ОШИБКА: updates должен быть списком, получено: {type(updates)}")
            return jsonify({'error': 'Неверный формат данных: updates должен быть списком'}), 400
        
        db = Database()
        if not db.connect():
            print("ОШИБКА: Не удалось подключиться к базе данных")
            return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
        try:
            cursor = db.conn.cursor()
            print("\nНачало обработки обновлений...")
            print(f"Используется таблица: {TABLE_NAME}")
            
            # Обновляем статусы фотографий
            for i, update in enumerate(updates):
                if 'path' not in update or 'status' not in update:
                    print(f"Пропущено обновление {i+1}: отсутствуют обязательные поля")
                    continue
                
                path = update['path']
                status = update['status']
                print(f"\nОбработка обновления {i+1}:")
                print(f"Путь: {path}")
                print(f"Новый статус: {status}")
                
                # Проверяем, существует ли запись для этого пути
                cursor.execute(f"SELECT path, status FROM {TABLE_NAME} WHERE path = %s", (path,))
                result = cursor.fetchone()
                
                if result:
                    old_status = result[1]
                    print(f"Найдена существующая запись:")
                    print(f"Путь: {result[0]}")
                    print(f"Старый статус: {old_status}")
                    print(f"Новый статус: {status}")
                    
                    cursor.execute(
                        f"UPDATE {TABLE_NAME} SET status = %s WHERE path = %s",
                        (status, path)
                    )
                    print("Запись обновлена")
                else:
                    print("Создание новой записи...")
                    cursor.execute(
                        f"INSERT INTO {TABLE_NAME} (path, status) VALUES (%s, %s)",
                        (path, status)
                    )
                    print("Новая запись создана")
            
            db.conn.commit()
            print("\nВсе изменения сохранены в базе данных")
            
            # Проверяем, что изменения действительно сохранились
            print("\nПроверка сохраненных изменений:")
            cursor.execute(f"SELECT path, status FROM {TABLE_NAME} WHERE path IN %s", 
                          (tuple(update['path'] for update in updates if 'path' in update),))
            saved_updates = cursor.fetchall()
            for path, status in saved_updates:
                print(f"Путь: {path}")
                print(f"Статус: {status}")
                print("---")
            
            print("\n=== ОБНОВЛЕНИЕ СТАТУСОВ ЗАВЕРШЕНО ===\n")
            
            return jsonify({
                'success': True,
                'message': f'Успешно обновлено {len(updates)} статусов фотографий',
                'updated_count': len(updates),
                'saved_updates': [{'path': path, 'status': status} for path, status in saved_updates]
            })
        except Exception as e:
            db.conn.rollback()
            print(f"\nОШИБКА при обновлении статусов: {str(e)}")
            return jsonify({'error': f'Ошибка при обновлении статусов: {str(e)}'}), 500
        finally:
            db.close()
    except Exception as e:
        print(f"\nОШИБКА при обработке запроса: {str(e)}")
        return jsonify({'error': f'Ошибка при обработке запроса: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 