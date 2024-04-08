'use client';
import React, { FC } from 'react';
import { Avatar, Button, Card, CardContent, List, Stack, Typography, useTheme } from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { ProgressBar } from '@/components/progress-bar';

export interface ResourceListProps {
  name: string;
  icon?: React.ReactNode;
  children?: React.ReactNode;
  openIssues?: number;
  total?: number;
}

export const ResourceList: FC<ResourceListProps> = ({ name, icon, children, openIssues, total }) => {
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
      {openIssues && total && <ProgressBar openIssues={openIssues} totalResources={total} />}
      <Card>
        <CardContent>
          <List>{children}</List>
        </CardContent>
      </Card>
    </Stack>
  );
};
