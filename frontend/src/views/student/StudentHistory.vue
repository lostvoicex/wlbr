<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import { getMyHistory } from "@/api/diagnosis";
import { useKpLabelsStore } from "@/stores/kpLabels";
import { extractErrorMessage } from "@/api/client";
import BrandLogo from "@/components/BrandLogo.vue";
import brand from "@/config/brand";

const router = useRouter();
const kpLabels = useKpLabelsStore();

const loading = ref(true);
const items = ref<
  Array<{
    id: number;
    session_type: string;
    syllabus_target: string;
    total_count: number;
    correct_count: number;
    status: string;
    started_at: string;
    finished_at: string | null;
    kp_snapshots: Array<{
      knowledge_point: string;
      correct_count: number;
      total_count: number;
      correct_rate: number;
      mastery_level: string;
    }>;
  }>
>([]);

const typeEmoji: Record<string, string> = {
  diagnosis: "🎯",
  retest_t1: "🌱",
  retest_t2: "🌳",
};

const typeName: Record<string, string> = {
  diagnosis: "闯关挑战",
  retest_t1: "第一次复习",
  retest_t2: "第二次复习",
};

const syllabusLabels: Record<string, string> = {
  scratch_l1: "Scratch 一级",
  scratch_l2: "Scratch 二级",
  scratch_l3: "Scratch 三级",
  scratch_l4: "Scratch 四级",
  cpp_l1: "C++ 一级",
  cpp_l2: "C++ 二级",
  cpp_l3: "C++ 三级",
  cpp_l4: "C++ 四级",
  cpp_l5: "C++ 五级",
  cpp_l6: "C++ 六级",
  cpp_l7: "C++ 七级",
  cpp_l8: "C++ 八级",
  python_l1: "Python 一级",
  python_l2: "Python 二级",
  python_l3: "Python 三级",
  python_l4: "Python 四级",
  python_l5: "Python 五级",
  python_l6: "Python 六级",
};

function formatDate(text: string): string {
  if (!text) return "";
  const d = new Date(text);
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}

function getScoreStars(correct: number, total: number): string {
  if (total === 0) return "☆☆☆☆☆";
  const rate = correct / total;
  const filled = Math.round(rate * 5);
  return "★".repeat(filled) + "☆".repeat(5 - filled);
}

function getScoreColor(correct: number, total: number): string {
  if (total === 0) return "#6b7280";
  const rate = correct / total;
  if (rate >= 0.8) return "#52c41a";
  if (rate >= 0.5) return "#faad14";
  return "#ff4d4f";
}

function getWeakKpCount(snapshots: Array<{ mastery_level: string }>): number {
  return snapshots.filter((s) => s.mastery_level === "need_repair").length;
}

function viewResult(sessionId: number) {
  router.push(`/student/result/${sessionId}`);
}

function goHome() {
  router.push("/student/home");
}

