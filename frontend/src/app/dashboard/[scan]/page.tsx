import Image from 'next/image';
import { Container } from '@mui/system';
import { Card, CardHeader, Grid, Typography } from '@mui/material';
import React from 'react';
import { InfoCard } from '@/components/info-card';

export default function Dashboard() {
  return (
    <Container>
      <Grid container>
        <Grid item xs={12} md={4}>
          <InfoCard title="Open Issues">
            <Typography variant="h3">17</Typography>
          </InfoCard>
        </Grid>
      </Grid>
    </Container>
  );
}
