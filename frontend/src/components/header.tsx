import { AppBar, IconButton, Toolbar, Typography } from '@mui/material';
import Image from 'next/image';

export const Header = () => {
  return (
    <AppBar position="static" elevation={0} sx={{ background: 'transparent' }}>
      <Toolbar>
        <IconButton size="large" edge="start" aria-label="logo">
          <Image src="/logo.png" alt="logo" width={60} height={60} />
        </IconButton>
        <Typography variant="h6" component="div" color="primary" sx={{ flexGrow: 1 }}>
          ScrutinyCSPM
        </Typography>
      </Toolbar>
    </AppBar>
  );
};
