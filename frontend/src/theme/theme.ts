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
    text: {
      primary: '#173a4d'
    },
    success: {
      main: '#4caf50'
    },
    error: {
      main: '#f44336'
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
  },
  shape: {
    borderRadius: 10
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 50
        }
      },
      defaultProps: {
        color: 'secondary'
      }
    }
  }
});
