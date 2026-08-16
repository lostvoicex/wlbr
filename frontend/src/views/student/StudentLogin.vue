<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import { login } from "@/api/auth";
import { extractErrorMessage } from "@/api/client";
import { useAuthStore } from "@/stores/auth";
import BrandLogo from "@/components/BrandLogo.vue";
import CaptchaInput from "@/components/CaptchaInput.vue";
import brand from "@/config/brand";

const router = useRouter();
const auth = useAuthStore();

type Tab = "phone" | "id";
const tab = ref<Tab>("phone");
const loading = ref(false);

const phone = ref("");
const code = ref("");
const studentId = ref("");
const password = ref("");
const captchaId = ref("");
const captchaCode = ref("");

async function submit() {
  if (loading.value) return;
  if (!captchaCode.value) {
    message.warning("请输入验证码");
    return;
  }
  loading.value = true;
  try {
    if (tab.value === "phone") {
      if (!/^1\d{10}$/.test(phone.value)) {
        message.warning("请输入 11 位手机号哦");
        return;
      }
      if (!/^\d{4,6}$/.test(code.value)) {
        message.warning("验证码是 4-6 位数字");
        return;
      }
      const data = await login({
        mode: "student_phone",
        account: phone.value,
        credential: code.value,
        captcha_id: captchaId.value,
        captcha_code: captchaCode.value,
      });
      auth.setAuth(data);
    } else {
      if (!studentId.value.trim() || !password.value) {
        message.warning("请把学号和密码填完整");
        return;
      }
      const data = await login({
        mode: "student_id",
        account: studentId.value.trim(),
        credential: password.value,
        captcha_id: captchaId.value,
        captcha_code: captchaCode.value,
      });
      auth.setAuth(data);
    }
    message.success("欢迎回来，准备好闯关啦！");
    router.push("/student/home");
  } catch (e) {
    message.error(extractErrorMessage(e, "再试一次！"));
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="kid-app center-page">
    <div class="max-w-480 kid-card">
      <div class="logo-row">
        <BrandLogo which="student" :size="56" />
        <div>
          <div class="brand-name">{{ brand.platformNameStudent }}</div>
          <div class="brand-tag">编程闯关小工坊</div>
        </div>
      </div>

      <h1 class="kid-title">你好呀，小小工程师！</h1>
      <p class="kid-subtitle">选一种方式登录，就能开始今天的编程闯关啦～</p>

      <div class="tab-row">
        <button
          class="tab-btn"
          :class="{ active: tab === 'phone' }"
          @click="tab = 'phone'"
          type="button"
        >
          手机号登录
        </button>
        <button
          class="tab-btn"
          :class="{ active: tab === 'id' }"
          @click="tab = 'id'"
          type="button"
        >
          学号登录
        </button>
      </div>

      <a-form layout="vertical" @submit.prevent="submit">
        <template v-if="tab === 'phone'">
          <a-form-item label="家长手机号">
            <a-input
              v-model:value="phone"
              placeholder="11 位手机号"
              size="large"
              maxlength="11"
              allow-clear
            />
          </a-form-item>
          <a-form-item label="验证码">
            <a-input
              v-model:value="code"
              placeholder="4-6 位数字"
              size="large"
              maxlength="6"
              allow-clear
            />
          </a-form-item>
        </template>

        <template v-else>
          <a-form-item label="学号">
            <a-input
              v-model:value="studentId"
              placeholder="老师发给你的学号"
              size="large"
              allow-clear
            />
          </a-form-item>
          <a-form-item label="密码">
            <a-input-password
              v-model:value="password"
              placeholder="小小工程师的秘密口令"
              size="large"
            />
          </a-form-item>
        </template>

        <a-form-item label="图形验证码">
          <CaptchaInput
            @update:captchaId="captchaId = $event"
            @update:captchaCode="captchaCode = $event"
          />
        </a-form-item>

        <a-button
          type="primary"
          block
          :loading="loading"
          html-type="submit"
        >
          出发！开始闯关
        </a-button>

        <div class="switch-row">
          我是老师？
          <router-link to="/teacher/login">这里进老师端</router-link>
        </div>
      </a-form>
    </div>
  </div>
</template>

<style scoped>
.logo-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.logo-badge {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ff7a45 0%, #faad14 100%);
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 16px rgba(255, 122, 69, 0.32);
}
.brand-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
}
.brand-tag {
  color: var(--color-text-sub);
  font-size: 13px;
}
.tab-row {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  background: #fff5eb;
  padding: 4px;
  border-radius: 12px;
}
.tab-btn {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 12px;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-sub);
  border-radius: 10px;
  cursor: pointer;
  transition: all 200ms var(--ease-bounce);
  font-family: inherit;
}
.tab-btn.active {
  background: #fff;
  color: var(--color-primary);
  box-shadow: 0 2px 6px rgba(255, 122, 69, 0.16);
}
.switch-row {
  margin-top: 16px;
  text-align: center;
  color: var(--color-text-sub);
  font-size: 14px;
}
.switch-row a {
  color: var(--color-secondary);
  font-weight: 600;
  text-decoration: none;
}
.switch-row a:hover {
  text-decoration: underline;
}
</style>
