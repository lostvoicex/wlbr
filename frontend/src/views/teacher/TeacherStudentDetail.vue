<script setup lang="ts">
import { onMounted, reactive, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { message } from "ant-design-vue";
import {
  getStudent,
  getStudentSessions,
  updateStudent,
  type StudentOut,
  type StudentUpdate,
  type SessionHistoryItem,
  type KpSnapshot,
} from "@/api/students";
import {
  createWorkOrder,
  type WorkOrderCreate,
} from "@/api/workOrders";
import { listTeachers, type TeacherOut } from "@/api/teachers";
import { extractErrorMessage } from "@/api/client";
import { useKpLabelsStore } from "@/stores/kpLabels";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const kpLabels = useKpLabelsStore();

const studentId = Number(route.params.id);
const isAdmin = computed(() => auth.role === "admin");

const loading = ref(false);
const student = ref<StudentOut | null>(null);
const sessions = ref<SessionHistoryItem[]>([]);

// ---- 翻译映射 ----
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
  mastered: { text: "已掌握", color: "green" },
  need_review: { text: "需巩固", color: "orange" },
  need_repair: { text: "薄弱", color: "red" },
  low_confidence: { text: "数据不足", color: "default" },
};

const gradeOptions = [
  { label: "二年级", value: 2 },
  { label: "三年级", value: 3 },
  { label: "四年级", value: 4 },
  { label: "五年级", value: 5 },
  { label: "六年级", value: 6 },
];

const syllabusOptions = [
  { label: "Scratch 一级", value: "scratch_l1" },
  { label: "Scratch 二级", value: "scratch_l2" },
  { label: "Scratch 三级", value: "scratch_l3" },
  { label: "Scratch 四级", value: "scratch_l4" },
  { label: "C++ 一级", value: "cpp_l1" },
  { label: "C++ 二级", value: "cpp_l2" },
  { label: "C++ 三级", value: "cpp_l3" },
  { label: "C++ 四级", value: "cpp_l4" },
  { label: "C++ 五级", value: "cpp_l5" },
  { label: "C++ 六级", value: "cpp_l6" },
  { label: "C++ 七级", value: "cpp_l7" },
  { label: "C++ 八级", value: "cpp_l8" },
  { label: "Python 一级", value: "python_l1" },
  { label: "Python 二级", value: "python_l2" },
  { label: "Python 三级", value: "python_l3" },
  { label: "Python 四级", value: "python_l4" },
  { label: "Python 五级", value: "python_l5" },
  { label: "Python 六级", value: "python_l6" },
];

const sessionColumns = [
  { title: "类型", key: "session_type", width: 100 },
  { title: "大纲", dataIndex: "syllabus_target", width: 130 },
  { title: "正确/总数", key: "score", width: 100 },
  { title: "状态", key: "status", width: 100 },
  { title: "开始时间", key: "started_at", width: 170 },
  { title: "异常标记", key: "suspicious", width: 100 },
  { title: "操作", key: "action", width: 120 },
];

function formatDate(text: string | null): string {
  if (!text) return "—";
  return text.slice(0, 19).replace("T", " ");
}

function formatRate(rate: number): string {
  return `${Math.round(rate * 100)}%`;
}

function getKpName(kp: string): string {
  return kpLabels.getDisplay(kp);
}

// ---- 数据加载 ----
async function fetchStudent() {
  loading.value = true;
  try {
    student.value = await getStudent(studentId);
  } catch (e) {
    message.error(extractErrorMessage(e, "学员信息加载失败"));
  } finally {
    loading.value = false;
  }
}

async function fetchSessions() {
  try {
    const resp = await getStudentSessions(studentId);
    sessions.value = resp.items;
  } catch (e) {
    message.error(extractErrorMessage(e, "诊断历史加载失败"));
  }
}

// ---- 编辑弹窗 ----
const editVisible = ref(false);
const editLoading = ref(false);
const editForm = reactive<StudentUpdate>({
  name: "",
  grade: 3,
  phone: "",
  syllabus_target: "",
  learning_note: "",
  password: "",
});

