'use client';
import { AppBar, Button, IconButton, Stack, Toolbar, Typography, useTheme } from '@mui/material';
import Image from 'next/image';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

export const Header = () => {
  const { palette } = useTheme();
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
        <Stack gap={3} direction="row" alignItems="center">
          <IconButton size="large" edge="end" aria-label="github" href="https://github.com/ericmarg/ScrutinyCSPM" component="a" target="_blank">
            <FontAwesomeIcon color={palette.secondary.main} icon={faGithub} />
          </IconButton>
          <Link href="/dashboard">
            <Button color="secondary">
              <Typography variant="h6">Dashboard</Typography>
            </Button>
          </Link>
        </Stack>
      </Toolbar>
    </AppBar>
  );
};
