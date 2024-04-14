'use server';

import { statSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { ScanListItem } from '@/types/scan-list-item';

export async function getScans() {
  const scans: ScanListItem[] = [];
  try {
    if (existsSync('scans')) {
      mkdirSync('scans', { recursive: true });
    }
    const files = readdirSync('scans').filter((file) => file.endsWith('.json'));

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
