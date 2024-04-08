'use client';
import React, { FC } from 'react';
import { ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';

export interface ResourceListItemProps {
  name: string;
  icon?: React.ReactNode;
}

export const ResourceListItem: FC<ResourceListItemProps> = ({ name, icon }) => {
  return (
    <ListItem disablePadding>
      <ListItemButton>
        <ListItemIcon>{icon}</ListItemIcon>
        <ListItemText>{name}</ListItemText>
      </ListItemButton>
    </ListItem>
  );
};
