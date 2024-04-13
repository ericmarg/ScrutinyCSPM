'use server';

import { Scan } from '@/types/scan';
import { statSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { ScanListItem } from '@/types/scan-list-item';

export async function getScans() {
  const scans: ScanListItem[] = [];
  try {
    const files = readdirSync('scans');

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const filePath = path.join('scans', file);
      const stats = statSync(filePath);
      scans.push({
        id: i,
        name: file,
        date: stats.birthtime
      });
    }
    return scans;
  } catch (error) {
    return [];
  }
}
