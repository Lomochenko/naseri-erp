<template>
  <div class="flex justify-center items-center py-8">
    <div class="relative">
      <div class="h-8 w-8 rounded-full border-4 border-black dark:border-gray-700"></div>
      <div class="absolute top-0 left-0 h-8 w-8 rounded-full border-4 border-gray-300 border-t-transparent animate-spin"></div>
    </div>
    <span v-if="text" class="mr-3 text-sm text-gray-600 dark:text-gray-400">{{ text }}</span>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: 'در حال بارگذاری...'
  }
})
</script>
