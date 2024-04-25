'use server';
import { exec } from "node:child_process";
import { Scan } from '@/types/scan';

export async function getScan(id: string) {
  try {
    const pythonProcess = exec(`python ../cli/main.py `);
    pythonProcess.kill();
    return null;
  } catch (error) {
    return {};
  }
}
