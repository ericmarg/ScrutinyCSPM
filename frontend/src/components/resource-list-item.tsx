'use client';
import React, { FC } from 'react';
import { Badge, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { Provider, Resource } from '@/types/scan';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAws, faWindows } from '@fortawesome/free-brands-svg-icons';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';

export interface ResourceListItemProps {
  resource: Resource;
}

export const ResourceListItem: FC<ResourceListItemProps> = ({ resource }) => {
  return (
    <ListItem disablePadding secondaryAction={<FontAwesomeIcon icon={faChevronRight} />}>
      <ListItemButton>
        <ListItemIcon>
          {resource.issues.length > 0 ? (
            <Badge color="error" variant="dot">
              <ResourceIcon provider={resource.provider} />
            </Badge>
          ) : (
            <ResourceIcon provider={resource.provider} />
          )}
        </ListItemIcon>
        <ListItemText secondary={`${resource.issues.length} issues`}>{resource.name}</ListItemText>
      </ListItemButton>
    </ListItem>
  );
};

const ResourceIcon: FC<{ provider: Provider }> = ({ provider }) => {
  switch (provider) {
    case 'aws':
      return <FontAwesomeIcon icon={faAws} />;
    case 'azure':
      return <FontAwesomeIcon icon={faWindows} />;
  }
};
