import React, { FC } from 'react';
import { Card, CardContent, CardHeader } from '@mui/material';

export interface InfoCardProps {
  title: string;
  children?: React.ReactNode;
}

export const InfoCard: FC<InfoCardProps> = ({ title, children }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardHeader title={title} />
      <CardContent>{children}</CardContent>
    </Card>
  );
};
