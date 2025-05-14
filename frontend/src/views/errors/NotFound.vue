<template>
  <div class="not-found-page">
    <div class="error-container">
      <h1 class="error-code">404</h1>
      <div class="error-divider"></div>
      <h2 class="error-title">صفحه یافت نشد</h2>
      <p class="error-message">
        صفحه‌ای که دنبال آن می‌گردید وجود ندارد یا ممکن است حذف شده باشد.
      </p>
      <router-link to="/" class="return-button">
        بازگشت به صفحه اصلی
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundPage'
}
</script>

<style scoped>
.not-found-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
  font-family: 'Vazirmatn', sans-serif;
}

.error-container {
  text-align: center;
  max-width: 600px;
  background-color: #fff;
  border-radius: 8px;
  padding: 3rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.error-code {
  font-size: 6rem;
  font-weight: 700;
  color: #3182ce;
  margin: 0;
  line-height: 1;
}

.error-divider {
  height: 4px;
  width: 60px;
  background-color: #3182ce;
  margin: 1.5rem auto;
  border-radius: 2px;
}

.error-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #2d3748;
}

.error-message {
  font-size: 1.1rem;
  color: #4a5568;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.return-button {
  display: inline-block;
  background-color: #3182ce;
  color: white;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.return-button:hover {
  background-color: #2b6cb0;
}
</style> 