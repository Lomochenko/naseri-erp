<template>
  <div v-if="show" :class="['rounded-xl border p-4 mb-4', variantClasses[variant].container]">
    <div class="flex items-start gap-3">
      <div :class="['-mt-0.5', variantClasses[variant].icon]">
        <!-- Success Icon -->
        <svg v-if="variant === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <!-- Error Icon -->
        <svg v-else-if="variant === 'error'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <!-- Warning Icon -->
        <svg v-else-if="variant === 'warning'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <!-- Info Icon -->
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      <div class="flex-1">
        <h4 class="mb-1 text-sm font-semibold text-gray-800 dark:text-white/90">
          {{ title }}
        </h4>

        <p class="text-sm text-gray-500 dark:text-gray-400">{{ message }}</p>
      </div>

      <!-- Close Button -->
      <button v-if="closable" @click="$emit('close')" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  show: {
    type: Boolean,
    default: true
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const variantClasses = {
  success: {
    container: 'border-green-500 bg-green-50 dark:border-green-500/30 dark:bg-green-500/15',
    icon: 'text-green-500',
  },
  error: {
    container: 'border-red-500 bg-red-50 dark:border-red-500/30 dark:bg-red-500/15',
    icon: 'text-red-500',
  },
  warning: {
    container: 'border-yellow-500 bg-yellow-50 dark:border-yellow-500/30 dark:bg-yellow-500/15',
    icon: 'text-yellow-500',
  },
  info: {
    container: 'border-blue-500 bg-blue-50 dark:border-blue-500/30 dark:bg-blue-500/15',
    icon: 'text-blue-500',
  },
}


</script>
