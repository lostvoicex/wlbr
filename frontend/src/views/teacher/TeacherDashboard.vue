<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import {
  fetchDashboardStats,
  type DashboardResp,
  type RecentActivity,
} from "@/api/dashboard";
import { extractErrorMessage } from "@/api/client";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();
const isAdmin = computed(() => auth.role === "admin");

const loading = ref(false);
const data = ref<DashboardResp | null>(null);

const sessionTypeMap: Record<string, string> = {
  diagnosis: "诊断",
  retest_t1: "复测 T1",
  retest_t2: "复测 T2",
};

const statusMap: Record<string, { text: string; color: string }> = {
  in_progress: { text: "进行中", color: "blue" },
  finished: { text: "已完成", color: "green" },
  abandoned: { text: "已放弃", color: "default" },
};

const masteryMap: Record<string, { text: string; color: string }> = {
  mastered: { text: "已掌握", color: "#52c41a" },
  need_review: { text: "需巩固", color: "#faad14" },
  need_repair: { text: "薄弱", color: "#ff4d4f" },
  low_confidence: { text: "数据不足", color: "#d9d9d9" },
};

const woStatusMap: Record<string, { text: string; color: string }> = {
  pending: { text: "待处理", color: "#faad14" },
  in_progress: { text: "进行中", color: "#1890ff" },
  completed: { text: "已完成", color: "#52c41a" },
  cancelled: { text: "已取消", color: "#d9d9d9" },
};

function formatDate(text: string): string {
  return text ? text.slice(0, 19).replace("T", " ") : "";
}

const recentColumns = [
  { title: "学员", key: "student_name", width: 100 },
  { title: "类型", key: "session_type", width: 90 },
  { title: "大纲", dataIndex: "syllabus_target", width: 120 },
  { title: "成绩", key: "score", width: 90 },
  { title: "状态", key: "status", width: 90 },
  { title: "时间", key: "started_at", width: 160 },
  { title: "操作", key: "action", width: 80 },
];

const cards = computed(() => {
  if (!data.value) return [];
  const d = data.value;
  return [
    {
      label: "学员总数",
      value: d.student_total,
      sub: `本周新增 ${d.student_new_this_week}`,
      icon: "team",
      color: "#1890ff",
      action: () => router.push("/teacher/students"),
    },
    {
      label: "诊断总数",
      value: d.session_total,
      sub: `已完成 ${d.session_finished} / 进行中 ${d.session_in_progress}`,
      icon: "file-search",
      color: "#52c41a",
    },
    {
      label: "待处理工单",
      value: d.work_order_pending,
      sub: `进行中 ${d.work_order_in_progress}`,
      icon: "container",
      color: "#faad14",
      action: () => router.push("/teacher/work-orders"),
    },
    {
      label: "异常标记",
      value: d.suspicious_count,
      sub: d.suspicious_count > 0 ? "需要关注" : "一切正常",
      icon: "warning",
      color: d.suspicious_count > 0 ? "#ff4d4f" : "#52c41a",
    },
  ];
});

const sessionTypeData = computed(() => {
  if (!data.value) return [];
  return data.value.session_type_stats.map((s) => ({
    name: sessionTypeMap[s.session_type] || s.session_type,
    value: s.count,
    color: s.session_type === "diagnosis" ? "#1890ff" : "#faad14",
  }));
});

const woBarData = computed(() => {
  if (!data.value) return [];
  return data.value.work_order_stats.map((s) => ({
    name: woStatusMap[s.status]?.text || s.status,
    value: s.count,
    color: woStatusMap[s.status]?.color || "#d9d9d9",
  }));
});

const masteryData = computed(() => {
  if (!data.value) return [];
  const total = data.value.mastery_stats.reduce((sum, s) => sum + s.count, 0);
  if (total === 0) return [];
  return data.value.mastery_stats.map((s) => ({
    name: masteryMap[s.mastery_level]?.text || s.mastery_level,
    value: s.count,
    percent: Math.round((s.count / total) * 100),
    color: masteryMap[s.mastery_level]?.color || "#d9d9d9",
  }));
});

const totalMastery = computed(() => {
  if (!data.value) return 0;
  return data.value.mastery_stats.reduce((sum, s) => sum + s.count, 0);
});

function viewStudent(record: RecentActivity) {
  router.push(`/teacher/students/${record.student_id}`);
}

