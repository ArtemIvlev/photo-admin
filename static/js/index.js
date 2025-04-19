import React from 'react';
import ReactDOM from 'react-dom';
import PhotoTree from './components/PhotoTree';
import PhotoGrid from './components/PhotoGrid';

// Инициализация компонента дерева
ReactDOM.render(
    <React.StrictMode>
        <PhotoTree />
    </React.StrictMode>,
    document.getElementById('root')
);

// Инициализация компонента сетки
ReactDOM.render(
    <React.StrictMode>
        <PhotoGrid />
    </React.StrictMode>,
    document.getElementById('photo-grid')
); 