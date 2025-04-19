import React, { useState, useEffect } from 'react';
import './PhotoGrid.css';

const PhotoGrid = () => {
    const [photos, setPhotos] = useState([]);
    const [selectedPhotos, setSelectedPhotos] = useState(new Set());
    const [currentPath, setCurrentPath] = useState('');
    const [filterStatus, setFilterStatus] = useState('all');
    const [modifiedPhotos, setModifiedPhotos] = useState({});
    const [isSaving, setIsSaving] = useState(false);
    const [sortDirection, setSortDirection] = useState('asc'); // 'asc' или 'desc'

    useEffect(() => {
        const handleDirectorySelected = (event) => {
            setCurrentPath(event.detail.path);
            setPhotos(event.detail.files || []);
            setSelectedPhotos(new Set());
            setModifiedPhotos({}); // Сбрасываем изменения при смене директории
        };

        document.addEventListener('directorySelected', handleDirectorySelected);
        return () => {
            document.removeEventListener('directorySelected', handleDirectorySelected);
        };
    }, []);

    const getThumbnailUrl = (photoPath) => {
        return `/api/photo/${encodeURIComponent(photoPath)}`;
    };

    const togglePhotoSelection = (photoPath) => {
        setSelectedPhotos(prev => {
            const newSet = new Set(prev);
            if (newSet.has(photoPath)) {
                newSet.delete(photoPath);
            } else {
                newSet.add(photoPath);
            }
            return newSet;
        });
    };

    const getStatusLabel = (status) => {
        const labels = {
            'approved': '✅ Одобрено',
            'rejected': '❌ Отклонено',
            'pending': '⏳ На проверке',
            'normal': '📷 Обычное',
            'published': '🌐 Опубликовано'
        };
        return labels[status] || status;
    };

    const cyclePhotoStatus = (photoPath, currentStatus, e) => {
        e.stopPropagation(); // Предотвращаем всплытие события клика
        
        // Определяем следующий статус в цикле
        const statusCycle = ['normal', 'pending', 'approved', 'rejected', 'published'];
        const currentIndex = statusCycle.indexOf(currentStatus);
        const nextIndex = (currentIndex + 1) % statusCycle.length;
        const nextStatus = statusCycle[nextIndex];
        
        // Обновляем статус в локальном состоянии
        setModifiedPhotos(prev => ({
            ...prev,
            [photoPath]: nextStatus
        }));
        
        // Обновляем фотографии в состоянии
        setPhotos(prevPhotos => 
            prevPhotos.map(photo => 
                photo.path === photoPath 
                    ? { ...photo, status: nextStatus } 
                    : photo
            )
        );
        
        console.log(`Статус фото ${photoPath} изменен с ${currentStatus} на ${nextStatus}`);
    };

    const getPhotoStatus = (photo) => {
        // Возвращаем измененный статус, если он есть, иначе оригинальный
        return modifiedPhotos[photo.path] || photo.status;
    };

    const saveChanges = async () => {
        if (Object.keys(modifiedPhotos).length === 0) {
            return; // Нет изменений для сохранения
        }

        setIsSaving(true);
        try {
            const response = await fetch('/api/update_statuses', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    updates: Object.entries(modifiedPhotos).map(([path, status]) => ({
                        path,
                        status
                    }))
                }),
            });

            if (!response.ok) {
                throw new Error('Ошибка при сохранении изменений');
            }

            const result = await response.json();
            console.log('Изменения успешно сохранены:', result);
            
            // Очищаем список изменений после успешного сохранения
            setModifiedPhotos({});
            
            // Обновляем фотографии с новыми статусами из базы
            const updatedPhotos = photos.map(photo => {
                if (modifiedPhotos[photo.path]) {
                    return { ...photo, status: modifiedPhotos[photo.path] };
                }
                return photo;
            });
            setPhotos(updatedPhotos);
            
            alert('Изменения успешно сохранены!');
        } catch (error) {
            console.error('Ошибка при сохранении изменений:', error);
            alert('Ошибка при сохранении изменений: ' + error.message);
        } finally {
            setIsSaving(false);
        }
    };

    const toggleSort = () => {
        setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    };

    const getSortedPhotos = (photosToSort) => {
        return [...photosToSort].sort((a, b) => {
            const nameA = a.path.split('/').pop().toLowerCase();
            const nameB = b.path.split('/').pop().toLowerCase();
            return sortDirection === 'asc' 
                ? nameA.localeCompare(nameB)
                : nameB.localeCompare(nameA);
        });
    };

    const filteredPhotos = filterStatus === 'all' 
        ? photos 
        : photos.filter(photo => getPhotoStatus(photo) === filterStatus);

    const sortedPhotos = getSortedPhotos(filteredPhotos);

    const hasChanges = Object.keys(modifiedPhotos).length > 0;

    return (
        <div className="photo-grid-container">
            <div className="filters-container">
                <button 
                    className={`filter-button ${filterStatus === 'all' ? 'active' : ''}`}
                    onClick={() => setFilterStatus('all')}
                >
                    Все
                </button>
                <button 
                    className={`filter-button ${filterStatus === 'approved' ? 'active' : ''}`}
                    onClick={() => setFilterStatus('approved')}
                >
                    Одобренные
                </button>
                <button 
                    className={`filter-button ${filterStatus === 'rejected' ? 'active' : ''}`}
                    onClick={() => setFilterStatus('rejected')}
                >
                    Отклоненные
                </button>
                <button 
                    className={`filter-button ${filterStatus === 'pending' ? 'active' : ''}`}
                    onClick={() => setFilterStatus('pending')}
                >
                    На проверке
                </button>
                <button 
                    className={`filter-button ${filterStatus === 'normal' ? 'active' : ''}`}
                    onClick={() => setFilterStatus('normal')}
                >
                    Обычные
                </button>
                <button 
                    className={`filter-button ${filterStatus === 'published' ? 'active' : ''}`}
                    onClick={() => setFilterStatus('published')}
                >
                    Опубликованные
                </button>
                
                <button 
                    className="sort-button"
                    onClick={toggleSort}
                >
                    Сортировка {sortDirection === 'asc' ? '↑' : '↓'}
                </button>
                
                {hasChanges && (
                    <button 
                        className="save-button"
                        onClick={saveChanges}
                        disabled={isSaving}
                    >
                        {isSaving ? 'Сохранение...' : 'Применить изменения'}
                    </button>
                )}
            </div>

            {sortedPhotos.length === 0 ? (
                <div className="no-photos">
                    Нет фотографий в этой директории
                </div>
            ) : (
                <div className="photo-grid">
                    {sortedPhotos.map(photo => {
                        const currentStatus = getPhotoStatus(photo);
                        return (
                            <div 
                                key={photo.path}
                                className={`photo-preview ${selectedPhotos.has(photo.path) ? 'selected' : ''}`}
                                onClick={() => togglePhotoSelection(photo.path)}
                            >
                                <img 
                                    src={getThumbnailUrl(photo.path)}
                                    alt={photo.path.split('/').pop()}
                                    loading="lazy"
                                    onError={(e) => {
                                        e.target.src = '/static/img/error-placeholder.png';
                                    }}
                                />
                                <div className="photo-info">
                                    <div className="photo-name">
                                        {photo.path.split('/').pop()}
                                    </div>
                                    <div 
                                        className={`photo-status ${currentStatus}`}
                                        onClick={(e) => cyclePhotoStatus(photo.path, currentStatus, e)}
                                    >
                                        {getStatusLabel(currentStatus)}
                                    </div>
                                    {photo.has_face && <div className="photo-has-face">👤</div>}
                                    {photo.is_nude && <div className="photo-is-nude">🔞</div>}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default PhotoGrid; 