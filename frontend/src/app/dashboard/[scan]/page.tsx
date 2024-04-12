'use client';
import { Container } from '@mui/system';
import { PageTitle } from '@/components/page-title';
import { faKey } from '@fortawesome/free-solid-svg-icons';
import { FileUpload } from '@/components/file-upload';
import { usePathname, useRouter } from 'next/navigation';

export default async function PrivateKey() {
  const router = useRouter();
  const path = usePathname();
  return (
    <Container>
      <PageTitle title="Upload your Private Key" icon={faKey} />
      <FileUpload
        onChange={() => {
          router.push(`${path}/results`);
        }}
        caption="Upload your private key"
        error={false}
        sx={{ width: '100%' }}
      />
    </Container>
  );
}
