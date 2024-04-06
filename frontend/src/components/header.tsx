import { AppBar, Button, IconButton, Toolbar, Typography } from '@mui/material';
import Image from 'next/image';
import Link from 'next/link';

export const Header = () => {
  return (
    <AppBar position="static" elevation={0} sx={{ background: 'transparent' }}>
      <Toolbar>
        <Link href="/">
          <IconButton size="large" edge="start" aria-label="logo">
            <Image src="/logo.png" alt="logo" width={60} height={60} />
          </IconButton>
        </Link>
        <Typography variant="h6" component="div" color="primary" sx={{ flexGrow: 1 }}>
          ScrutinyCSPM
        </Typography>
        <Link href="/dashboard">
          <Button color="secondary" variant="contained">
            <Typography variant="h6">Dashboard</Typography>
          </Button>
        </Link>
      </Toolbar>
    </AppBar>
  );
};
