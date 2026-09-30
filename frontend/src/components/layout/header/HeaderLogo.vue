<template>
  <router-link to="/" class="lg:hidden">
    <h1 class="text-title-md2 font-bold text-black dark:text-white">
      {{ brand.dashboardName }}
    </h1>
  </router-link>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { brand } from '@/config/brand'
</script>
