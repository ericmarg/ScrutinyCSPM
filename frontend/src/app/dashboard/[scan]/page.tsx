'use client';
import { Container } from '@mui/system';
import { PageTitle } from '@/components/page-title';
import { faKey } from '@fortawesome/free-solid-svg-icons';
import { FileUpload } from '@/components/file-upload';
import { usePathname, useRouter } from 'next/navigation';

export default async function PrivateKey() {
  const router = useRouter();
  const path = usePathname();
  const scanId = path.split('/')[2];
  return (
    <Container>
      <PageTitle title="Upload your Private Key" icon={faKey} />
      <FileUpload
        onChange={async ([file]) => {
          const formData = new FormData();
          formData.append('private_key', file);
          formData.append('scan_id', scanId);
          await fetch('/api/upload', {
            method: 'POST',
            body: formData
          }).then(() => {
            router.push(`${path}/results`);
          });
        }}
        caption="Upload your private key"
        error={false}
        sx={{ width: '100%' }}
      />
    </Container>
  );
}
