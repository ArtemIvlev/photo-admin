import React, { useState, useEffect } from 'react';
import './PhotoTree.css';

const PhotoTree = () => {
    const [tree, setTree] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedDir, setSelectedDir] = useState(null);

    useEffect(() => {
        const fetchTree = async () => {
            try {
                const response = await fetch('/api/tree');
                if (!response.ok) {
                    throw new Error('Ошибка при загрузке дерева');
                }
                const data = await response.json();
                // Находим директорию !Фотосессии
                const photoSessions = data?.dirs?.mnt?.dirs?.smb?.dirs?.OneDrive?.dirs?.Pictures?.dirs?.['!Фотосессии'];
                if (!photoSessions) {
                    throw new Error('Директория !Фотосессии не найдена');
                }
                setTree(photoSessions);
                setError(null);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTree();
    }, []);

    const handleDirClick = (path) => {
        console.log('PhotoTree: handleDirClick', path);
        setSelectedDir(path);

        // Находим выбранную директорию и её файлы
        let currentNode = tree;
        const pathParts = path.split('/').filter(Boolean);
        
        for (const part of pathParts) {
            if (part && currentNode.dirs && currentNode.dirs[part]) {
                currentNode = currentNode.dirs[part];
            }
        }

        // Генерируем событие для PhotoGrid с файлами
        const event = new CustomEvent('directorySelected', { 
            detail: { 
                path,
                files: currentNode.files || [] 
            } 
        });
        console.log('PhotoTree: dispatching event with files', event.detail);
        document.dispatchEvent(event);
    };

    const getDirectoryStats = (node) => {
        const stats = {
            total: 0,
            nude: 0,
            face: 0
        };

        if (node.files) {
            stats.total = node.files.length;
            stats.nude = node.files.filter(f => f.is_nude).length;
            stats.face = node.files.filter(f => f.has_face).length;
        }

        return stats;
    };

    const renderNode = (node, dirName = '', parentPath = '') => {
        const stats = getDirectoryStats(node);
        const currentPath = parentPath ? `${parentPath}/${dirName}` : dirName;
        
        return (
            <div key={currentPath} className="tree-node">
                <div className="directory">
                    {dirName && (
                        <div 
                            className={`directory-name ${selectedDir === currentPath ? 'selected' : ''}`}
                            onClick={() => handleDirClick(currentPath)}
                        >
                            {dirName}
                            <span className="directory-stats">
                                ({stats.total} фото, {stats.nude} ню, {stats.face} с лицами)
                            </span>
                        </div>
                    )}
                    {node.dirs && Object.entries(node.dirs).length > 0 && (
                        <div className="directories">
                            {Object.entries(node.dirs).map(([name, dir]) => renderNode(dir, name, currentPath))}
                        </div>
                    )}
                </div>
            </div>
        );
    };

    if (loading) {
        return <div className="loading">Загрузка дерева фотографий...</div>;
    }

    if (error) {
        return <div className="error">Ошибка: {error}</div>;
    }

    if (!tree) {
        return <div className="empty">Дерево фотографий пусто</div>;
    }

    return (
        <div className="photo-tree">
            <h2>Фотосессии</h2>
            {renderNode(tree)}
            {selectedDir && (
                <div className="selected-directory">
                    <h3>Выбрана директория: {selectedDir}</h3>
                </div>
            )}
        </div>
    );
};

export default PhotoTree; 