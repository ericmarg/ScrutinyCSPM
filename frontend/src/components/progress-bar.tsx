import { FC } from 'react';
import { LinearProgress, linearProgressClasses } from '@mui/material';

export interface ProgressBarProps {
  openIssues: number;
  totalResources: number;
}

export const ProgressBar: FC<ProgressBarProps> = ({ openIssues, totalResources }) => {
  return (
    <LinearProgress
      variant="determinate"
      value={((totalResources - openIssues) / totalResources) * 100}
      sx={(theme) => ({
        height: 10,
        borderRadius: 5,
        [`&.${linearProgressClasses.colorPrimary}`]: {
          backgroundColor: theme.palette.error.main
        },
        [`& .${linearProgressClasses.bar}`]: {
          borderRadius: 5,
          backgroundColor: theme.palette.success.main
        }
      })}
    />
  );
};
