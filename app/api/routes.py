from flask import jsonify
from app.api import bp
from app.photo_tree import PhotoTree
from app.database import Database

@bp.route('/tree')
def get_tree():
    db = Database()
    if not db.connect():
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        tree = PhotoTree(db, base_path="/mnt/smb/OneDrive/Pictures/!Фотосессии")
        tree.build_tree()
        return jsonify(tree.tree)
    finally:
        db.close()

@bp.route('/photos/<path:directory>')
def get_photos(directory):
    db = Database()
    if not db.connect():
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        tree = PhotoTree(db, base_path="/mnt/smb/OneDrive/Pictures/!Фотосессии")
        tree.build_tree()
        contents = tree.get_directory_contents(directory)
        if contents is None:
            return jsonify({'error': 'Directory not found'}), 404
        return jsonify(contents)
    finally:
        db.close() 