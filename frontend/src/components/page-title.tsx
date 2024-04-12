'use client';
import React, { FC } from 'react';
import { Scan } from '@/types/scan';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Typography } from '@mui/material';
import { format } from 'date-fns';
import { ProgressBar } from '@/components/progress-bar';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faSatelliteDish, IconDefinition } from '@fortawesome/free-solid-svg-icons';

export interface PageTitleProps {
  title: string;
  icon?: IconDefinition;
  children?: React.ReactNode;
}

export const PageTitle: FC<PageTitleProps> = ({ title, icon, children }) => {
  return (
    <Box display="flex" sx={{ mb: 2 }}>
      <Typography variant="h3" component="h1">
        {icon && <FontAwesomeIcon icon={icon} style={{ marginRight: '2rem' }} />}
        {title}
      </Typography>
      <Box sx={{ flexGrow: 1 }} />
      <Box alignContent="center">{children}</Box>
    </Box>
  );
};
