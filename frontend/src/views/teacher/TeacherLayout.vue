<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import BrandLogo from "@/components/BrandLogo.vue";
import brand from "@/config/brand";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const activeKey = computed(() =>
  route.name ? route.name.toString() : "TeacherStudents",
);

const isAdmin = computed(() => auth.role === "admin");

function go(name: string) {
  router.push({ name });
}

function onMenuClick(info: { key: string | number }) {
  go(String(info.key));
}

function logout() {
  auth.clear();
  router.replace("/teacher/login");
}
</script>

<template>
  <a-layout class="teacher-app" style="min-height: 100vh">
    <a-layout-sider width="220" theme="light" class="sider">
      <div class="brand">
        <BrandLogo which="teacher" :size="36" />
        <div>
          <div class="name">{{ brand.platformNameTeacher }}</div>
          <div class="tag">教师工作台</div>
        </div>
      </div>
      <a-menu
        mode="inline"
        :selected-keys="[activeKey]"
        @click="onMenuClick"
      >
        <a-menu-item key="TeacherStudents">学员列表</a-menu-item>
        <a-menu-item key="TeacherWorkOrders">补课工单</a-menu-item>
        <a-menu-item key="TeacherMappings">映射二审</a-menu-item>
        <a-menu-item key="TeacherTeachers" v-if="isAdmin">教师管理</a-menu-item>
        <a-menu-item key="TeacherDataAdmin" v-if="isAdmin">资料管理</a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout>
      <a-layout-header class="header">
        <div class="header-title">教师工作台</div>
        <div class="header-right">
          <span class="user">{{ auth.subject || "-" }}</span>
          <a-button size="small" @click="logout">退出</a-button>
        </div>
      </a-layout-header>
      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<style scoped>
.sider {
  border-right: 1px solid var(--color-border-teacher);
  padding: 20px 0;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px 20px;
  border-bottom: 1px solid var(--color-border-teacher);
  margin-bottom: 12px;
}
.name {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.25;
}
.tag {
  font-size: 12px;
  color: var(--color-text-sub);
}
.header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border-teacher);
}
.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user {
  color: var(--color-text-sub);
  font-size: 13px;
}
.content {
  padding: 24px;
  background: var(--color-bg-teacher);
}
</style>
