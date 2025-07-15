<template>
  <AdminLayout>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-6">API Connectivity Test</h1>

      <!-- Login Test -->
      <div class="mb-8 p-4 border rounded-lg">
        <h2 class="text-xl font-semibold mb-4">🔐 Login Test</h2>
        <div class="flex gap-4 mb-4">
          <input
            v-model="loginData.phone"
            placeholder="Phone Number"
            class="border p-2 rounded"
          />
          <input
            v-model="loginData.password"
            type="password"
            placeholder="Password"
            class="border p-2 rounded"
          />
          <button
            @click="testLogin"
            :disabled="isLoading"
            class="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            Test Login
          </button>
        </div>
        <div v-if="loginResult" class="p-2 rounded" :class="loginResult.success ? 'bg-green-100' : 'bg-red-100'">
          {{ loginResult.message }}
        </div>
      </div>

      <!-- API Endpoints Test -->
      <div class="mb-8 p-4 border rounded-lg">
        <h2 class="text-xl font-semibold mb-4">📡 API Endpoints Test</h2>
        <div class="grid grid-cols-2 gap-4">
          <button
            @click="testEndpoint('categories')"
            class="bg-green-500 text-white p-2 rounded"
          >
            Test Categories
          </button>
          <button
            @click="testEndpoint('units')"
            class="bg-green-500 text-white p-2 rounded"
          >
            Test Units
          </button>
          <button
            @click="testEndpoint('products')"
            class="bg-green-500 text-white p-2 rounded"
          >
            Test Products
          </button>
          <button
            @click="testEndpoint('customers')"
            class="bg-green-500 text-white p-2 rounded"
          >
            Test Customers
          </button>
        </div>
      </div>

      <!-- Results -->
      <div class="p-4 border rounded-lg">
        <h2 class="text-xl font-semibold mb-4">📊 Test Results</h2>
        <div class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="(result, index) in testResults"
            :key="index"
            class="p-2 rounded text-sm"
            :class="result.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'"
          >
            <div class="font-semibold">{{ result.endpoint }}</div>
            <div>Status: {{ result.status }}</div>
            <div>{{ result.message }}</div>
            <div v-if="result.data" class="text-xs text-gray-600 mt-1">
              Data: {{ JSON.stringify(result.data).substring(0, 100) }}...
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { authAPI, productsAPI, salesAPI } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useProductsStore } from '@/stores/products'

const isLoading = ref(false)
const loginData = ref({
  phone: '09122173180',
  password: 'Admin@123'
})
const loginResult = ref(null)
const testResults = ref([])
const authToken = ref(null)

const testLogin = async () => {
  isLoading.value = true
  loginResult.value = null

  try {
    console.log('🔐 Testing login with:', loginData.value.phone)
    console.log('📡 API Base URL:', 'http://127.0.0.1:8000/api')

    // Test using auth store
    console.log('🧪 Testing with auth store...')
    const authStore = useAuthStore()
    const result = await authStore.login(loginData.value.phone, loginData.value.password)

    if (result.success) {
      authToken.value = authStore.token
      loginResult.value = {
        success: true,
        message: `✅ Auth store login successful! Token: ${authStore.token.substring(0, 20)}...`
      }

      // Test products API after successful login
      console.log('📦 Testing products API...')
      const productsStore = useProductsStore()
      await productsStore.fetchProducts()

      console.log('Products loaded:', productsStore.products.length)

    } else {
      loginResult.value = {
        success: false,
        message: `❌ Auth store login failed: ${authStore.error}`
      }
    }

  } catch (error) {
    console.error('❌ Login test error:', error)
    loginResult.value = {
      success: false,
      message: `Login failed: ${error.message}`
    }
  } finally {
    isLoading.value = false
  }
}

const testEndpoint = async (endpoint) => {
  const result = {
    endpoint,
    timestamp: new Date().toLocaleTimeString(),
    success: false,
    status: 0,
    message: '',
    data: null
  }

  try {
    let response

    switch (endpoint) {
      case 'categories':
        response = await productsAPI.getCategories()
        break
      case 'units':
        response = await productsAPI.getUnits()
        break
      case 'products':
        response = await productsAPI.getProducts()
        break
      case 'customers':
        response = await salesAPI.getCustomers()
        break
      default:
        throw new Error('Unknown endpoint')
    }

    result.success = true
    result.status = response.status
    result.message = `Success! Found ${response.data.results?.length || response.data.length || 'unknown'} items`
    result.data = response.data

  } catch (error) {
    result.success = false
    result.status = error.response?.status || 0
    result.message = error.response?.data?.detail || error.message || 'Unknown error'
  }

  testResults.value.unshift(result)
}

// Auto-test login on mount
testLogin()
</script>
