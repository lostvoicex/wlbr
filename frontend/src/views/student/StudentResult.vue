<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { message } from "ant-design-vue";
import {
  getResult,
  getWeightedResult,
  shareReportToTeacher,
  type ResultResponse,
  type PerKpResult,
  type WeightedKpItem,
} from "@/api/diagnosis";
import { useKpLabelsStore } from "@/stores/kpLabels";
import { useCopyTextsStore } from "@/stores/copyTexts";
import BrandLogo from "@/components/BrandLogo.vue";
import brand from "@/config/brand";

const route = useRoute();
const router = useRouter();

const sessionId = Number(route.params.session_id);
const loading = ref(true);
const data = ref<ResultResponse | null>(null);
const expandMastered = ref(false);
const weightedData = ref<WeightedKpItem[] | null>(null);
const weightedLoading = ref(false);
const kpLabels = useKpLabelsStore();
const copyTexts = useCopyTextsStore();

onMounted(async () => {
  kpLabels.loadOnce();
  copyTexts.loadOnce();
  try {
    data.value = await getResult(sessionId);
  } catch {
    message.error("找不到这次的答题记录，先回主页看看～");
    router.replace("/student/home");
  } finally {
    loading.value = false;
  }
});

const totalRate = computed(() => {
  if (!data.value) return 0;
  return Math.round(Number(data.value.total_rate) * 100);
});

const isRetest = computed(() => {
  if (!data.value) return false;
  return data.value.session_type !== "diagnosis";
});

const retestLabel = computed(() => {
  if (!data.value) return "";
  const map: Record<string, string> = {
    diagnosis: "诊断闯关",
    retest_t1: "复测一（3天后）",
    retest_t2: "复测二（7天后）",
  };
  return map[data.value.session_type] || "";
});

const isLowConfidence = computed(() => {
  if (!data.value) return false;
  if (data.value.total_count <= 2) return true;
  const kps = data.value.per_kp || [];
  if (kps.length === 0) return false;
  return kps.every((k) => k.low_confidence);
});

const badge = computed(() =>
  copyTexts.getBadge(data.value ? data.value.badge : "together"),
);
const badgeSubtitle = computed(() =>
  copyTexts.getBadgeSubtitle(
    data.value ? data.value.badge : "together",
    isLowConfidence.value,
  ),
);

const grouped = computed(() => {
  const g = {
    mastered: [] as PerKpResult[],
    need_review: [] as PerKpResult[],
    need_repair: [] as PerKpResult[],
  };
  if (data.value && data.value.per_kp) {
    data.value.per_kp.forEach((k) => g[k.mastery_level].push(k));
  }
  return g;
});

function formatRate(k: PerKpResult) {
  const r = Math.round(Number(k.correct_rate) * 100);
  return `${k.correct_count}/${k.total_count}（${r}%）`;
}

function formatDate(iso: string | null) {
  if (!iso) return "";
  const d = new Date(iso);
  return `${d.getMonth() + 1}月${d.getDate()}日`;
}

async function shareToTeacher() {
  try {
    const resp = await shareReportToTeacher(sessionId);
    message.success(resp.message || "报告已分享给老师 ✉️");
  } catch {
    message.error("分享失败，请稍后再试～");
  }
}

function printReport() {
  window.print();
}

function backHome() {
  router.replace("/student/home");
}

function startRetest(type: "retest_t1" | "retest_t2") {
  if (!data.value) return;
  router.push(`/student/diagnosis/${data.value.syllabus_target}?type=${type}`);
}

async function loadWeighted() {
  if (!data.value) return;
  weightedLoading.value = true;
  try {
    const resp = await getWeightedResult(data.value.syllabus_target);
    weightedData.value = resp.items || [];
  } catch {
    message.error("总评加载失败，稍后再试～");
  } finally {
    weightedLoading.value = false;
  }
}

const weightedGrouped = computed(() => {
  const g = {
    mastered: [] as WeightedKpItem[],
    need_review: [] as WeightedKpItem[],
    need_repair: [] as WeightedKpItem[],
  };
  if (weightedData.value) {
    weightedData.value.forEach((k) => g[k.mastery_level as keyof typeof g].push(k));
  }
  return g;
});
</script>

