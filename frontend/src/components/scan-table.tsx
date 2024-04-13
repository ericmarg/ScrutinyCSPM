'use client';
import React, { FC } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Stack, Typography } from '@mui/material';
import { format, formatDistanceToNow } from 'date-fns';
import Link from 'next/link';
import { ScanListItem } from '@/types/scan-list-item';

export interface ScanTableProps {
  scans: ScanListItem[];
}

const columns: GridColDef[] = [
  {
    field: 'name',
    headerName: 'Scan Name',
    flex: 1,
    renderCell: (params) => {
      return (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            height: '100%'
          }}
        >
          <Typography>
            <strong>{params.value}</strong>
          </Typography>
        </Box>
      );
    }
  },
  {
    field: 'date',
    headerName: 'Timestamp',
    flex: 1,
    renderCell: (params) => {
      return (
        <Stack
          direction="row"
          gap={2}
          sx={{
            display: 'flex',
            alignItems: 'center',
            height: '100%'
          }}
        >
          <Typography>{format(params.value, 'MM/dd/yyyy HH:mm aa')}</Typography>
          <Typography variant="body2">{formatDistanceToNow(params.value)} ago</Typography>
        </Stack>
      );
    }
  },
  {
    field: 'id',
    width: 200,
    headerName: '',
    renderCell: (params) => {
      return (
        <Link href={`/dashboard/${params.value}`}>
          <Button variant="contained" color="primary" component="a">
            <Typography>View Scan</Typography>
          </Button>
        </Link>
      );
    }
  }
];
export const ScanTable: FC<ScanTableProps> = ({ scans }) => {
  return <DataGrid columns={columns} rows={scans} hideFooter />;
};
