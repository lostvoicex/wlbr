<script setup lang="ts">
import { computed } from "vue";
import brand from "@/config/brand";

interface Props {
  which: "student" | "teacher";
  size?: number;
}

const props = withDefaults(defineProps<Props>(), { size: 40 });

const url = computed(() =>
  props.which === "student" ? brand.logoStudent : brand.logoTeacher,
);

const baseStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  flexShrink: 0,
}));

const imgStyle = computed(() => ({
  ...baseStyle.value,
  borderRadius: "50%",
  objectFit: "cover" as const,
}));

const fallbackStyle = computed(() => ({
  ...baseStyle.value,
  borderRadius: "50%",
  background: "#ff7e1a",
  color: "#fff",
  fontWeight: 800,
  fontSize: `${Math.round(props.size * 0.5)}px`,
  lineHeight: 1,
  userSelect: "none" as const,
  boxShadow: "0 2px 6px rgba(255, 126, 26, 0.24)",
}));

const altText = computed(() =>
  props.which === "student" ? "学员端 Logo" : "老师端 Logo",
);
</script>

<template>
  <img v-if="url" :src="url" :alt="altText" :style="imgStyle" />
  <div v-else :style="fallbackStyle">瓦</div>
</template>