<template>
  <div class="kid-app result-app">
    <header class="r-header">
      <div class="brand">
        <BrandLogo which="student" :size="32" />
        <span class="brand-title">{{ brand.platformNameStudent }}</span>
        <span class="brand-sub">· 我的闯关成绩单</span>
      </div>
      <button class="ghost-btn" @click="backHome">↩ 回主页</button>
    </header>

    <main class="r-main" v-if="!loading && data">
      <!-- 顶部得分卡 -->
      <section class="score-card">
        <div v-if="isRetest" class="retest-badge">{{ retestLabel }}</div>
        <div class="badge-emoji">{{ badge.emoji }}</div>
        <div class="score-line">
          你答对了
          <span class="score-num">{{ data.correct_count }}</span>
          / {{ data.total_count }} 题
        </div>
        <div class="rate-line">正确率 {{ totalRate }}%</div>
        <div class="badge-text">{{ badge.title }}！</div>
        <div class="badge-sub">{{ badgeSubtitle }}</div>
      </section>

      <!-- 红：需要重点补的 -->
      <section v-if="grouped.need_repair.length" class="kp-section kp-red">
        <div class="kp-title">🔴 需要重点补的部分</div>
        <div
          v-for="k in grouped.need_repair"
          :key="k.knowledge_point"
          class="kp-card kp-card-red"
        >
          <div class="kp-name">
            {{ kpLabels.getDisplay(k.knowledge_point) }}
            <span v-if="k.low_confidence" class="low-tag">题量少 · 再练几道更准</span>
          </div>
          <div v-if="kpLabels.getDescription(k.knowledge_point)" class="kp-sub">
            {{ kpLabels.getDescription(k.knowledge_point) }}
          </div>
          <div class="kp-meta">答对 {{ formatRate(k) }}</div>
          <div v-if="k.ppt_ref" class="kp-ppt">📖 关联章节：{{ k.ppt_ref }}</div>
          <div v-else class="kp-ppt kp-ppt-empty">📖 关联章节：老师正在整理中</div>
        </div>
      </section>

      <!-- 黄：需要再练练 -->
      <section v-if="grouped.need_review.length" class="kp-section kp-yellow">
        <div class="kp-title">🟡 需要再练练的部分</div>
        <div
          v-for="k in grouped.need_review"
          :key="k.knowledge_point"
          class="kp-card kp-card-yellow"
        >
          <div class="kp-name">
            {{ kpLabels.getDisplay(k.knowledge_point) }}
            <span v-if="k.low_confidence" class="low-tag">题量少 · 再练几道更准</span>
          </div>
          <div v-if="kpLabels.getDescription(k.knowledge_point)" class="kp-sub">
            {{ kpLabels.getDescription(k.knowledge_point) }}
          </div>
          <div class="kp-meta">答对 {{ formatRate(k) }}</div>
          <div v-if="k.ppt_ref" class="kp-ppt">📖 关联章节：{{ k.ppt_ref }}</div>
          <div v-else class="kp-ppt kp-ppt-empty">📖 关联章节：老师正在整理中</div>
        </div>
      </section>

      <!-- 绿：已掌握（默认折叠） -->
      <section v-if="grouped.mastered.length" class="kp-section kp-green">
        <div class="kp-title toggle" @click="expandMastered = !expandMastered">
          🟢 已经掌握的部分（{{ grouped.mastered.length }} 个）
          <span class="toggle-arrow">{{ expandMastered ? "▲" : "▼" }}</span>
        </div>
        <div v-show="expandMastered">
          <div
            v-for="k in grouped.mastered"
            :key="k.knowledge_point"
            class="kp-card kp-card-green"
          >
            <div class="kp-name">
              {{ kpLabels.getDisplay(k.knowledge_point) }}
              <span v-if="k.low_confidence" class="low-tag">题量少 · 再练几道更准</span>
            </div>
            <div v-if="kpLabels.getDescription(k.knowledge_point)" class="kp-sub">
              {{ kpLabels.getDescription(k.knowledge_point) }}
            </div>
            <div class="kp-meta">答对 {{ formatRate(k) }}</div>
            <div v-if="k.ppt_ref" class="kp-ppt">📖 关联章节：{{ k.ppt_ref }}</div>
          </div>
        </div>
      </section>

      <!-- 复测计划 -->
      <section class="retest-card">
        <div class="retest-title">📅 接下来的小任务</div>
        <div class="retest-item">
          <span class="retest-emoji">🌱</span>
          <div class="retest-body">
            <div class="retest-hint">{{ data.retest_plan.t1_hint }}</div>
            <div class="retest-desc">帮我们看看有没有真的记住～</div>
            <div v-if="data.retest_plan.t1_at" class="retest-date">
              计划日期：{{ formatDate(data.retest_plan.t1_at) }}
            </div>
          </div>
          <button
            v-if="data.session_type === 'diagnosis'"
            class="retest-btn"
            @click="startRetest('retest_t1')"
          >
            开始复测一
          </button>
        </div>
        <div class="retest-item">
          <span class="retest-emoji">🌳</span>
          <div class="retest-body">
            <div class="retest-hint">{{ data.retest_plan.t2_hint }}</div>
            <div class="retest-desc">这次通过就说明真的学会啦！</div>
            <div v-if="data.retest_plan.t2_at" class="retest-date">
              计划日期：{{ formatDate(data.retest_plan.t2_at) }}
            </div>
          </div>
          <button
            v-if="data.session_type === 'retest_t1'"
            class="retest-btn"
            @click="startRetest('retest_t2')"
          >
            开始复测二
          </button>
        </div>
      </section>

      <!-- T2 完成后：加权总评 -->
      <section v-if="data.session_type === 'retest_t2'" class="retest-card weighted-card">
        <div class="retest-title">📊 综合总评（诊断 + 复测加权）</div>
        <div v-if="!weightedData && !weightedLoading" class="weighted-intro">
          把诊断和两次复测的成绩加在一起算，看看最后到底掌握得怎么样～
        </div>
        <button
          v-if="!weightedData && !weightedLoading"
          class="retest-btn"
          @click="loadWeighted"
        >
          查看总评
        </button>
        <div v-if="weightedLoading" class="loading-box">📊 正在计算总评…</div>
        <div v-if="weightedData" class="weighted-results">
          <div v-if="weightedGrouped.need_repair.length" class="w-group">
            <div class="w-group-title">🔴 还需要补一补</div>
            <div
              v-for="k in weightedGrouped.need_repair"
              :key="k.knowledge_point"
              class="w-item"
            >
              <span class="w-kp">{{ kpLabels.getDisplay(k.knowledge_point) }}</span>
              <span class="w-rate">{{ Math.round(k.weighted_rate * 100) }}%</span>
            </div>
          </div>
          <div v-if="weightedGrouped.need_review.length" class="w-group">
            <div class="w-group-title">🟡 基本掌握了</div>
            <div
              v-for="k in weightedGrouped.need_review"
              :key="k.knowledge_point"
              class="w-item"
            >
              <span class="w-kp">{{ kpLabels.getDisplay(k.knowledge_point) }}</span>
              <span class="w-rate">{{ Math.round(k.weighted_rate * 100) }}%</span>
            </div>
          </div>
          <div v-if="weightedGrouped.mastered.length" class="w-group">
            <div class="w-group-title">🟢 完全掌握</div>
            <div
              v-for="k in weightedGrouped.mastered"
              :key="k.knowledge_point"
              class="w-item"
            >
              <span class="w-kp">{{ kpLabels.getDisplay(k.knowledge_point) }}</span>
              <span class="w-rate">{{ Math.round(k.weighted_rate * 100) }}%</span>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <div class="cta-row">
        <button class="cta-btn primary" @click="shareToTeacher">
          ✉️ 把这份报告分享给老师
        </button>
        <button class="cta-btn secondary" @click="printReport">
          🖨 打印报告
        </button>
      </div>
    </main>

    <div v-else class="loading-box">📖 成绩单正在整理…</div>
  </div>
