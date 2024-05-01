'use server';

import { statSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { ScanListItem } from '@/types/scan-list-item';

export async function getScans(): Promise<ScanListItem[]> {
  try {
    if (existsSync('scans')) {
      mkdirSync('scans', { recursive: true });
    }
    // Read the scans directory and read the folders
    const folders = readdirSync('scans');
    // Check to see if the folder is valid
    const validScans = folders.filter((folder) => {
      // Check if the folder is a directory
      const isDirectory = statSync(path.join('scans', folder)).isDirectory();
      if (!isDirectory) {
        return false;
      }
      // Check if the folder has a inventory.json file
      const inventory = existsSync(path.join('scans', folder, 'inventory.json'));
      if (!inventory) {
        return false;
      }
      return true;
    });
    return validScans.map((folder): ScanListItem => {
      return {
        id: Number(folder),
        name: folder,
        date: new Date(Number(folder))
      };
    });
  } catch (error) {
    return [];
  }
}
