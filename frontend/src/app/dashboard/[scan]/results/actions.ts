'use server';

import { existsSync, readFileSync } from 'node:fs';
import { ResourceList, ResourceType, Scan } from '@/types/scan';
import { isAfter, subDays } from 'date-fns';
import { IssueType } from '@/components/issue';

export async function getScan(id: string): Promise<Scan | null> {
  // Check if the scan exists
  const scanFolder = existsSync(`scans/${id}`);
  if (!scanFolder) {
    return null;
  }
  // Check if the inventory file exists
  const inventoryFile = existsSync(`scans/${id}/inventory.json`);
  if (!inventoryFile) {
    return null;
  }
  // Read the inventory file
  const inventory = JSON.parse(readFileSync(`scans/${id}/inventory.json`, 'utf8'));
  const vms = await getResources(inventory, 'vms');
  const buckets = await getResources(inventory, 'buckets');
  const securityGroups = await getResources(inventory, 'security_group');
  const openIssues = vms.openIssues + buckets.openIssues + securityGroups.openIssues;
  let avgAge = vms.avgAge.getTime() * vms.totalResources + buckets.avgAge.getTime() * buckets.totalResources + securityGroups.avgAge.getTime() * securityGroups.totalResources;
  avgAge = avgAge / (vms.totalResources + buckets.totalResources + securityGroups.totalResources);
  const recentIssues = vms.recentIssues + buckets.recentIssues + securityGroups.recentIssues;

  return {
    id,
    inventory,
    vms,
    buckets,
    securityGroups,
    openIssues,
    recentIssues,
    timestamp: new Date(Number(id)).toISOString(),
    totalResources: countTotalResources(inventory),
    avgAge: new Date(avgAge)
  };
}

function countTotalResources(inventory: Record<string, any>): number {
  let count = 0;
  for (const provider in inventory) {
    const account = inventory[provider].account;
    count += Number(account.ec2_instance_count);
    count += Number(account.s3_bucket_count);
    count += Number(account.vpc_count);
    count += Number(account.security_group_count);
  }
  return count;
}

async function getResources(inventory: Record<string, any>, type: ResourceType): Promise<ResourceList> {
  let totalResources = 0;
  let resources = [];
  for (const provider in inventory) {
    const provider_resources = inventory[provider][type] || [];
    totalResources += provider_resources.length;
    resources.push(
      ...provider_resources.map((r: any) => {
        return {
          id: r.Name || r.InstanceId || r.GroupId,
          name: r.Name || (r.Tags ? r.Tags.find((t: any) => t.Key === 'Name')?.Value || null : null) || r.InstanceId || r.GroupName || r.GroupId,
          type,
          provider,
          age: !!r.CreatedAt || !!r.LaunchTime ? new Date(r.CreatedAt || r.LaunchTime) : new Date(),
          issues: getIssues(r, provider, type)
        };
      })
    );
  }
  resources.sort((a: any, b: any) => b.issues.length - a.issues.length);
  let openIssues = 0;
  let recentIssues = 0;
  let avgAge = 0;
  resources.forEach((r: any) => {
    openIssues += r.issues.length;
    avgAge += r.age.getTime();
    if (isAfter(r.age, subDays(new Date(), 30))) {
      recentIssues++;
    }
  });
  if (resources.length > 0) {
    avgAge = avgAge / resources.length;
  }

  return {
    totalResources,
    resources,
    openIssues,
    avgAge: new Date(avgAge),
    recentIssues
  };
}

function getIssues(resource: any, provider: string, type: ResourceType): string[] {
  switch (type) {
    case 'vms':
      return getVmIssues(resource);
    case 'buckets':
      return getBucketIssues(resource);
    case 'security_group':
      return [];
    default:
      return [];
  }
}

function getVmIssues(resource: any): string[] {
  const issues: string[] = [];
  if (resource.PublicIpAddress) {
    issues.push(IssueType.PublicIP);
  }
  return issues;
}

function getBucketIssues(resource: any): string[] {
  const issues: string[] = [];
  if (!resource?.Details?.Encryption) {
    issues.push(IssueType.UnencryptedBucket);
  }
  if (resource?.Details.Policy?.Statement.length > 0) {
    issues.push(IssueType.OpenBucket);
  }
  if (!resource?.Details.Policy?.Versioning) {
    issues.push(IssueType.BucketVersioning);
  }
  return issues;
}
