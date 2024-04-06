'use client';
import { Container } from '@mui/system';
import { Box, Button, Card, Stack, Typography } from '@mui/material';
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faSatelliteDish } from '@fortawesome/free-solid-svg-icons';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Scan } from '@/types/scan';
import { format } from 'date-fns';
import Link from 'next/link';
import { ProgressBar } from '@/components/progress-bar';

const columns: GridColDef[] = [
  {
    field: 'timestamp',
    headerName: 'Timestamp',
    width: 200,
    renderCell: (params) => {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
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
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
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

const getScans = async () => {
  const scans: Scan[] = [
    {
      id: '1',
      timestamp: '2021-09-01T12:23:00Z',
      openIssues: 17,
      totalResources: 105
    },
    {
      id: '2',
      timestamp: '2021-09-02T13:12:00Z',
      openIssues: 12,
      totalResources: 102
    },
    {
      id: '3',
      timestamp: '2021-09-03T14:43:00Z',
      openIssues: 9,
      totalResources: 100
    }
  ];
  return scans;
};

export default async function Dashboard() {
  const scans = await getScans();
  return (
    <Container>
      <Box display="flex" sx={{ mb: 2 }}>
        <Typography variant="h3" component="h1">
          <FontAwesomeIcon icon={faSatelliteDish} style={{ marginRight: '2rem' }} />
          Previous Scans
        </Typography>
        <Box sx={{ flexGrow: 1 }} />
        <Box alignContent="center">
          <Button startIcon={<FontAwesomeIcon icon={faPlus} />} variant="contained">
            <Typography>New Scan</Typography>
          </Button>
        </Box>
      </Box>
      <Card sx={{ height: '75vh' }}>
        <DataGrid columns={columns} rows={scans} hideFooter />
      </Card>
    </Container>
  );
}
