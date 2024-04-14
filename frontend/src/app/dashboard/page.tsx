'use server';
import { Container } from '@mui/system';
import { Button, Card, Typography } from '@mui/material';
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faSatelliteDish } from '@fortawesome/free-solid-svg-icons';
import { getScans } from '@/app/dashboard/actions';
import { ScanTable } from '@/components/scan-table';
import { PageTitle } from '@/components/page-title';

export default async function Dashboard() {
  const scans = await getScans();
  return (
    <Container>
      <PageTitle title={'Dashboard'} icon={faSatelliteDish}>
        <Button startIcon={<FontAwesomeIcon icon={faPlus} />} variant="contained">
          <Typography>New Scan</Typography>
        </Button>
      </PageTitle>
      <Card sx={{ height: '75vh' }}>
        <ScanTable scans={scans} />
      </Card>
    </Container>
  );
}