</template>

<style scoped>
.result-app {
  min-height: 100vh;
  background: var(--color-bg);
  padding-bottom: 40px;
}
.r-header {
  padding: 16px 20px;
  background: #fff;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 16px;
  color: var(--color-text);
  flex-wrap: wrap;
}
.brand-title {
  font-weight: 700;
}
.brand-sub {
  color: var(--color-text-sub);
  font-weight: 500;
  font-size: 14px;
}
.ghost-btn {
  background: none;
  border: 1.5px solid var(--color-border);
  color: var(--color-text-sub);
  padding: 6px 14px;
  border-radius: 999px;
  cursor: pointer;
  font-family: inherit;
  font-size: 14px;
}
.ghost-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.r-main {
  max-width: 640px;
  margin: 0 auto;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.loading-box {
  padding: 80px 12px;
  text-align: center;
  color: var(--color-text-sub);
  font-size: 18px;
}

.score-card {
  background: linear-gradient(135deg, #fff2e8 0%, #ffe0c2 100%);
  border-radius: var(--radius-lg);
  padding: 26px 20px 24px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(255, 122, 69, 0.16);
}
.retest-badge {
  display: inline-block;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 14px;
  border-radius: 999px;
  margin-bottom: 10px;
}
.badge-emoji {
  font-size: 60px;
  line-height: 1;
  margin-bottom: 4px;
}
.score-line {
  font-size: 18px;
  color: var(--color-text-sub);
}
.score-num {
  font-size: 40px;
  font-weight: 800;
  color: var(--color-primary);
  margin: 0 4px;
  vertical-align: -4px;
}
.rate-line {
  margin-top: 6px;
  font-size: 15px;
  color: var(--color-text-sub);
}
.badge-text {
  margin-top: 10px;
  font-size: 22px;
  font-weight: 800;
  color: var(--color-primary);
}
.badge-sub {
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-sub);
  padding: 0 4px;
}

.kp-section {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 16px 16px 8px;
  border-left: 4px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.kp-red {
  border-left-color: var(--color-weak);
}
.kp-yellow {
  border-left-color: var(--color-warn);
}
.kp-green {
  border-left-color: var(--color-pass);
}
.kp-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.kp-title.toggle {
  cursor: pointer;
  user-select: none;
}
.toggle-arrow {
  font-size: 13px;
  color: var(--color-text-sub);
}

.kp-card {
  padding: 12px 14px;
  border-radius: var(--radius-md);
  margin-bottom: 10px;
  border: 1.5px solid var(--color-border);
}
.kp-card-red {
  background: #fff1f0;
  border-color: #ffccc7;
}
.kp-card-yellow {
  background: #fffbe6;
  border-color: #ffe58f;
}
.kp-card-green {
  background: #f6ffed;
  border-color: #b7eb8f;
}
.kp-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 6px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}
.kp-sub {
  font-size: 13px;
  color: var(--color-text-sub);
  margin-bottom: 8px;
  line-height: 1.5;
  padding: 6px 10px;
  background: #fffaf3;
  border-radius: 10px;
  border-left: 3px solid var(--color-accent);
}
.low-tag {
  font-size: 12px;
  color: #ad6800;
  background: #fff7e6;
  border: 1px solid #ffd591;
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 500;
}
.kp-meta {
  font-size: 14px;
  color: var(--color-text-sub);
  margin-bottom: 4px;
}
.kp-ppt {
  font-size: 13px;
  color: #7a3a00;
  background: #fff2e8;
  border-radius: 8px;
  padding: 6px 10px;
  margin-top: 4px;
  display: inline-block;
}
.kp-ppt-empty {
  color: var(--color-text-sub);
  background: #f5f5f5;
}

.retest-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 16px 18px 14px;
  border-left: 4px solid var(--color-secondary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.retest-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 12px;
}
.retest-item {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--color-border);
  align-items: flex-start;
}
.retest-item:last-child {
  border-bottom: none;
}
.retest-emoji {
  font-size: 26px;
  line-height: 1;
  flex-shrink: 0;
}
.retest-body {
  flex: 1;
}
.retest-hint {
  font-weight: 700;
  color: var(--color-text);
  font-size: 15px;
}
.retest-desc {
  font-size: 13px;
  color: var(--color-text-sub);
  margin-top: 2px;
}
.retest-date {
  font-size: 12px;
  color: var(--color-primary);
  margin-top: 4px;
  font-weight: 600;
}
.retest-btn {
  background: var(--color-primary);
  color: #fff;
  border: none;
  padding: 6px 14px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  flex-shrink: 0;
  white-space: nowrap;
}
.retest-btn:hover {
  background: #ff9763;
}

.cta-row {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 4px;
}
.cta-btn {
  min-height: 50px;
  border-radius: var(--radius-lg);
  border: none;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.15s ease-out, box-shadow 0.2s ease-out;
}
.cta-btn.primary {
  background: var(--color-primary);
  color: #fff;
}
.cta-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 122, 69, 0.24);
}
.cta-btn.secondary {
  background: #fff;
  color: var(--color-text);
  border: 2px solid var(--color-border);
}
.cta-btn.secondary:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* 加权总评 */
.weighted-card {
  background: linear-gradient(135deg, #f0f5ff 0%, #e6f4ff 100%);
  border-left-color: #1677ff;
}
.weighted-intro {
  font-size: 14px;
  color: var(--color-text-sub);
  margin-bottom: 12px;
}
.weighted-results {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.w-group-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 6px;
}
.w-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #fff;
  border-radius: var(--radius-md);
  margin-bottom: 6px;
}
.w-kp {
  font-size: 14px;
  color: var(--color-text);
}
.w-rate {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-primary);
}

@media print {
  .r-header,
  .cta-row {
    display: none;
  }
  .result-app {
    background: #fff;
  }
}
</style>
