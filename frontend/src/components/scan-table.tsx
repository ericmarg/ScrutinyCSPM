'use client';
import React, { FC } from 'react';
import { Scan } from '@/types/scan';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Typography } from '@mui/material';
import { format } from 'date-fns';
import { ProgressBar } from '@/components/progress-bar';
import Link from 'next/link';

export interface ScanTableProps {
  scans: Scan[];
}

const columns: GridColDef[] = [
  {
    field: 'timestamp',
    headerName: 'Timestamp',
    width: 200,
    renderCell: (params) => {
      return (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%'
          }}
        >
          <Typography>{format(new Date(params.value as string), 'yyyy-MM-dd HH:mm aa')}</Typography>
        </Box>
      );
    }
  },
  {
    field: 'openIssues',
    headerName: 'Open Issues',
    flex: 1,
    renderCell: (params) => {
      return (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%'
          }}
        >
          <Box sx={{ width: '100%', mr: 1 }}>
            <ProgressBar openIssues={params.value} totalResources={params.row.totalResources} />
          </Box>
          <Box sx={{ minWidth: 35 }}>
            <Typography variant="h6">{params.value}</Typography>
          </Box>
        </Box>
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
