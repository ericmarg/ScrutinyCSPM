'use client';
import { Container } from '@mui/system';
import { Grid, Stack, Typography } from '@mui/material';
import React from 'react';
import { InfoCard } from '@/components/info-card';
import { ResourceList } from '@/components/resource-list';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAws, faBitbucket, faWindows } from '@fortawesome/free-brands-svg-icons';
import { ResourceListItem } from '@/components/resource-list-item';
import { ProgressBar } from '@/components/progress-bar';
import { faServer, faUserShield } from '@fortawesome/free-solid-svg-icons';
import { getScan } from '@/app/dashboard/[scan]/results/actions';
import { usePathname } from 'next/navigation';

export default function ScanResult() {
  const path = usePathname();
  const scanId = path.split('/')[2];
  getScan(scanId).then((data) => {
    console.log(data);
  });
  return (
    <Container maxWidth="lg">
      <Stack spacing={3}>
        <ProgressBar openIssues={17} totalResources={100} />
        <Grid container spacing={3} display="flex">
          <Grid item xs={12} md={4}>
            <InfoCard title="Open Issues">
              <Typography variant="h3">17</Typography>
            </InfoCard>
          </Grid>
          <Grid item xs={12} md={4}>
            <InfoCard title="Recent Issues">
              <Typography variant="h3">6</Typography>
              <Typography variant="h6">last 30 days</Typography>
            </InfoCard>
          </Grid>
          <Grid item xs={12} md={4}>
            <InfoCard title="Issue Avg Age">
              <Typography variant="h3">103</Typography>
              <Typography variant="h6">days</Typography>
            </InfoCard>
          </Grid>
        </Grid>
        <Grid container spacing={3} display="flex">
          <Grid item xs={12} sm={6} md={4} lg={4}>
            <ResourceList name="Object Storage Buckets" icon={<FontAwesomeIcon icon={faBitbucket} />} openIssues={5} total={24}>
              <ResourceListItem name="aws-storage-bucket" icon={<FontAwesomeIcon icon={faAws} />} />
              <ResourceListItem name="azure-storage-bucket" icon={<FontAwesomeIcon icon={faWindows} />} />
              <ResourceListItem name="aws-storage-bucket" icon={<FontAwesomeIcon icon={faAws} />} />
            </ResourceList>
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4}>
            <ResourceList name="Virtual Machines" icon={<FontAwesomeIcon icon={faServer} />} openIssues={6} total={15}>
              <ResourceListItem name="aws-vm-1" icon={<FontAwesomeIcon icon={faAws} />} />
              <ResourceListItem name="azure-vm-2" icon={<FontAwesomeIcon icon={faWindows} />} />
              <ResourceListItem name="aws-vm-3" icon={<FontAwesomeIcon icon={faAws} />} />
            </ResourceList>
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4}>
            <ResourceList name="Roles & Permissions" icon={<FontAwesomeIcon icon={faUserShield} />} openIssues={6} total={24}>
              <ResourceListItem name="aws-iam-role" icon={<FontAwesomeIcon icon={faAws} />} />
              <ResourceListItem name="azure-iam-role" icon={<FontAwesomeIcon icon={faWindows} />} />
              <ResourceListItem name="aws-iam-role-2" icon={<FontAwesomeIcon icon={faAws} />} />
            </ResourceList>
          </Grid>
        </Grid>
      </Stack>
    </Container>
  );
}
