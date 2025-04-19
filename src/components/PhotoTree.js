import React, { useState, useEffect } from 'react';
import './PhotoTree.css';

const PhotoTree = () => {
  const [tree, setTree] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTree = async () => {
      try {
        const response = await fetch('/api/tree');
        if (!response.ok) {
          throw new Error('Ошибка при загрузке дерева');
        }
        const data = await response.json();
        setTree(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTree();
  }, []);

  const renderNode = (node, path = '') => {
    const currentPath = path ? `${path}/${node.name}` : node.name;

    return (
      <div key={currentPath} className="tree-node">
        <div className="directory">
          <div className="directory-name">{node.name}</div>
          {node.files && node.files.length > 0 && (
            <div className="files">
              {node.files.map((file) => (
                <div key={file.path} className="file">
                  <span className={`file-name ${file.is_nude ? 'nude' : ''} ${file.has_face ? 'face' : ''}`}>
                    {file.name}
                  </span>
                  <span className="file-status">{file.status}</span>
                  <span className="file-score">{file.nsfw_score?.toFixed(2) || 'N/A'}</span>
                </div>
              ))}
            </div>
          )}
          {node.dirs && Object.keys(node.dirs).length > 0 && (
            <div className="directories">
              {Object.values(node.dirs).map((dir) => renderNode(dir, currentPath))}
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
      {renderNode(tree)}
    </div>
  );
};

export default PhotoTree; 