async function fetchData() {
  loading.value = true;
  try {
    data.value = await fetchDashboardStats();
  } catch (e) {
    message.error(extractErrorMessage(e, "仪表盘数据加载失败"));
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="dashboard" :class="{ loading: loading }">
    <a-spin v-if="loading && !data" tip="加载中..." class="loading-spin" />

    <template v-if="data">
      <!-- 统计卡片 -->
      <div class="cards-row">
        <div
          v-for="card in cards"
          :key="card.label"
          class="stat-card teacher-card"
          :class="{ clickable: card.action }"
          @click="card.action?.()"
        >
          <div class="stat-icon" :style="{ background: card.color }">
            <span class="icon-letter">{{ card.label.charAt(0) }}</span>
          </div>
          <div class="stat-body">
            <div class="stat-value" :style="{ color: card.color }">
              {{ card.value }}
            </div>
            <div class="stat-label">{{ card.label }}</div>
            <div class="stat-sub">{{ card.sub }}</div>
          </div>
        </div>
      </div>

      <!-- 图表行 -->
      <div class="charts-row">
        <!-- 会话类型分布 -->
        <div class="chart-card teacher-card">
          <div class="chart-title">诊断类型分布</div>
          <div v-if="!sessionTypeData.length" class="chart-empty">暂无数据</div>
          <div v-else class="bar-chart">
            <div v-for="item in sessionTypeData" :key="item.name" class="bar-item">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{
                    width: (item.value / Math.max(...sessionTypeData.map((d) => d.value)) * 100) + '%',
                    background: item.color,
                  }"
                >
                  <span class="bar-value">{{ item.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 工单状态分布 -->
        <div class="chart-card teacher-card">
          <div class="chart-title">工单状态分布</div>
          <div v-if="!woBarData.length" class="chart-empty">暂无数据</div>
          <div v-else class="bar-chart">
            <div v-for="item in woBarData" :key="item.name" class="bar-item">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{
                    width: (item.value / Math.max(...woBarData.map((d) => d.value), 1) * 100) + '%',
                    background: item.color,
                  }"
                >
                  <span class="bar-value">{{ item.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- KP 掌握度分布 -->
      <div class="mastery-card teacher-card">
        <div class="chart-title">知识点掌握度分布</div>
        <div v-if="!masteryData.length" class="chart-empty">暂无数据</div>
        <div v-else class="mastery-bars">
          <div v-for="item in masteryData" :key="item.name" class="mastery-item">
            <div class="mastery-header">
              <span class="mastery-name">{{ item.name }}</span>
              <span class="mastery-count">{{ item.value }} ({{ item.percent }}%)</span>
            </div>
            <div class="mastery-track">
              <div
                class="mastery-fill"
                :style="{ width: item.percent + '%', background: item.color }"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动 -->
      <div class="activity-card teacher-card">
        <div class="chart-title">最近诊断活动</div>
        <a-empty v-if="!data.recent_activities.length" description="暂无活动" />
        <a-table
          v-else
          row-key="session_id"
          :columns="recentColumns"
          :data-source="data.recent_activities"
          :pagination="false"
          size="small"
          :scroll="{ x: 700 }"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'student_name'">
              <a-button type="link" size="small" @click="viewStudent(record)">
                {{ record.student_name }}
              </a-button>
            </template>
            <template v-else-if="column.key === 'session_type'">
              <a-tag :color="record.session_type === 'diagnosis' ? 'blue' : 'orange'">
                {{ sessionTypeMap[record.session_type] || record.session_type }}
              </a-tag>
            </template>
            <template v-else-if="column.key === 'score'">
              <span :class="['score', record.correct_count / record.total_count >= 0.8 ? 'pass' : 'weak']">
                {{ record.correct_count }}/{{ record.total_count }}
              </span>
              <a-tag v-if="record.suspicious_flag" color="red" size="small" style="margin-left: 4px">
                可疑
              </a-tag>
            </template>
            <template v-else-if="column.key === 'status'">
              <a-tag :color="statusMap[record.status]?.color || 'default'">
                {{ statusMap[record.status]?.text || record.status }}
              </a-tag>
            </template>
            <template v-else-if="column.key === 'started_at'">
              {{ formatDate(record.started_at) }}
            </template>
            <template v-else-if="column.key === 'action'">
              <a-button type="link" size="small" @click="viewStudent(record)">
                详情
              </a-button>
            </template>
          </template>
        </a-table>
      </div>
    </template>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.loading-spin {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

/* 统计卡片 */
.cards-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  transition: box-shadow 0.2s;
}

.stat-card.clickable {
  cursor: pointer;
}

.stat-card.clickable:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-letter {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
}

.stat-body {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  font-family: var(--font-num);
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: var(--color-text);
  font-weight: 500;
}

.stat-sub {
  font-size: 12px;
  color: var(--color-text-sub);
  margin-top: 2px;
}

/* 图表行 */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.chart-card {
  padding: 16px 20px 20px;
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 16px;
}

.chart-empty {
  color: var(--color-text-sub);
  font-size: 13px;
  text-align: center;
  padding: 24px 0;
}

/* 柱状图 */
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bar-label {
  width: 70px;
  font-size: 13px;
  color: var(--color-text-sub);
  text-align: right;
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  height: 24px;
  background: #f5f5f5;
  border-radius: 6px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  min-width: 28px;
  transition: width 0.3s;
}

.bar-value {
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  font-family: var(--font-num);
}

/* KP 掌握度 */
.mastery-card {
  padding: 16px 20px 20px;
}

.mastery-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mastery-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.mastery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mastery-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
}

.mastery-count {
  font-size: 13px;
  color: var(--color-text-sub);
  font-family: var(--font-num);
}

.mastery-track {
  height: 12px;
  background: #f5f5f5;
  border-radius: 6px;
  overflow: hidden;
}

.mastery-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.3s;
}

/* 活动表 */
.activity-card {
  padding: 16px 20px 20px;
}

.score {
  font-weight: 600;
  font-family: var(--font-num);
}

.score.pass {
  color: var(--color-pass);
}

.score.weak {
  color: var(--color-weak);
}

/* 响应式 */
@media (max-width: 1200px) {
  .cards-row {
    grid-template-columns: repeat(2, 1fr);
  }
  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .cards-row {
    grid-template-columns: 1fr;
  }
}
</style>
