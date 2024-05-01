import { IssueType } from '@/components/issue';

export interface Scan {
  id: string;
  timestamp: string;
  inventory: Inventory;
  totalResources: number;
  openIssues: number;
  avgAge: Date;
  recentIssues: number;
  vms: ResourceList;
  buckets: ResourceList;
  securityGroups: ResourceList;
}

export type Inventory = Record<string, ProviderInfo>;

export interface ProviderInfo {
  account: string;
}

export type ResourceType = 'vms' | 'buckets' | 'vpc' | 'security_group';
export type Provider = 'aws' | 'azure' | 'gcp';

export type ResourceList = {
  totalResources: number;
  openIssues: number;
  avgAge: Date;
  resources: Resource[];
  recentIssues: number;
};

export type Resource = {
  id: string;
  name: string;
  type: ResourceType;
  provider: Provider;
  age: Date;
  issues: IssueType[];
};
