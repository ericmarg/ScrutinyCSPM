'use client';
import React, { FC } from 'react';
import { Avatar, Box, Stack, Typography, useTheme } from '@mui/material';
import { Resource } from '@/types/scan';
import { ResourceIcon } from '@/components/resource-list-item';
import { Issue } from '@/components/issue';

export interface ResourceProps {
  resource: Resource;
}

export const ResourceItem: FC<ResourceProps> = ({ resource }) => {
  const { palette } = useTheme();

  return (
    <Stack gap={2} sx={{ m: 3, minWidth: '50vw', maxWidth: '50vw' }}>
      <Stack direction="row" alignItems="center" gap={1}>
        <Avatar
          variant="rounded"
          sx={{
            width: '5vw',
            height: '5vw',
            bgcolor: resource.provider === 'aws' ? '#ff9900' : '#0080ff'
          }}
        >
          <ResourceIcon provider={resource.provider} color="#FFF" />
        </Avatar>
        <Box>
          <Typography variant="h5" color={palette.text.primary}>
            {resource.name}
          </Typography>
          <Typography variant="subtitle1" color={palette.text.primary}>
            ID: {resource.id}
          </Typography>
        </Box>
      </Stack>
      <Typography variant="h6" color={palette.text.primary}>
        Identified Vulnerabilities
      </Typography>
      {resource.issues.map((issue, index) => (
        <Issue issue={issue} key={index} />
      ))}
      {resource.issues.length === 0 && (
        <Typography variant="subtitle1" color={palette.text.primary}>
          No vulnerabilities found
        </Typography>
      )}
    </Stack>
  );
};
