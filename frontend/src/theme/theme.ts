'use client';
import { createTheme } from '@mui/material';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#173a4d'
    },
    secondary: {
      main: '#6CCDEA'
    },
    background: {
      default: '#fef7e7'
    }
  },
  typography: {
    fontFamily: 'Roboto',
    h1: {
      fontFamily: 'Quicksand',
      fontWeight: 700
    },
    h2: {
      fontFamily: 'Quicksand',
      fontWeight: 700
    },
    h3: {
      fontFamily: 'Quicksand',
      fontWeight: 700
    },
    h4: {
      fontFamily: 'Quicksand',
      fontWeight: 700
    },
    h5: {
      fontFamily: 'Quicksand',
      fontWeight: 700
    },
    h6: {
      fontFamily: 'Quicksand',
      fontWeight: 700
    }
  }
});
