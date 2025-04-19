import React from 'react';
import { List, ListItem, ListItemIcon, ListItemText, Collapse } from '@mui/material';
import { Folder, FolderOpen, ExpandMore, ChevronRight } from '@mui/icons-material';

const DirectoryTree = ({ tree, onSelectDirectory, selectedDirectory }) => {
  const [expanded, setExpanded] = React.useState({});

  const handleToggle = (path) => {
    setExpanded(prev => ({
      ...prev,
      [path]: !prev[path]
    }));
  };

  const renderTree = (node, path = '') => {
    if (!node) return null;

    return (
      <List component="div" disablePadding>
        {Object.entries(node.dirs).map(([name, dirNode]) => {
          const currentPath = path ? `${path}/${name}` : name;
          const isExpanded = expanded[currentPath];
          const isSelected = currentPath === selectedDirectory;

          return (
            <React.Fragment key={currentPath}>
              <ListItem
                button
                onClick={() => {
                  handleToggle(currentPath);
                  onSelectDirectory(currentPath);
                }}
                selected={isSelected}
                sx={{ pl: path ? 4 : 2 }}
              >
                <ListItemIcon>
                  {isExpanded ? <FolderOpen /> : <Folder />}
                </ListItemIcon>
                <ListItemText primary={name} />
                {Object.keys(dirNode.dirs).length > 0 && (
                  isExpanded ? <ExpandMore /> : <ChevronRight />
                )}
              </ListItem>
              <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                {renderTree(dirNode, currentPath)}
              </Collapse>
            </React.Fragment>
          );
        })}
      </List>
    );
  };

  return renderTree(tree);
};

export default DirectoryTree; 