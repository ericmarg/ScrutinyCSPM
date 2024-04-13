import { Container } from '@mui/system';
import { Box, Button, Card, CardContent, CardHeader, Grid, Stack, Typography } from '@mui/material';
import Image from 'next/image';
import Link from 'next/link';

export default function Home() {
  return (
    <Container>
      <Stack gap={2} sx={{ height: '75vh', display: 'flex', justifyContent: 'center', flexDirection: 'column' }}>
        <Stack gap={2} direction="row" component="section" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Image src="/logo.png" alt="logo" width={200} height={200} />
          <Typography variant="h1" gutterBottom>
            ScrutinyCSPM
          </Typography>
        </Stack>
        <Stack gap={2}>
          <Typography variant="body1">
            Secure your cloud infrastructure with ScrutinyCSPM, the premier open-source Cloud Security Posture Management (CSPM) solution engineered to help businesses proactively
            manage and mitigate cloud security risks. Developed by a network of security innovators, ScrutinyCSPM guarantees your cloud environments are safeguarded, compliant, and
            efficiently managed.
          </Typography>
          <Box display="flex" justifyContent="center">
            <Link href="/dashboard">
              <Button variant="contained">
                <Typography variant="h6">View Scans</Typography>
              </Button>
            </Link>
          </Box>
        </Stack>
      </Stack>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Open Source Security Solution" />
            <CardContent>
              <Typography>
                <strong>Empower Your Cloud Security:</strong> ScrutinyCSPM is fully open-source, allowing you to leverage the collective expertise of a global security community.
                Enjoy the flexibility of a transparently developed tool that evolves with the latest security trends and technologies. ScrutinyCSPM not only enhances your security
                posture but also keeps you ahead of the curve without the burden of costly licenses.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Community-Sourced Security Policies" />
            <CardContent>
              <Typography>
                <strong>Enhanced Compliance with Confidence:</strong> Benefit from a robust library of community-sourced security policies designed to ensure compliance with the
                most stringent standards. ScrutinyCSPM’s collaborative environment allows users to share, refine, and update compliance protocols, ensuring your cloud environments
                adhere to the latest security protocols. Engage with security professionals worldwide to maintain an up-to-date and resilient security framework.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Multi-Cloud Compatibility" />
            <CardContent>
              <Typography>
                <strong>Empower Your Cloud Security:</strong> ScrutinyCSPM is fully open-source, allowing you to leverage the collective expertise of a global security community.
                Enjoy the flexibility of a transparently developed tool that evolves with the latest security trends and technologies. ScrutinyCSPM not only enhances your security
                posture but also keeps you ahead of the curve without the burden of costly licenses.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Box sx={{ height: '30vh' }} />
    </Container>
  );
}
