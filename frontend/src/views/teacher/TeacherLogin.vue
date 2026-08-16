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

const account = ref("");
const password = ref("");
const captchaId = ref("");
const captchaCode = ref("");
const loading = ref(false);

async function submit() {
  if (loading.value) return;
  if (!account.value.trim() || !password.value) {
    message.warning("请输入工号和密码");
    return;
  }
  if (!captchaCode.value) {
    message.warning("请输入验证码");
    return;
  }
  loading.value = true;
  try {
    const data = await login({
      mode: "teacher",
      account: account.value.trim(),
      credential: password.value,
      captcha_id: captchaId.value,
      captcha_code: captchaCode.value,
    });
    auth.setAuth(data);
    message.success("登录成功");
    router.push("/teacher/students");
  } catch (e) {
    message.error(extractErrorMessage(e, "登录失败"));
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="teacher-login-wrap">
    <div class="teacher-login-card teacher-card">
      <div class="header">
        <div class="brand">
          <BrandLogo which="teacher" :size="40" />
          <div>
            <div class="name">{{ brand.platformNameTeacher }}</div>
            <div class="tag">教师工作台</div>
          </div>
        </div>
      </div>

      <h2 class="title">老师登录</h2>
      <p class="sub">查看学员诊断结果、推补课工单、二审映射表</p>

      <a-form layout="vertical" @submit.prevent="submit">
        <a-form-item label="工号 / 账号">
          <a-input
            v-model:value="account"
            placeholder="如 T001 / admin"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="密码">
          <a-input-password v-model:value="password" placeholder="登录密码" />
        </a-form-item>
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
          登 录
        </a-button>
      </a-form>

      <div class="footer">
        <router-link to="/student/login">切换到学员端</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.teacher-login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f5f7fa 0%, #eef2f7 100%);
  padding: 24px;
}
.teacher-login-card {
  width: 100%;
  max-width: 420px;
  padding: 32px;
}
.header {
  margin-bottom: 24px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.name {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.3;
}
.tag {
  color: var(--color-text-sub);
  font-size: 13px;
}
.title {
  margin: 0 0 4px;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
}
.sub {
  color: var(--color-text-sub);
  margin-bottom: 20px;
  font-size: 14px;
}
.footer {
  margin-top: 16px;
  text-align: center;
  color: var(--color-text-sub);
  font-size: 12px;
}
.footer a {
  color: var(--color-secondary);
  text-decoration: none;
}
.footer a:hover {
  text-decoration: underline;
}
.dot {
  margin: 0 6px;
}
</style>
