'use client';
import { Container } from '@mui/system';
import { Box, Drawer, Grid, IconButton, Stack, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { InfoCard } from '@/components/info-card';
import { ResourceList } from '@/components/resource-list';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBitbucket } from '@fortawesome/free-brands-svg-icons';
import { ProgressBar } from '@/components/progress-bar';
import { faArrowDownUpLock, faServer, faX } from '@fortawesome/free-solid-svg-icons';
import { getScan } from '@/app/dashboard/[scan]/results/actions';
import { usePathname } from 'next/navigation';
import { Resource, Scan } from '@/types/scan';
import { differenceInDays, format, formatDistanceToNow } from 'date-fns';
import { LoadingBackdrop } from '@/components/loading-backgrop';
import { ResourceItem } from '@/components/resource-item';

export default function ScanResult() {
  const path = usePathname();
  const scanId = path.split('/')[2];
  const [scan, setScan] = useState<Scan>();
  const [selectedResource, setSelectedResource] = useState<Resource | null>();
  useEffect(() => {
    getScan(scanId).then((data) => {
      if (data) {
        console.log(data);
        setScan(data);
      }
    });
  }, [scanId]);

  if (!scan) {
    return <LoadingBackdrop />;
  }
  return (
    <Container maxWidth="lg" sx={{ pb: 10 }}>
      <Stack spacing={3}>
        <ProgressBar openIssues={scan.openIssues} totalResources={scan.totalResources} />
        <Stack direction="row" alignItems="center">
          <Typography variant="h4" flex={1}>
            Scan Results
          </Typography>
          <Stack flex={1}>
            <Typography variant="h6" align="center">
              Scan ID: {scanId}
            </Typography>
            <Typography variant="subtitle1" align="center">
              Total Resources: {scan.totalResources}
            </Typography>
          </Stack>
          <Stack flex={1}>
            <Typography variant="h6" align="right">
              {format(new Date(scan?.timestamp), 'MM/dd/yyyy hh:mm aa')}
            </Typography>
            <Typography variant="subtitle1" align="right">
              {formatDistanceToNow(new Date(scan?.timestamp))} ago
            </Typography>
          </Stack>
        </Stack>
        <Grid container spacing={3} display="flex">
          <Grid item xs={12} md={4}>
            <InfoCard title="Open Issues">
              <Typography variant="h3">{scan.openIssues}</Typography>
            </InfoCard>
          </Grid>
          <Grid item xs={12} md={4}>
            <InfoCard title="Recent Issues">
              <Typography variant="h3">{scan.recentIssues}</Typography>
              <Typography variant="h6">last 30 days</Typography>
            </InfoCard>
          </Grid>
          <Grid item xs={12} md={4}>
            <InfoCard title="Issue Avg Age">
              <Typography variant="h3">{differenceInDays(new Date(), scan.avgAge)}</Typography>
              <Typography variant="h6">days ago</Typography>
            </InfoCard>
          </Grid>
        </Grid>
        <Grid container spacing={3} display="flex">
          <Grid item xs={12} sm={6} md={4} lg={4}>
            <ResourceList resourceList={scan.buckets} name="Object Storage Buckets" icon={<FontAwesomeIcon icon={faBitbucket} />} onResource={(r) => setSelectedResource(r)} />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4}>
            <ResourceList resourceList={scan.vms} name="Virtual Machines" icon={<FontAwesomeIcon icon={faServer} />} onResource={(r) => setSelectedResource(r)} />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4}>
            <ResourceList
              resourceList={scan.securityGroups}
              name="Security Groups"
              icon={<FontAwesomeIcon icon={faArrowDownUpLock} />}
              onResource={(r) => setSelectedResource(r)}
            />
          </Grid>
        </Grid>
      </Stack>
      <Drawer
        open={!!selectedResource}
        anchor="right"
        onClose={() => setSelectedResource(null)}
        PaperProps={{
          sx: {
            bgcolor: '#fef7e7'
          }
        }}
      >
        <Box mt={2} ml={2}>
          <IconButton onClick={() => setSelectedResource(null)}>
            <FontAwesomeIcon icon={faX} />
          </IconButton>
        </Box>
        {selectedResource && <ResourceItem resource={selectedResource} />}
      </Drawer>
    </Container>
  );
}
