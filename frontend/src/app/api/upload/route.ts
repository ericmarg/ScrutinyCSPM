import * as fs from 'node:fs';
import { NextResponse } from 'next/server';
import { pipeline } from 'node:stream/promises';

export async function POST(req: any) {
  try {
    const data = await req.formData();
    const file = data.get('private_key');
    const scanId = data.get('scan_id');
    const fileName = scanId + '.pem';
    const filePath = 'scans/keys/' + fileName;
    if (!fs.existsSync('scans/keys')) {
      fs.mkdirSync('scans/keys', { recursive: true });
    }
    await pipeline(
      file.stream(), // Read from the file stream
      fs.createWriteStream(filePath) // Write to a new file in the filesystem
    );
    return NextResponse.json({ status: 'success', data: 'File uploaded successfully' });
  } catch (e) {
    return NextResponse.json({ status: 'fail', data: e });
  }
}
