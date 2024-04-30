'use server';

import { existsSync, readFileSync } from 'node:fs';
import { Scan } from '@/types/scan';

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
  return {
    id,
    timestamp: new Date(Number(id)).toISOString(),
    inventory,
    totalResources: countTotalResources(inventory)
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
