import React, { useState, useEffect } from 'react';
import { Box, Grid, Paper } from '@mui/material';
import DirectoryTree from './DirectoryTree';
import PhotoGrid from './PhotoGrid';

const App = () => {
  const [tree, setTree] = useState(null);
  const [selectedDirectory, setSelectedDirectory] = useState('');
  const [photos, setPhotos] = useState([]);

  useEffect(() => {
    fetch('/api/tree')
      .then(response => response.json())
      .then(data => setTree(data))
      .catch(error => console.error('Error fetching tree:', error));
  }, []);

  useEffect(() => {
    if (selectedDirectory) {
      fetch(`/api/photos/${encodeURIComponent(selectedDirectory)}`)
        .then(response => response.json())
        .then(data => setPhotos(data.files))
        .catch(error => console.error('Error fetching photos:', error));
    }
  }, [selectedDirectory]);

  return (
    <Box sx={{ flexGrow: 1, height: '100vh', p: 2 }}>
      <Grid container spacing={2} sx={{ height: '100%' }}>
        <Grid item xs={3}>
          <Paper sx={{ height: '100%', overflow: 'auto' }}>
            <DirectoryTree 
              tree={tree} 
              onSelectDirectory={setSelectedDirectory}
              selectedDirectory={selectedDirectory}
            />
          </Paper>
        </Grid>
        <Grid item xs={9}>
          <Paper sx={{ height: '100%', overflow: 'auto' }}>
            <PhotoGrid photos={photos} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default App; 