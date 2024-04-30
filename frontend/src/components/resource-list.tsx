'use client';
import React, { FC } from 'react';
import { Avatar, Button, Card, CardContent, List, Stack, Typography, useTheme } from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { ProgressBar } from '@/components/progress-bar';
import { ResourceList as ScanResourceList } from '@/types/scan';
import { ResourceListItem } from '@/components/resource-list-item';

export interface ResourceListProps {
  resourceList: ScanResourceList;
  icon?: React.ReactNode;
  name: string;
}

export const ResourceList: FC<ResourceListProps> = ({ resourceList, icon, name }) => {
  const { palette } = useTheme();
  return (
    <Stack gap={1}>
      <Stack direction="row" alignItems="center" gap={1}>
        {icon && (
          <Avatar variant="rounded" sx={{ bgcolor: palette.secondary.main, p: 1 }}>
            {icon}
          </Avatar>
        )}
        <Button endIcon={<FontAwesomeIcon icon={faChevronRight} color={palette.text.primary} />}>
          <Typography variant="h6" color={palette.text.primary}>
            {name}
          </Typography>
        </Button>
      </Stack>
      {resourceList && <ProgressBar openIssues={resourceList.openIssues} totalResources={resourceList.totalResources} />}
      <Card>
        <CardContent>
          <List dense>
            {resourceList.resources.map((resource) => (
              <ResourceListItem key={resource.id} resource={resource} />
            ))}
          </List>
        </CardContent>
      </Card>
    </Stack>
  );
};
