<script setup lang="ts">
import { ConfigProvider, theme as antdTheme } from "ant-design-vue";
import zhCN from "ant-design-vue/es/locale/zh_CN";
import brand from "@/config/brand";

const themeConfig = {
  algorithm: antdTheme.defaultAlgorithm,
  token: {
    colorPrimary: brand.primaryColor,
    colorLink: brand.accentColor,
    colorInfo: brand.accentColor,
    colorSuccess: "#52C41A",
    colorWarning: "#FAAD14",
    colorError: "#FF4D4F",
    borderRadius: 8,
    fontFamily:
      '"PingFang SC", "Microsoft YaHei", -apple-system, sans-serif',
  },
};
</script>

<template>
  <ConfigProvider :locale="zhCN" :theme="themeConfig">
    <RouterView />
  </ConfigProvider>
</template>
