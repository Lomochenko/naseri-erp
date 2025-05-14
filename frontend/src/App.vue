<script setup>
import { computed, ref } from 'vue';
import { useAuthStore } from './store/auth';
import { useRoute, useRouter } from 'vue-router';

const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

// Check if current route is login page or error page to hide layout
const isAuthPage = computed(() => 
  route.path === '/login' || 
  route.path === '/register' || 
  route.path === '/forgot-password' ||
  route.path.includes('/error/'));

// Get user's full name for display
const userFullName = computed(() => {
  if (authStore.user) {
    return authStore.user.first_name && authStore.user.last_name 
      ? `${authStore.user.first_name} ${authStore.user.last_name}`
      : authStore.user.phone_number || 'کاربر سیستم';
  }
  return 'کاربر سیستم';
});

// تنظیمات درکشوی ناوبری
const drawer = ref(true);
const rail = ref(false);

// مدیریت وضعیت تم (روشن/تاریک)
const isDarkTheme = ref(localStorage.getItem('darkTheme') === 'true');

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value;
  localStorage.setItem('darkTheme', isDarkTheme.value);
};

// Handle logout
const logout = () => {
  authStore.logout();
};
</script>

<template>
  <!-- Login/Error page should not have layout -->
  <v-app :theme="isDarkTheme ? 'dark' : 'light'">
    <template v-if="isAuthPage">
      <router-view></router-view>
    </template>
    
    <!-- Main layout for authenticated pages (Materio-inspired) -->
    <template v-else>
      <!-- Navbar -->
      <v-app-bar elevation="1">
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </template>
        
        <v-app-bar-title>سیستم مدیریت یراق‌آلات ناصری</v-app-bar-title>
        
        <v-spacer></v-spacer>
        
        <!-- تغییر تم -->
        <v-btn icon class="ml-2" @click="toggleTheme">
          <v-icon>{{ isDarkTheme ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
        </v-btn>
        
        <!-- دکمه اعلان‌ها -->
        <v-btn icon class="ml-2">
          <v-icon>mdi-bell-outline</v-icon>
          <v-badge
            content="2"
            color="error"
            floating
            dot
          ></v-badge>
        </v-btn>
        
        <!-- منو کاربر -->
        <v-menu location="bottom end" transition="scale-transition">
          <template v-slot:activator="{ props }">
            <v-btn
              class="ml-2"
              v-bind="props"
              variant="text"
            >
              <v-avatar size="32" color="primary" class="ml-2">
                <span class="text-white">{{ userFullName.substring(0, 2) }}</span>
              </v-avatar>
              {{ userFullName }}
              <v-icon class="mr-2">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          
          <v-card min-width="200" elevation="4">
            <v-list>
              <v-list-item prepend-icon="mdi-account-outline" title="پروفایل" @click="router.push('/profile')"></v-list-item>
              <v-list-item prepend-icon="mdi-cog-outline" title="تنظیمات" @click="router.push('/settings')"></v-list-item>
              <v-divider></v-divider>
              <v-list-item prepend-icon="mdi-logout" title="خروج از سیستم" @click="logout" class="text-error"></v-list-item>
            </v-list>
          </v-card>
        </v-menu>
      </v-app-bar>

      <!-- Sidebar (Materio-style) -->
      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        @mouseenter="rail = false"
        @mouseleave="rail = true"
        elevation="2"
        permanent
      >
        <!-- لوگو -->
        <div class="py-3 px-4 d-flex align-center">
          <v-avatar color="primary" size="32" class="ml-2">
            <span class="text-white font-weight-bold">ن</span>
          </v-avatar>
          <span v-if="!rail" class="text-h6 font-weight-bold">ناصری</span>
          <v-spacer></v-spacer>
          <v-btn
            v-if="!rail"
            variant="text"
            icon="mdi-menu-open"
            size="small"
            @click.stop="rail = true"
          ></v-btn>
        </div>
        
        <v-divider></v-divider>
        
        <!-- منوی اصلی -->
        <v-list nav>
          <v-list-item
            to="/"
            :prepend-icon="'mdi-home-outline'"
            title="داشبورد"
            :active="route.path === '/'"
          ></v-list-item>
          
          <v-list-item
            to="/products"
            :prepend-icon="'mdi-package-variant-closed'"
            title="محصولات"
            :active="route.path.includes('/products')"
          ></v-list-item>
          
          <v-list-item
            to="/inventory"
            :prepend-icon="'mdi-warehouse'"
            title="موجودی انبار"
            :active="route.path.includes('/inventory')"
          ></v-list-item>
          
          <v-list-item
            to="/sales"
            :prepend-icon="'mdi-cart-outline'"
            title="فروش"
            :active="route.path.includes('/sales')"
          ></v-list-item>
          
          <v-list-item
            to="/purchases"
            :prepend-icon="'mdi-cart-plus'"
            title="خرید"
            :active="route.path.includes('/purchases')"
          ></v-list-item>
          
          <v-list-item
            to="/accounting"
            :prepend-icon="'mdi-calculator-variant-outline'"
            title="حسابداری"
            :active="route.path.includes('/accounting')"
          ></v-list-item>
          
          <v-list-group
            v-if="authStore.isAdmin"
            prepend-icon="mdi-cog-outline"
            title="مدیریت سیستم"
          >
            <v-list-item
              to="/settings/users"
              title="مدیریت کاربران"
              :active="route.path.includes('/settings/users')"
            ></v-list-item>
            
            <v-list-item
              to="/settings/roles"
              title="مدیریت نقش‌ها"
              :active="route.path.includes('/settings/roles')"
            ></v-list-item>
            
            <v-list-item
              to="/settings/system"
              title="تنظیمات سیستم"
              :active="route.path.includes('/settings/system')"
            ></v-list-item>
          </v-list-group>
        </v-list>
        
        <template v-slot:append>
          <div class="pa-2">
            <v-btn
              block
              variant="tonal"
              color="primary"
              href="mailto:support@example.com"
              prepend-icon="mdi-lifebuoy"
            >
              پشتیبانی
            </v-btn>
          </div>
        </template>
      </v-navigation-drawer>

      <!-- Main content -->
      <v-main>
        <v-container fluid class="pa-4">
          <router-view></router-view>
        </v-container>
      </v-main>
      
      <!-- نوار وضعیت (footer) -->
      <v-footer class="d-flex flex-column">
        <div class="d-flex justify-space-between align-center py-2 px-4 w-100">
          <div>
            سیستم مدیریت یراق‌آلات ناصری &copy; {{ new Date().getFullYear() }}
          </div>
          <div>
            <v-btn
              v-for="icon in ['mdi-facebook', 'mdi-twitter', 'mdi-instagram']"
              :key="icon"
              :icon="icon"
              variant="text"
              size="small"
            ></v-btn>
          </div>
        </div>
      </v-footer>
    </template>
  </v-app>
</template>

<style>
/* RTL support for Persian language */
html {
  direction: rtl;
  font-family: 'Vazirmatn', sans-serif;
}

/* نوار اسکرول سفارشی */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.05);
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

/* Import Vazirmatn font */
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

/* سایه برای کارت‌ها */
.v-card {
  transition: box-shadow 0.3s ease;
}

.v-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

/* انیمیشن برای دکمه‌ها */
.v-btn {
  transition: transform 0.2s;
}

.v-btn:active {
  transform: scale(0.98);
}
</style>
