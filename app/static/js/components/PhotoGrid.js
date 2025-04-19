import React from 'react';
import { Grid, Card, CardMedia, CardContent, Typography, Box } from '@mui/material';

const PhotoGrid = ({ photos }) => {
  const getThumbnailUrl = (path) => {
    // Ищем позицию "Pictures/!Фотосессии" в пути
    const targetPrefix = "Pictures/!Фотосессии";
    let processedPath = path;
    
    // Удаляем префикс /mnt/smb/OneDrive из пути
    if (path.startsWith('/mnt/smb/OneDrive/')) {
      processedPath = path.substring('/mnt/smb/OneDrive/'.length);
    } else if (path.startsWith('mnt/smb/OneDrive/')) {
      processedPath = path.substring('mnt/smb/OneDrive/'.length);
    }
    
    // Находим позицию "Pictures/!Фотосессии" в обработанном пути
    const targetIndex = processedPath.indexOf(targetPrefix);
    
    // Если нашли, откусываем путь до "Pictures/!Фотосессии"
    if (targetIndex !== -1) {
      processedPath = processedPath.substring(targetIndex);
    }
    
    // Кодируем только нужную часть пути
    const encodedPath = encodeURIComponent(processedPath);
    return `https://gallery.homoludens.photos/pgapi/gallery/content/${encodedPath}/thumbnail/480`;
  };

  return (
    <Box sx={{ p: 2 }}>
      <Grid container spacing={2}>
        {photos.map((photo) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={photo.path}>
            <Card>
              <CardMedia
                component="img"
                height="240"
                image={getThumbnailUrl(photo.path)}
                alt={photo.path}
              />
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  Status: {photo.status}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Nude: {photo.is_nude ? 'Yes' : 'No'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Face: {photo.has_face ? 'Yes' : 'No'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default PhotoGrid; 