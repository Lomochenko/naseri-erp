<template>
  <v-card class="mb-4" variant="outlined">
    <v-card-title class="text-subtitle-1">دسترسی سریع به بخش‌های انبار</v-card-title>
    <v-card-text>
      <v-alert type="info" variant="tonal" density="compact" class="mb-3">
        به دلیل وجود مشکل فنی در ناوبری، از این بخش برای دسترسی مستقیم به بخش‌های مختلف انبار استفاده کنید.
      </v-alert>
      
      <v-btn-group variant="outlined" class="d-flex flex-wrap">
        <v-btn
          :color="route.name === 'inventory' ? 'primary' : ''"
          class="flex-grow-1"
          @click="navigateTo('inventory')"
        >
          موجودی کالا
        </v-btn>
        <v-btn
          :color="route.name === 'inventory-transaction' ? 'primary' : ''"
          class="flex-grow-1"
          @click="navigateTo('inventory-transaction')"
        >
          ثبت تراکنش
        </v-btn>
        <v-btn
          :color="route.name === 'inventory-transfer' ? 'primary' : ''"
          class="flex-grow-1"
          @click="navigateTo('inventory-transfer')"
        >
          انتقال بین انبارها
        </v-btn>
        <v-btn
          :color="route.name === 'transaction-history' ? 'primary' : ''"
          class="flex-grow-1"
          @click="navigateTo('transaction-history')"
        >
          تاریخچه تراکنش‌ها
        </v-btn>
        <v-btn
          :color="route.name === 'warehouse-management' ? 'primary' : ''"
          class="flex-grow-1"
          @click="navigateTo('warehouse-management')"
        >
          مدیریت انبارها
        </v-btn>
      </v-btn-group>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const navigateTo = (routeName) => {
  console.log('InventoryNavigator: Navigating to', routeName);
  router.push({ name: routeName }).catch(err => {
    console.error('Navigation failed:', err);
    // راه‌حل جایگزین
    window.location.href = router.resolve({ name: routeName }).href;
  });
};
</script>

<style scoped>
.v-btn-group {
  flex-wrap: wrap;
}
.v-btn-group .v-btn {
  margin: 2px;
}
</style> 