import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Ecommerce.vue'),
      meta: {
        title: 'داشبورد',
        requiresAuth: true,
      },
    },
    {
      path: '/calendar',
      name: 'Calendar',
      component: () => import('../views/Others/Calendar.vue'),
      meta: {
        title: 'Calendar',
      },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Others/UserProfile.vue'),
      meta: {
        title: 'Profile',
      },
    },
    {
      path: '/form-elements',
      name: 'Form Elements',
      component: () => import('../views/Forms/FormElements.vue'),
      meta: {
        title: 'Form Elements',
      },
    },
    {
      path: '/basic-tables',
      name: 'Basic Tables',
      component: () => import('../views/Tables/BasicTables.vue'),
      meta: {
        title: 'Basic Tables',
      },
    },
    {
      path: '/line-chart',
      name: 'Line Chart',
      component: () => import('../views/Chart/LineChart/LineChart.vue'),
    },
    {
      path: '/bar-chart',
      name: 'Bar Chart',
      component: () => import('../views/Chart/BarChart/BarChart.vue'),
    },
    {
      path: '/alerts',
      name: 'Alerts',
      component: () => import('../views/UiElements/Alerts.vue'),
      meta: {
        title: 'Alerts',
      },
    },
    {
      path: '/avatars',
      name: 'Avatars',
      component: () => import('../views/UiElements/Avatars.vue'),
      meta: {
        title: 'Avatars',
      },
    },
    {
      path: '/badge',
      name: 'Badge',
      component: () => import('../views/UiElements/Badges.vue'),
      meta: {
        title: 'Badge',
      },
    },

    {
      path: '/buttons',
      name: 'Buttons',
      component: () => import('../views/UiElements/Buttons.vue'),
      meta: {
        title: 'Buttons',
      },
    },

    {
      path: '/images',
      name: 'Images',
      component: () => import('../views/UiElements/Images.vue'),
      meta: {
        title: 'Images',
      },
    },
    {
      path: '/videos',
      name: 'Videos',
      component: () => import('../views/UiElements/Videos.vue'),
      meta: {
        title: 'Videos',
      },
    },
    {
      path: '/blank',
      name: 'Blank',
      component: () => import('../views/Pages/BlankPage.vue'),
      meta: {
        title: 'Blank',
      },
    },

    {
      path: '/error-404',
      name: '404 Error',
      component: () => import('../views/Errors/FourZeroFour.vue'),
      meta: {
        title: '404 Error',
      },
    },

    {
      path: '/signin',
      name: 'Signin',
      component: () => import('../views/Auth/Signin.vue'),
      meta: {
        title: 'ورود',
      },
    },

    // Products Routes
    {
      path: '/products',
      name: 'Products',
      component: () => import('../views/Products/ProductsList.vue'),
      meta: {
        title: 'محصولات',
        requiresAuth: true,
      },
    },
    {
      path: '/products/create',
      name: 'CreateProduct',
      component: () => import('../views/Products/CreateProduct.vue'),
      meta: {
        title: 'افزودن محصول',
        requiresAuth: true,
      },
    },
    {
      path: '/products/:id/edit',
      name: 'EditProduct',
      component: () => import('../views/Products/EditProduct.vue'),
      meta: {
        title: 'ویرایش محصول',
        requiresAuth: true,
      },
    },

    // Sales Routes
    {
      path: '/sales',
      name: 'Sales',
      component: () => import('../views/Sales/SalesList.vue'),
      meta: {
        title: 'فروش',
        requiresAuth: true,
      },
    },
    {
      path: '/customers',
      name: 'Customers',
      component: () => import('../views/Customers/CustomersList.vue'),
      meta: {
        title: 'مشتریان',
        requiresAuth: true,
      },
    },

    // Inventory Routes
    {
      path: '/inventory',
      name: 'Inventory',
      component: () => import('../views/Inventory/InventoryList.vue'),
      meta: {
        title: 'موجودی',
        requiresAuth: true,
      },
    },

    // Reports Routes
    {
      path: '/reports',
      name: 'Reports',
      component: () => import('../views/Reports/ReportsList.vue'),
      meta: {
        title: 'گزارشات',
        requiresAuth: true,
      },
    },

    // Test Page
    {
      path: '/test',
      name: 'TestPage',
      component: () => import('../views/TestPage.vue'),
      meta: {
        title: 'تست سیستم',
        requiresAuth: true,
      },
    },
  ],
})

export default router

router.beforeEach((to, from, next) => {
  document.title = `یراقالات ناصری - ${to.meta.title || 'سیستم مدیریت'}`

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      next('/signin')
      return
    }
  }

  // Redirect to dashboard if already authenticated and trying to access signin
  if (to.name === 'Signin') {
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
      next('/')
      return
    }
  }

  next()
})