onMounted(async () => {
  kpLabels.loadOnce();
  try {
    const resp = await getMyHistory();
    items.value = resp.items;
  } catch (e) {
    message.error(extractErrorMessage(e, "记录加载失败，请稍后再试"));
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="kid-app history-page">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="brand-area">
        <BrandLogo which="student" :size="36" />
        <span class="brand-name">{{ brand.platformNameStudent }}</span>
      </div>
      <a-button type="text" class="home-btn" @click="goHome">
        回到首页
      </a-button>
    </div>

    <!-- 标题区 -->
    <div class="title-area">
      <div class="title-emoji">📋</div>
      <h1 class="page-title">我的闯关记录</h1>
      <p class="page-subtitle" v-if="items.length">
        一共完成了 {{ items.length }} 次挑战，继续加油！
      </p>
      <p class="page-subtitle" v-else>
        还没有挑战记录哦，快去首页开始第一次闯关吧！
      </p>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-area">
      <a-spin tip="正在翻找你的记录..." />
    </div>

    <!-- 记录列表 -->
    <div v-else-if="items.length" class="record-list">
      <div
        v-for="item in items"
        :key="item.id"
        class="record-card"
        :class="{ 'is-finished': item.status === 'finished' }"
      >
        <div class="card-left">
          <div class="card-emoji">{{ typeEmoji[item.session_type] || "🎯" }}</div>
        </div>
        <div class="card-body">
          <div class="card-header">
            <span class="card-type">{{ typeName[item.session_type] || item.session_type }}</span>
            <span class="card-syllabus">
              {{ syllabusLabels[item.syllabus_target] || item.syllabus_target }}
            </span>
          </div>
          <div class="card-score">
            <span class="stars" :style="{ color: getScoreColor(item.correct_count, item.total_count) }">
              {{ getScoreStars(item.correct_count, item.total_count) }}
            </span>
            <span class="score-text" :style="{ color: getScoreColor(item.correct_count, item.total_count) }">
              {{ item.correct_count }}/{{ item.total_count }} 题答对
            </span>
          </div>
          <div class="card-meta">
            <span class="meta-date">{{ formatDate(item.started_at) }}</span>
            <span
              v-if="item.status === 'finished' && getWeakKpCount(item.kp_snapshots) > 0"
              class="meta-weak"
            >
              {{ getWeakKpCount(item.kp_snapshots) }} 个知识点需要加油
            </span>
            <span
              v-else-if="item.status === 'finished'"
              class="meta-good"
            >
              全部掌握，太棒了！
            </span>
            <span v-else class="meta-progress">挑战进行中…</span>
          </div>
        </div>
        <div class="card-action" v-if="item.status === 'finished'">
          <button class="view-btn" @click="viewResult(item.id)">
            查看报告
          </button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-area">
      <div class="empty-emoji">🌟</div>
      <p class="empty-title">还没有闯关记录</p>
      <p class="empty-desc">完成第一次挑战后，这里就会显示你的成长足迹啦！</p>
      <button class="start-btn" @click="goHome">
        去闯关
      </button>
    </div>
  </div>
</template>

<style scoped>
.history-page {
  min-height: 100vh;
  padding-bottom: 40px;
}

/* 顶部栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-primary);
}

.home-btn {
  color: var(--color-primary);
  font-weight: 600;
}

/* 标题区 */
.title-area {
  text-align: center;
  padding: 24px 20px 16px;
}

.title-emoji {
  font-size: 48px;
  margin-bottom: 8px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px;
}

.page-subtitle {
  font-size: 14px;
  color: var(--color-text-sub);
  margin: 0;
}

/* 加载 */
.loading-area {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

/* 记录列表 */
.record-list {
  max-width: 640px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: #fff;
  border-radius: var(--radius-md-kid);
  box-shadow: var(--shadow-card-kid);
  transition: transform 0.15s var(--ease-bounce);
}

.record-card:active {
  transform: scale(0.98);
}

.card-left {
  flex-shrink: 0;
}

.card-emoji {
  font-size: 36px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff5ed;
  border-radius: 12px;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.card-type {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text);
}

.card-syllabus {
  font-size: 12px;
  color: var(--color-text-sub);
  background: #f5f5f5;
  padding: 1px 8px;
  border-radius: 999px;
}

.card-score {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.stars {
  font-size: 16px;
  letter-spacing: 2px;
}

.score-text {
  font-size: 13px;
  font-weight: 600;
  font-family: var(--font-num);
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
}

.meta-date {
  color: var(--color-text-sub);
}

.meta-weak {
  color: #ff4d4f;
}

.meta-good {
  color: #52c41a;
  font-weight: 600;
}

.meta-progress {
  color: #1890ff;
}

/* 查看报告按钮 */
.card-action {
  flex-shrink: 0;
}

.view-btn {
  background: var(--color-primary);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.view-btn:hover {
  background: var(--color-primary-hover);
}

/* 空状态 */
.empty-area {
  text-align: center;
  padding: 60px 20px;
}

.empty-emoji {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px;
}

.empty-desc {
  font-size: 14px;
  color: var(--color-text-sub);
  margin: 0 0 24px;
}

.start-btn {
  background: var(--color-primary);
  color: #fff;
  border: none;
  padding: 12px 32px;
  border-radius: 999px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.15s var(--ease-bounce), background 0.2s;
}

.start-btn:hover {
  background: var(--color-primary-hover);
}

.start-btn:active {
  transform: scale(0.95);
}
</style>
