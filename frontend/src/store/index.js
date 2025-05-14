// استورهای اصلی سیستم
import { useAuthStore } from './auth';
import { useProductsStore } from './products';
import { useInventoryStore } from './inventory';
import { useSalesStore } from './sales';
import { usePurchasesStore } from './purchases';
import { useAccountingStore } from './accounting';

export {
  useAuthStore,
  useProductsStore,
  useInventoryStore,
  useSalesStore,
  usePurchasesStore,
  useAccountingStore
}; 