function openEdit() {
  if (!student.value) return;
  editForm.name = student.value.name;
  editForm.grade = student.value.grade;
  editForm.phone = student.value.phone || "";
  editForm.syllabus_target = student.value.syllabus_target || "";
  editForm.learning_note = student.value.learning_note || "";
  editForm.password = "";
  editVisible.value = true;
}

async function handleEditSubmit() {
  editLoading.value = true;
  try {
    const payload: StudentUpdate = {
      name: editForm.name?.trim(),
      grade: editForm.grade,
      phone: editForm.phone?.trim() || null,
      syllabus_target: editForm.syllabus_target || null,
      learning_note: editForm.learning_note || null,
    };
    if (editForm.password) {
      payload.password = editForm.password;
    }
    student.value = await updateStudent(studentId, payload);
    message.success("修改成功");
    editVisible.value = false;
  } catch (e) {
    message.error(extractErrorMessage(e, "修改失败"));
  } finally {
    editLoading.value = false;
  }
}

// ---- 工单创建弹窗 ----
const woVisible = ref(false);
const woLoading = ref(false);
const teachers = ref<TeacherOut[]>([]);
const teachersLoading = ref(false);

const woForm = reactive<{
  syllabus_target: string;
  weak_kps: string;
  title: string;
  description: string;
  priority: string;
  due_date: string;
  assignee_id: number | undefined;
}>({
  syllabus_target: "",
  weak_kps: "",
  title: "",
  description: "",
  priority: "medium",
  due_date: "",
  assignee_id: undefined,
});

async function loadTeachers() {
  if (!isAdmin.value) return;
  teachersLoading.value = true;
  try {
    const data = await listTeachers({ page_size: 200, status: "active" });
    teachers.value = data.items.filter((t) => t.role === "teacher");
  } catch {
    teachers.value = [];
  } finally {
    teachersLoading.value = false;
  }
}

function openWorkOrder(session?: SessionHistoryItem) {
  if (!student.value) return;
  woForm.syllabus_target = session?.syllabus_target || student.value.syllabus_target || "";
  woForm.weak_kps = "";
  woForm.title = `【补课】${student.value.name} 的${sessionTypeMap[session?.session_type || "diagnosis"] || "诊断"}后补课`;
  woForm.description = "";
  woForm.priority = "medium";
  woForm.due_date = "";
  woForm.assignee_id = undefined;

  if (session && session.kp_snapshots.length > 0) {
    const weakKps = session.kp_snapshots
      .filter((kp) => kp.mastery_level !== "mastered")
      .map((kp) => kp.knowledge_point);
    if (weakKps.length > 0) {
      woForm.weak_kps = weakKps.join(",");
    }
  }

  woVisible.value = true;
  if (isAdmin.value && !teachers.value.length) {
    loadTeachers();
  }
}

async function handleWorkOrderSubmit() {
  if (!woForm.title.trim()) {
    message.warning("请输入工单标题");
    return;
  }
  if (!woForm.syllabus_target.trim()) {
    message.warning("请输入目标大纲");
    return;
  }
  if (!woForm.weak_kps.trim()) {
    message.warning("请输入薄弱知识点");
    return;
  }
  woLoading.value = true;
  try {
    const payload: WorkOrderCreate = {
      student_id: studentId,
      syllabus_target: woForm.syllabus_target,
      weak_kps: woForm.weak_kps,
      title: woForm.title,
      description: woForm.description || undefined,
      priority: woForm.priority,
      due_date: woForm.due_date || undefined,
      assignee_id: woForm.assignee_id,
    };
    await createWorkOrder(payload);
    message.success("工单创建成功");
    woVisible.value = false;
  } catch (e) {
    message.error(extractErrorMessage(e, "创建工单失败"));
  } finally {
    woLoading.value = false;
  }
}

function goBack() {
  router.push("/teacher/students");
}

onMounted(async () => {
  kpLabels.loadOnce();
  await Promise.all([fetchStudent(), fetchSessions()]);
  if (route.query.action === "workorder" && student.value) {
    openWorkOrder();
  }
});
</script>

