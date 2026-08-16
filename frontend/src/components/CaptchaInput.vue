<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getCaptchaImage, createCaptcha } from "@/api/auth";

const captchaId = ref("");
const captchaCode = ref("");
const imgUrl = ref("");
const loading = ref(false);

const emit = defineEmits<{
  (e: "update:captchaId", v: string): void;
  (e: "update:captchaCode", v: string): void;
}>();

async function refreshCaptcha() {
  loading.value = true;
  try {
    const resp = await createCaptcha();
    captchaId.value = resp.captcha_id;
    imgUrl.value = getCaptchaImage(resp.captcha_id);
    captchaCode.value = "";
    emit("update:captchaId", captchaId.value);
    emit("update:captchaCode", captchaCode.value);
  } catch {
    // 静默失败，用户可点击重试
  } finally {
    loading.value = false;
  }
}

function onInput(v: string) {
  captchaCode.value = v;
  emit("update:captchaCode", v);
}

onMounted(() => {
  refreshCaptcha();
});
</script>

<template>
  <div class="captcha-row">
    <a-input
      :value="captchaCode"
      placeholder="输入图中字符"
      size="large"
      maxlength="6"
      allow-clear
      @update:value="onInput"
      @pressEnter="$emit('update:captchaCode', captchaCode)"
    />
    <div class="captcha-img-wrap" @click="refreshCaptcha" title="点击换一张">
      <img v-if="imgUrl" :src="imgUrl" alt="验证码" class="captcha-img" />
      <div v-else class="captcha-loading">加载中...</div>
    </div>
  </div>
</template>

<style scoped>
.captcha-row {
  display: flex;
  gap: 8px;
  align-items: center;
}
.captcha-img-wrap {
  flex-shrink: 0;
  width: 120px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e8e8e8;
  transition: border-color 200ms;
}
.captcha-img-wrap:hover {
  border-color: var(--color-primary);
}
.captcha-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.captcha-loading {
  font-size: 12px;
  color: #999;
}
</style>
