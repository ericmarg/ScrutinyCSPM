'use server';

import { statSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { ScanListItem } from '@/types/scan-list-item';
import { Scan } from '@/types/scan';
import { readFileSync } from 'fs';

export async function getScan(id: string) {
  let scans: Scan;
  try {
    if (existsSync('scans/keys')) {
      mkdirSync('scans/leys', { recursive: true });
    }
    const keyFile = readFileSync('scans/keys/' + id + '.pem', 'utf8');
    const scanFiles = readdirSync('scans').filter((file) => file.endsWith('.json'));
    const files = scanFiles[Number(id)];
    const filePath = path.join('scans', files);
    const scanFile = readFileSync(filePath, 'utf8');

    return 'test';
  } catch (error) {
    return {};
  }
}