<template>
  <div class="student-detail" v-if="student">
    <!-- 学员信息卡片 -->
    <div class="info-card teacher-card">
      <div class="info-header">
        <div class="info-title">
          <a-button type="text" size="small" @click="goBack" class="back-btn">
            &larr; 返回列表
          </a-button>
          <span class="student-name">{{ student.name }}</span>
          <a-tag color="blue">ID: {{ student.id }}</a-tag>
        </div>
        <a-space>
          <a-button type="primary" @click="openEdit">编辑信息</a-button>
          <a-button @click="openWorkOrder()">推补课工单</a-button>
        </a-space>
      </div>

      <a-descriptions :column="3" size="middle" class="info-desc">
        <a-descriptions-item label="年级">
          {{ gradeOptions.find((g) => g.value === student.grade)?.label || student.grade }}
        </a-descriptions-item>
        <a-descriptions-item label="手机号">
          {{ student.phone || "—" }}
        </a-descriptions-item>
        <a-descriptions-item label="目标大纲">
          {{ syllabusOptions.find((s) => s.value === student.syllabus_target)?.label || student.syllabus_target || "—" }}
        </a-descriptions-item>
        <a-descriptions-item label="学习备注" :span="3">
          {{ student.learning_note || "—" }}
        </a-descriptions-item>
        <a-descriptions-item label="注册时间">
          {{ formatDate(student.created_at) }}
        </a-descriptions-item>
        <a-descriptions-item label="更新时间">
          {{ formatDate(student.updated_at) }}
        </a-descriptions-item>
      </a-descriptions>
    </div>

    <!-- 诊断历史 -->
    <div class="history-card teacher-card">
      <div class="section-title">诊断历史</div>
      <a-empty
        v-if="!sessions.length"
        description="暂无诊断记录"
        :image-style="{ height: '60px' }"
      />
      <a-table
        v-else
        row-key="id"
        :columns="sessionColumns"
        :data-source="sessions"
        :pagination="false"
        :loading="loading"
        size="middle"
        :expandable="{ expandedRowRender: undefined }"
      >
        <template #expandedRowRender="{ record }">
          <div class="kp-snapshots" v-if="record.kp_snapshots && record.kp_snapshots.length">
            <div class="kp-header">知识点掌握度快照</div>
            <div class="kp-list">
              <div
                v-for="kp in record.kp_snapshots"
                :key="kp.knowledge_point"
                class="kp-item"
              >
                <span class="kp-name">{{ getKpName(kp.knowledge_point) }}</span>
                <span class="kp-score">{{ kp.correct_count }}/{{ kp.total_count }}</span>
                <span class="kp-rate">{{ formatRate(Number(kp.correct_rate)) }}</span>
                <a-tag
                  :color="masteryMap[kp.mastery_level]?.color || 'default'"
                  size="small"
                >
                  {{ masteryMap[kp.mastery_level]?.text || kp.mastery_level }}
                </a-tag>
              </div>
            </div>
          </div>
          <a-empty v-else description="无知识点快照" :image-style="{ height: '40px' }" />
        </template>
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'session_type'">
            <a-tag :color="record.session_type === 'diagnosis' ? 'blue' : 'orange'">
              {{ sessionTypeMap[record.session_type] || record.session_type }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'score'">
            <span :class="['score-text', record.correct_count / record.total_count >= 0.8 ? 'pass' : 'weak']">
              {{ record.correct_count }}/{{ record.total_count }}
            </span>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="statusMap[record.status]?.color || 'default'">
              {{ statusMap[record.status]?.text || record.status }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'started_at'">
            {{ formatDate(record.started_at) }}
          </template>
          <template v-else-if="column.key === 'suspicious'">
            <a-tag v-if="record.suspicious_flag" color="red">可疑</a-tag>
            <span v-else class="normal-text">正常</span>
          </template>
          <template v-else-if="column.key === 'action'">
            <a-button
              size="small"
              type="link"
              :disabled="record.status !== 'finished'"
              @click="openWorkOrder(record)"
            >
              推工单
            </a-button>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 编辑弹窗 -->
    <a-modal
      v-model:open="editVisible"
      title="编辑学员信息"
      :confirm-loading="editLoading"
      @ok="handleEditSubmit"
      ok-text="保存"
      cancel-text="取消"
      :width="520"
    >
      <a-form :model="editForm" layout="vertical" style="margin-top: 16px">
        <a-form-item label="姓名" required>
          <a-input v-model:value="editForm.name" placeholder="学员姓名" :maxlength="64" />
        </a-form-item>
        <a-form-item label="年级" required>
          <a-select v-model:value="editForm.grade" :options="gradeOptions" />
        </a-form-item>
        <a-form-item label="手机号">
          <a-input v-model:value="editForm.phone" placeholder="选填" :maxlength="20" />
        </a-form-item>
        <a-form-item label="目标大纲">
          <a-select
            v-model:value="editForm.syllabus_target"
            :options="syllabusOptions"
            placeholder="选填"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="学习备注">
          <a-input v-model:value="editForm.learning_note" placeholder="选填" :maxlength="50" />
        </a-form-item>
        <a-form-item label="重置密码">
          <a-input-password
            v-model:value="editForm.password"
            placeholder="留空则不修改密码"
            :maxlength="64"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 创建工单弹窗 -->
    <a-modal
      v-model:open="woVisible"
      title="创建补课工单"
      :confirm-loading="woLoading"
      @ok="handleWorkOrderSubmit"
      ok-text="创建"
      cancel-text="取消"
      :width="560"
    >
      <a-form :model="woForm" layout="vertical" style="margin-top: 16px">
        <a-form-item label="工单标题" required>
          <a-input v-model:value="woForm.title" placeholder="工单标题" />
        </a-form-item>
        <a-form-item label="目标大纲" required>
          <a-select
            v-model:value="woForm.syllabus_target"
            :options="syllabusOptions"
            placeholder="选择目标大纲"
          />
        </a-form-item>
        <a-form-item label="薄弱知识点" required>
          <a-textarea
            v-model:value="woForm.weak_kps"
            placeholder="多个知识点用英文逗号分隔"
            :rows="2"
          />
        </a-form-item>
        <a-form-item v-if="isAdmin" label="分配给">
          <a-select
            v-model:value="woForm.assignee_id"
            placeholder="选择处理老师（留空则待分配）"
            :loading="teachersLoading"
            show-search
            option-filter-prop="label"
            allow-clear
          >
            <a-select-option
              v-for="t in teachers"
              :key="t.id"
              :value="t.id"
              :label="t.name"
            >
              {{ t.name }}（{{ t.teacher_no }}）
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="描述">
          <a-textarea v-model:value="woForm.description" placeholder="选填" :rows="3" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="优先级">
              <a-select v-model:value="woForm.priority">
                <a-select-option value="low">低</a-select-option>
                <a-select-option value="medium">中</a-select-option>
                <a-select-option value="high">高</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="截止日期">
              <a-date-picker
                v-model:value="woForm.due_date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>
  </div>

  <div v-else class="loading-wrap">
    <a-spin tip="加载中..." />
  </div>
</template>

<style scoped>
.student-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-card {
  padding: 16px 20px;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.info-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn {
  padding: 0 4px;
  color: var(--color-text-sub);
}

.back-btn:hover {
  color: var(--color-primary);
}

.student-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
}

.info-desc {
  margin-top: 8px;
}

.history-card {
  padding: 16px 20px 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 12px;
}

.score-text {
  font-weight: 600;
  font-family: var(--font-num);
}

.score-text.pass {
  color: var(--color-pass);
}

.score-text.weak {
  color: var(--color-weak);
}

.normal-text {
  color: var(--color-text-sub);
  font-size: 13px;
}

/* KP 快照展开区 */
.kp-snapshots {
  padding: 8px 0;
}

.kp-header {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-sub);
  margin-bottom: 8px;
}

.kp-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.kp-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 6px;
  background: #fafafa;
  font-size: 13px;
}

.kp-name {
  flex: 1;
  color: var(--color-text);
}

.kp-score {
  font-family: var(--font-num);
  color: var(--color-text-sub);
  min-width: 60px;
}

.kp-rate {
  font-family: var(--font-num);
  font-weight: 600;
  min-width: 50px;
}

.loading-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
