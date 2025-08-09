<template>
  <div
    class="relative h-[10em] w-full border-2 rounded-[1.5em] text-white font-nunito p-[1.5em] flex justify-center items-left flex-col gap-[1em] backdrop-blur-[12px] hover:shadow-2xl transition-all duration-500 group/card hover:-translate-y-1"
    :class="[cardBackgroundClass, cardBorderClass, cardShadowClass]"
  >
    <div
      class="absolute inset-0 opacity-0 group-hover/card:opacity-100 transition-opacity duration-500 rounded-[1.5em]"
      :class="cardHoverOverlayClass"
    ></div>
    <div
      class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,50,190,0.1),transparent_60%)] group-hover/card:animate-pulse"
    ></div>

    <div class="absolute top-4 right-4 flex gap-2">
      <div class="w-2 h-2 rounded-full" :class="dotClass1"></div>
      <div class="w-2 h-2 rounded-full" :class="dotClass2"></div>
      <div class="w-2 h-2 rounded-full" :class="dotClass3"></div>
    </div>

    <div
      class="relative z-10 transition-transform duration-300 group-hover/card:translate-y-[-2px] space-y-3"
    >
      <h1
        class="text-[2.2em] text-center font-bold bg-gradient-to-r bg-clip-text text-transparent"
        :class="headingGradientClass"
      >
        {{ formatValue(value) }}
      </h1>
      <p class="text-[1rem]  text-center leading-relaxed " :class="textColorClass">
        {{ label }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  label: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'total',
    validator: (value) => ['total', 'success', 'warning', 'danger'].includes(value)
  }
})

const formatValue = (value) => {
  if (value >= 1000000) {
    return Math.floor(value / 1000000) + 'M'
  } else if (value >= 1000) {
    return Math.floor(value / 1000) + 'K'
  }
  return value?.toString() || '0'
}

// Color themes based on card type
const cardBackgroundClass = computed(() => {
  switch(props.type) {
    case 'success': return 'bg-gradient-to-br from-[rgba(22,163,74,1)] via-green-700/80 to-[rgba(22,163,74,0.2)]' // Green
    case 'warning': return 'bg-gradient-to-br from-[rgba(202,138,4,1)] via-yellow-600/80 to-[rgba(202,138,4,0.2)]' // Yellow
    case 'danger': return 'bg-gradient-to-br from-[rgba(220,38,38,1)] via-red-600/80 to-[rgba(220,38,38,0.2)]' // Red
    case 'total': return 'bg-gradient-to-br from-[rgba(37,99,235,1)] via-blue-700/80 to-[rgba(37,99,235,0.2)]' // Blue
    default: return 'bg-gradient-to-br from-[rgba(75,30,133,1)] via-purple-700/80 to-[rgba(75,30,133,0.2)]'
  }
})

const cardBorderClass = computed(() => {
  switch(props.type) {
    case 'success': return 'border-[rgba(22,163,74,0.5)]'
    case 'warning': return 'border-[rgba(202,138,4,0.5)]'
    case 'danger': return 'border-[rgba(220,38,38,0.5)]'
    case 'total': return 'border-[rgba(37,99,235,0.5)]'
    default: return 'border-[rgba(75,30,133,0.5)]'
  }
})

const cardShadowClass = computed(() => {
  switch(props.type) {
    case 'success': return 'hover:shadow-green-500/30'
    case 'warning': return 'hover:shadow-yellow-500/30'
    case 'danger': return 'hover:shadow-red-500/30'
    case 'total': return 'hover:shadow-blue-500/30'
    default: return 'hover:shadow-purple-500/30'
  }
})

const cardHoverOverlayClass = computed(() => {
  switch(props.type) {
    case 'success': return 'bg-gradient-to-br from-green-600/30 via-emerald-500/20 to-transparent'
    case 'warning': return 'bg-gradient-to-br from-yellow-600/30 via-amber-500/20 to-transparent'
    case 'danger': return 'bg-gradient-to-br from-red-600/30 via-rose-500/20 to-transparent'
    case 'total': return 'bg-gradient-to-br from-blue-600/30 via-sky-500/20 to-transparent'
    default: return 'bg-gradient-to-br from-purple-600/30 via-fuchsia-500/20 to-transparent'
  }
})

const dotClass1 = computed(() => {
  switch(props.type) {
    case 'success': return 'bg-green-300/50'
    case 'warning': return 'bg-yellow-300/50'
    case 'danger': return 'bg-red-300/50'
    case 'total': return 'bg-blue-300/50'
    default: return 'bg-purple-300/50'
  }
})

const dotClass2 = computed(() => {
  switch(props.type) {
    case 'success': return 'bg-green-300/30'
    case 'warning': return 'bg-yellow-300/30'
    case 'danger': return 'bg-red-300/30'
    case 'total': return 'bg-blue-300/30'
    default: return 'bg-purple-300/30'
  }
})

const dotClass3 = computed(() => {
  switch(props.type) {
    case 'success': return 'bg-green-300/10'
    case 'warning': return 'bg-yellow-300/10'
    case 'danger': return 'bg-red-300/10'
    case 'total': return 'bg-blue-300/10'
    default: return 'bg-purple-300/10'
  }
})

const headingGradientClass = computed(() => {
  switch(props.type) {
    case 'success': return 'from-white via-green-100 to-green-200'
    case 'warning': return 'from-white via-yellow-100 to-yellow-200'
    case 'danger': return 'from-white via-red-100 to-red-200'
    case 'total': return 'from-white via-blue-100 to-blue-200'
    default: return 'from-white via-purple-100 to-purple-200'
  }
})

const textColorClass = computed(() => {
  switch(props.type) {
    case 'success': return 'text-green-100/90'
    case 'warning': return 'text-yellow-100/90'
    case 'danger': return 'text-red-100/90'
    case 'total': return 'text-blue-100/90'
    default: return 'text-purple-100/90'
  }
})
</script>

<style scoped>
/* Responsive design */
@media (max-width: 1200px) {
  .responsive-height {
    @apply h-[16em];
  }
}

@media (max-width: 768px) {
  .responsive-height {
    @apply h-[14em];
  }
  .responsive-text {
    @apply text-[1.8em];
  }
}

@media (max-width: 480px) {
  .responsive-height {
    @apply h-[12em];
  }
  .responsive-text {
    @apply text-[1.5em];
  }
  .responsive-padding {
    @apply p-[1em];
  }
}

/* Responsive grid layout */
.parent-container {
  display: grid;
  grid-template-columns: repeat(1, 1fr); /* Default: 1 card per row */
  gap: 1rem;
}

@media (max-width: 768px) {
  .parent-container {
    grid-template-columns: repeat(2, 1fr); /* 2 cards per row on mobile */
  }
}

@media (max-width: 1200px) {
  .parent-container {
    grid-template-columns: repeat(3, 1fr); /* 3 cards per row on tablets */
  }
}
</style>
