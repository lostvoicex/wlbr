import { defineStore } from "pinia";
import { ref } from "vue";
import { fetchKpLabels, type KpLabel } from "@/api/kpLabels";

/**
 * KP 童趣化标签 store：把数据库里存的"事件模块 / 循环结构"这类技术味 KP 名
 * 在展示层统一转成小朋友能懂的名字 + 讲解词。
 *
 * - 数据库存储保持原名不变
 * - 前端启动时 loadOnce() 拉一次，缓存到本地内存
 * - 页面用 getDisplay(kp) / getDescription(kp)；找不到就降级为原名
 */
export const useKpLabelsStore = defineStore("kpLabels", () => {
  const labels = ref<Record<string, KpLabel>>({});
  const loaded = ref(false);
  const loading = ref(false);

  async function loadOnce(): Promise<void> {
    if (loaded.value || loading.value) return;
    loading.value = true;
    try {
      const resp = await fetchKpLabels();
      labels.value = resp.map || {};
      loaded.value = true;
    } catch (e) {
      // 降级：labels 保持为空对象，getDisplay 会退回原名
      // eslint-disable-next-line no-console
      console.warn("[kpLabels] 拉取童趣化 KP 标签失败，将展示原名", e);
    } finally {
      loading.value = false;
    }
  }

  function getDisplay(originalName: string): string {
    const item = labels.value[originalName];
    if (item && item.display_name) return item.display_name;
    return originalName;
  }

  function getDescription(originalName: string): string {
    const item = labels.value[originalName];
    if (item && item.description) return item.description;
    return "";
  }

  return {
    labels,
    loaded,
    loading,
    loadOnce,
    getDisplay,
    getDescription,
  };
});
