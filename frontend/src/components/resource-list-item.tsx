'use client';
import React, { FC } from 'react';
import { Badge, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { Provider, Resource } from '@/types/scan';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAws, faWindows } from '@fortawesome/free-brands-svg-icons';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';

export interface ResourceListItemProps {
  resource: Resource;
  onClick?: () => void;
}

export const ResourceListItem: FC<ResourceListItemProps> = ({ resource, onClick }) => {
  return (
    <ListItem disablePadding secondaryAction={<FontAwesomeIcon icon={faChevronRight} />}>
      <ListItemButton onClick={() => (onClick ? onClick() : null)}>
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

export const ResourceIcon: FC<{ provider: Provider; color?: string }> = ({ provider, color }) => {
  switch (provider) {
    case 'aws':
      return <FontAwesomeIcon icon={faAws} color={color ? color : '#ff9900'} />;
    case 'azure':
      return <FontAwesomeIcon icon={faWindows} color={color ? color : '#0080ff'} />;
  }
};
