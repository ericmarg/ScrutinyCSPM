import React, { FC } from 'react';
import { Card, CardContent, CardHeader } from '@mui/material';

export interface InfoCardProps {
  title: string;
  children?: React.ReactNode;
}

export const InfoCard: FC<InfoCardProps> = ({ title, children }) => {
  return (
    <Card>
      <CardHeader title={title} />
      <CardContent>{children}</CardContent>
    </Card>
  );
};
