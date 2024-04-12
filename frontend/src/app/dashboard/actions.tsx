'use server';

import { Scan } from '@/types/scan';
import { readFileSync, readdirSync } from 'node:fs';

export async function getScans() {
  const scans: Scan[] = [];
  const files = await readdirSync('scans');
  for (const file of files) {
    const data = await readFileSync(`scans/${file}`);
    const scan = JSON.parse(Buffer.from(data).toString());
    scans.push({
      id: scan.id,
      timestamp: scan.date,
      openIssues: scan.openIssues,
      totalResources: scan.totalResources
    });
  }
  return scans;
}
