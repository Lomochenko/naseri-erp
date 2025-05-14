<template>
  <div class="d-flex justify-center align-center" style="height: 100vh;">
    <v-card width="400" class="pa-6 mx-auto">
      <div class="text-center mb-6">
        <h1 class="text-h5 font-weight-bold mb-2">سیستم مدیریت یراق‌آلات ناصری</h1>
        <p class="text-subtitle-1">ورود به حساب کاربری</p>
      </div>

      <v-form @submit.prevent="login">
        <v-text-field
          v-model="phoneNumber"
          label="شماره تلفن"
          type="tel"
          required
          variant="outlined"
          prepend-inner-icon="mdi-phone"
          :error-messages="phoneErrors"
          dir="ltr"
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="رمز عبور"
          type="password"
          required
          variant="outlined"
          prepend-inner-icon="mdi-lock"
          :error-messages="passwordErrors"
          dir="ltr"
        ></v-text-field>

        <v-checkbox
          v-model="rememberMe"
          label="مرا به خاطر بسپار"
        ></v-checkbox>

        <v-btn
          block
          color="primary"
          type="submit"
          :loading="authStore.loading"
          class="mt-4"
        >
          ورود به سیستم
        </v-btn>
      </v-form>

      <div class="text-center mt-6">
        <v-alert
          v-if="authStore.error"
          type="error"
          closable
          variant="tonal"
        >
          {{ authStore.error }}
        </v-alert>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../store/auth';

const router = useRouter();
const authStore = useAuthStore();
const phoneNumber = ref('');
const password = ref('');
const rememberMe = ref(false);
const phoneErrors = ref('');
const passwordErrors = ref('');

const validateForm = () => {
  let isValid = true;
  phoneErrors.value = '';
  passwordErrors.value = '';

  // Validate phone number
  if (!phoneNumber.value) {
    phoneErrors.value = 'شماره تلفن الزامی است';
    isValid = false;
  } else if (!/^09\d{9}$/.test(phoneNumber.value)) {
    phoneErrors.value = 'شماره تلفن باید 11 رقم و با 09 شروع شود';
    isValid = false;
  }

  // Validate password
  if (!password.value) {
    passwordErrors.value = 'رمز عبور الزامی است';
    isValid = false;
  } else if (password.value.length < 6) {
    passwordErrors.value = 'رمز عبور باید حداقل 6 کاراکتر باشد';
    isValid = false;
  }

  return isValid;
};

const login = async () => {
  if (!validateForm()) return;
  
  console.log('Attempting login with:', phoneNumber.value, password.value);
  
  try {
    // ارسال اطلاعات لاگین به استور
    const result = await authStore.login({
      phone_number: phoneNumber.value,
      password: password.value
    });
    
    if (result) {
      // در صورت موفقیت، انتقال به صفحه داشبورد
      router.push({ name: 'dashboard' });
    }
  } catch (error) {
    console.error('Login failed:', error);
  }
};
</script> 