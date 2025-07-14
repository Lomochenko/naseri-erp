<template>
  <div class="rounded-lg bg-green-50 border border-green-200 p-4 dark:bg-green-900/20 dark:border-green-800">
    <div class="flex items-center">
      <svg class="h-5 w-5 text-green-400 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div class="flex-1">
        <h3 class="text-sm font-medium text-green-800 dark:text-green-200">
          موفق
        </h3>
        <p class="mt-1 text-sm text-green-700 dark:text-green-300">
          {{ message }}
        </p>
      </div>
      <button
        v-if="dismissible"
        @click="$emit('dismiss')"
        class="text-green-400 hover:text-green-600 dark:text-green-300 dark:hover:text-green-100"
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    required: true
  },
  dismissible: {
    type: Boolean,
    default: true
  }
})

defineEmits(['dismiss'])
</script>
