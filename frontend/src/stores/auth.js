import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_superuser === true)
  const isManager = computed(() => user.value?.is_manager === true)

  // Actions
  const login = async (phone, password) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await authAPI.login(phone, password)
      const { token: authToken, user: userData } = response.data

      // Store token and user data
      token.value = authToken
      user.value = userData

      // Persist to localStorage
      localStorage.setItem('auth_token', authToken)
      localStorage.setItem('user_data', JSON.stringify(userData))

      return { success: true }
    } catch (err) {
      console.error('Login error:', err)

      // Handle different types of errors
      let errorMessage = 'خطا در ورود به سیستم'

      if (err.response) {
        // Server responded with error status
        if (err.response.status === 400) {
          errorMessage = 'اطلاعات ورودی نامعتبر است'
        } else if (err.response.status === 401) {
          errorMessage = err.response.data?.error || 'شماره تلفن یا رمز عبور اشتباه است'
        } else if (err.response.status >= 500) {
          errorMessage = 'خطا در سرور. لطفاً دوباره تلاش کنید'
        } else {
          errorMessage = err.response.data?.error || err.response.data?.message || errorMessage
        }
      } else if (err.request) {
        // Network error
        errorMessage = 'خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید'
      }

      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true

    try {
      if (token.value) {
        await authAPI.logout()
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear state and localStorage
      token.value = null
      user.value = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_data')
      isLoading.value = false
    }
  }

  const getCurrentUser = async () => {
    if (!token.value) return

    isLoading.value = true

    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
      localStorage.setItem('user_data', JSON.stringify(response.data))
    } catch (err) {
      console.error('Get current user error:', err)
      // If token is invalid, logout
      if (err.response?.status === 401) {
        await logout()
      }
    } finally {
      isLoading.value = false
    }
  }

  const initializeAuth = () => {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('user_data')

    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        user.value = JSON.parse(storedUser)
      } catch (err) {
        console.error('Error parsing stored user data:', err)
        logout()
      }
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    token,
    isLoading,
    error,

    // Getters
    isAuthenticated,
    isAdmin,
    isManager,

    // Actions
    login,
    logout,
    getCurrentUser,
    initializeAuth,
    clearError,
  }
})
