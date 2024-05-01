'use server';
import { Container } from '@mui/system';
import { Card } from '@mui/material';
import React from 'react';
import { faSatelliteDish } from '@fortawesome/free-solid-svg-icons';
import { getScans } from '@/app/dashboard/actions';
import { ScanTable } from '@/components/scan-table';
import { PageTitle } from '@/components/page-title';

export default async function Dashboard() {
  const scans = await getScans();
  return (
    <Container>
      <PageTitle title={'Dashboard'} icon={faSatelliteDish} />
      <Card sx={{ height: '75vh' }}>
        <ScanTable scans={scans} />
      </Card>
    </Container>
  );
}
