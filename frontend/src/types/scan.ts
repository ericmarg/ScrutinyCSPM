export interface Scan {
  id: string;
  timestamp: string;
  inventory: Record<string, ProviderInfo>;
  totalResources: number;
}

export interface ProviderInfo {
  account: string;
}
