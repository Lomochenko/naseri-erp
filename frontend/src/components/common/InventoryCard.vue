<template>
  <div class="outer">
    <div class="card" :class="cardClass">
      <div class="ray"></div>
      <div class="text">{{ formatValue(value) }}</div>
      <div class="label">{{ label }}</div>
      
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
  return value.toString()
}

const cardClass = computed(() => {
  return {
    'card-success': props.type === 'success',
    'card-warning': props.type === 'warning',
    'card-danger': props.type === 'danger',
    'card-total': props.type === 'total'
  }
})
</script>

<style scoped>
  .outer {
    width: 100%;
    max-width: 300px;
    height: 250px;
    border-radius: 10px;
    padding: 1px;
    background: radial-gradient(circle 230px at 0% 0%, inherit, inherit);
    position: relative;
    margin: 0 auto;
  }
  .card {
    z-index: 1;
    width: 100%;
    height: 100%;
    border-radius: 9px;
    border: solid 1px #202222;
    background-size: 20px 20px;
    background: radial-gradient(circle 280px at 0% 0%, #444444, #0c0d0d);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-direction: column;
    color: #fff;
    transition: all 0.3s ease;
  }

  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
  }

  .ray {
    width: 220px;
    height: 45px;
    border-radius: 100px;
    position: absolute;
    background-color: #c7c7c7;
    opacity: 0.4;
    box-shadow: 0 0 50px #fff;
    filter: blur(10px);
    transform-origin: 10%;
    top: 0%;
    left: 0;
    transform: rotate(40deg);
  }

  .card .text {
    font-weight: bolder;
    font-size: 4rem;
    background: linear-gradient(45deg, #000000 4%, #fff, #000);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 10px;
  }

  .label {
    font-size: 1rem;
    font-weight: 500;
    opacity: 0.9;
    text-align: center;
  }

  .line {
    position: absolute;
    background-color: #2c2c2c;
    opacity: 0.6;
  }

  .topl {
    top: 10%;
    left: 10%;
    right: 10%;
    height: 1px;
    background: linear-gradient(90deg, #bdbcbc 30%, #688080 70%);
  }

  .bottoml {
    bottom: 10%;
    left: 10%;
    right: 10%;
    height: 1px;
  }

  .leftl {
    left: 10%;
    top: 10%;
    bottom: 10%;
    width: 1px;
    background: linear-gradient(180deg, #747474 30%, #222424 70%);
  }

  .rightl {
    right: 10%;
    top: 10%;
    bottom: 10%;
    width: 1px;
  }

  /* Different color schemes for different types */
  .card-success .text {
    background: linear-gradient(45deg, #10b981 4%, #34d399, #10b981);
    background-clip: text;
    -webkit-background-clip: text;
  }

  .card-success .ray {
    background-color: #10b981;
    box-shadow: 0 0 50px #10b981;
  }

  .card-warning .text {
    background: linear-gradient(45deg, #f59e0b 4%, #fbbf24, #f59e0b);
    background-clip: text;
    -webkit-background-clip: text;
  }

  .card-warning .ray {
    background-color: #f59e0b;
    box-shadow: 0 0 50px #f59e0b;
  }

  .card-danger .text {
    background: linear-gradient(45deg, #ef4444 4%, #f87171, #ef4444);
    background-clip: text;
    -webkit-background-clip: text;
  }

  .card-danger .ray {
    background-color: #ef4444;
    box-shadow: 0 0 50px #ef4444;
  }

  .card-total .text {
    background: linear-gradient(45deg, #3b82f6 4%, #60a5fa, #3b82f6);
    background-clip: text;
    -webkit-background-clip: text;
  }

  .card-total .ray {
    background-color: #3b82f6;
    box-shadow: 0 0 50px #3b82f6;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .outer {
      max-width: 280px;
      height: 200px;
    }

    .card .text {
      font-size: 3rem;
    }

    .label {
      font-size: 0.9rem;
    }

    .ray {
      width: 180px;
      height: 35px;
    }
  }

  @media (max-width: 480px) {
    .outer {
      max-width: 250px;
      height: 180px;
    }

    .card .text {
      font-size: 2.5rem;
    }

    .label {
      font-size: 0.8rem;
    }

    .ray {
      width: 150px;
      height: 30px;
    }
  }
</style>
