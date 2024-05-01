'use client';
import React, { FC } from 'react';
import { Avatar, Card, CardContent, List, Stack, Typography, useTheme } from '@mui/material';
import { ProgressBar } from '@/components/progress-bar';
import { Resource, ResourceList as ScanResourceList } from '@/types/scan';
import { ResourceListItem } from '@/components/resource-list-item';

export interface ResourceListProps {
  resourceList: ScanResourceList;
  icon?: React.ReactNode;
  name: string;
  onResource: (resource: Resource) => void;
}

export const ResourceList: FC<ResourceListProps> = ({ resourceList, icon, name, onResource }) => {
  const { palette } = useTheme();
  return (
    <Stack gap={1}>
      <Stack direction="row" alignItems="center" gap={1}>
        {icon && (
          <Avatar variant="rounded" sx={{ bgcolor: palette.secondary.main, p: 1 }}>
            {icon}
          </Avatar>
        )}
        <Typography variant="h6" color={palette.text.primary}>
          {name}
        </Typography>
      </Stack>
      {resourceList && <ProgressBar openIssues={resourceList.openIssues} totalResources={resourceList.totalResources} />}
      <Card>
        <CardContent>
          <List dense>
            {resourceList.resources.map((resource) => (
              <ResourceListItem key={resource.id} resource={resource} onClick={() => onResource(resource)} />
            ))}
          </List>
        </CardContent>
      </Card>
    </Stack>
  );
};
