import React, { FC } from 'react';
import { Card, CardContent, CardHeader, Chip, Typography } from '@mui/material';

export enum IssueType {
  PublicIP = 'Public IP',
  OpenBucket = 'Open Bucket',
  UnencryptedBucket = 'Unencrypted Bucket',
  BucketVersioning = 'Bucket Versioning'
}

export interface IssueProps {
  issue: IssueType;
}

export const Issue: FC<IssueProps> = ({ issue }) => {
  return (
    <Card>
      <CardHeader title={getTitle(issue)} subheader={<Typography variant="subtitle1">{getStandard(issue)}</Typography>} action={getSeverity(issue)} />
      <CardContent>
        <Typography variant="body1">{getDetails(issue)}</Typography>
      </CardContent>
    </Card>
  );
};

const getTitle = (issue: IssueType) => {
  switch (issue) {
    case IssueType.PublicIP:
      return 'VMs should not have a public IP address';
    case IssueType.OpenBucket:
      return 'Bucket should prohibit public read access';
    case IssueType.UnencryptedBucket:
      return 'Bucket default encryption should be enabled';
    case IssueType.BucketVersioning:
      return 'Bucket versioning should be enabled';
  }
};

const getStandard = (issue: IssueType) => {
  switch (issue) {
    case IssueType.PublicIP:
      return 'NIST Cybersecurity Framework (CSF) v1.1';
    case IssueType.OpenBucket:
      return 'NIST 800-171 Revision 2';
    case IssueType.UnencryptedBucket:
      return 'NIST 800-171 Revision 2';
    case IssueType.BucketVersioning:
      return 'NIST 800-53 Revision 4';
  }
};

const getSeverity = (issue: IssueType) => {
  switch (issue) {
    case IssueType.PublicIP:
      return <Chip label="High" color="error" />;
    case IssueType.OpenBucket:
      return <Chip label="Medium" color="warning" />;
    case IssueType.UnencryptedBucket:
      return <Chip label="Low" color="info" />;
    case IssueType.BucketVersioning:
      return <Chip label="High" color="error" />;
  }
};

const getDetails = (issue: IssueType) => {
  switch (issue) {
    case IssueType.PublicIP:
      return 'The rule in NIST Cybersecurity Framework (CSF) v1 specifies that vm instances should not have public IP addresses. This rule is enforced to ensure the security and protection of the vm instances from potential external threats. Public IP addresses make the instances directly accessible from the internet, increasing the attack surface and exposing them to potential vulnerabilities.';
    case IssueType.OpenBucket:
      return 'This rule requires that all buckets should have public read access disabled in order to comply with NIST 800-171 Revision 2 security standards. Allowing public read access to buckets could potentially expose sensitive data to unauthorized users, which poses a security risk.';
    case IssueType.UnencryptedBucket:
      return 'This rule ensures that default encryption is enabled for buckets to comply with the security requirements specified in the National Institute of Standards and Technology (NIST) Special Publication 800-171 Revision 2. By enabling default encryption, all newly created objects in the bucket will be encrypted using server-side encryption.';
    case IssueType.BucketVersioning:
      return 'This rule requires that versioning is enabled for buckets in compliance with NIST 800-53 Revision 4, a publication by the National Institute of Standards and Technology (NIST) that provides a catalog of security and privacy controls for federal information systems and organizations.\n Enabling versioning for buckets ensures that all versions of objects stored in the bucket are retained, allowing for easy retrieval of previous versions if needed. This helps in maintaining data integrity and supports data recovery in case of accidental deletions or data corruption.';
  }
};
