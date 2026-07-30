<script setup lang="ts">
import { onMounted, reactive, ref, computed } from "vue";
import { message, Modal } from "ant-design-vue";
import type { TablePaginationConfig } from "ant-design-vue";
import {
  listWorkOrders,
  createWorkOrder,
  updateWorkOrder,
  cancelWorkOrder,
  completeWorkOrder,
  type WorkOrderOut,
  type WorkOrderCreate,
  type WorkOrderUpdate,
} from "@/api/workOrders";
import { listStudents, type StudentOut } from "@/api/students";
import { listTeachers, type TeacherOut } from "@/api/teachers";
import { extractErrorMessage } from "@/api/client";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const isAdmin = computed(() => auth.role === "admin");

const loading = ref(false);
const dataSource = ref<WorkOrderOut[]>([]);
const total = ref(0);

const students = ref<StudentOut[]>([]);
const studentsLoading = ref(false);

const teachers = ref<TeacherOut[]>([]);
const teachersLoading = ref(false);

const filters = reactive({
  keyword: "",
  status: undefined as string | undefined,
  priority: undefined as string | undefined,
  syllabus_target: undefined as string | undefined,
});

const pagination = reactive<TablePaginationConfig>({
  current: 1,
  pageSize: 10,
  showSizeChanger: true,
  showTotal: (t: number) => `共 ${t} 条工单`,
});

const statusMap: Record<string, { text: string; color: string }> = {
  pending: { text: "待处理", color: "orange" },
  in_progress: { text: "进行中", color: "blue" },
  completed: { text: "已完成", color: "green" },
  cancelled: { text: "已取消", color: "default" },
};

const priorityMap: Record<string, { text: string; color: string }> = {
  low: { text: "低", color: "green" },
  medium: { text: "中", color: "orange" },
  high: { text: "高", color: "red" },
};

const columns = computed(() => {
  const cols: any[] = [
    { title: "ID", dataIndex: "id", width: 80 },
    { title: "学员姓名", dataIndex: "student_name", width: 120 },
    { title: "标题", dataIndex: "title", ellipsis: true },
    { title: "薄弱知识点", dataIndex: "weak_kps", key: "weak_kps", ellipsis: true },
    { title: "状态", dataIndex: "status", key: "status", width: 100 },
    { title: "优先级", dataIndex: "priority", key: "priority", width: 90 },
  ];
  // admin 显示分配对象
  if (isAdmin.value) {
    cols.push({ title: "处理老师", dataIndex: "assignee_name", key: "assignee_name", width: 120 });
  }
  cols.push(
    { title: "创建时间", dataIndex: "created_at", key: "created_at", width: 170 },
    { title: "操作", key: "action", width: 240, fixed: "right" as const }
  );
  return cols;
});

function formatWeakKps(text: string): string {
  if (!text) return "—";
  const parts = text.split(",").filter(Boolean);
  return parts.length > 2 ? parts.slice(0, 2).join("、") + "..." : text;
}

function formatDate(text: string): string {
  return text ? text.slice(0, 19).replace("T", " ") : "";
}

async function fetchData() {
  loading.value = true;
  try {
    const data = await listWorkOrders({
      keyword: filters.keyword || undefined,
      status: filters.status,
      priority: filters.priority,
      syllabus_target: filters.syllabus_target,
      page: pagination.current,
      page_size: pagination.pageSize,
    });
    dataSource.value = data.items;
    total.value = data.total;
    pagination.total = data.total;
  } catch (e) {
    message.error(extractErrorMessage(e, "加载失败"));
  } finally {
    loading.value = false;
  }
}

async function loadStudents() {
  studentsLoading.value = true;
  try {
    const data = await listStudents({ page_size: 200 });
    students.value = data.items;
  } catch {
    students.value = [];
  } finally {
    studentsLoading.value = false;
  }
}

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

function onSearch() {
  pagination.current = 1;
  fetchData();
}

function onReset() {
  filters.keyword = "";
  filters.status = undefined;
  filters.priority = undefined;
  filters.syllabus_target = undefined;
  pagination.current = 1;
  fetchData();
}

function onTableChange(p: TablePaginationConfig) {
  pagination.current = p.current || 1;
  pagination.pageSize = p.pageSize || 10;
  fetchData();
}

// ---------- 新建/编辑弹窗 ----------
const modalVisible = ref(false);
const modalMode = ref<"create" | "edit">("create");
const editingId = ref<number | null>(null);
const formLoading = ref(false);

const formData = reactive<WorkOrderCreate & { student_name?: string }>({
  student_id: 0,
  syllabus_target: "",
  weak_kps: "",
  title: "",
  description: "",
  priority: "medium",
  due_date: "",
  assignee_id: undefined,
});

function openCreate() {
  modalMode.value = "create";
  editingId.value = null;
  Object.assign(formData, {
    student_id: 0,
    syllabus_target: "",
    weak_kps: "",
    title: "",
    description: "",
    priority: "medium",
    due_date: "",
    assignee_id: undefined,
  });
  modalVisible.value = true;
}

function openEdit(record: WorkOrderOut) {
  modalMode.value = "edit";
  editingId.value = record.id;
  Object.assign(formData, {
    student_id: record.student_id,
    syllabus_target: record.syllabus_target,
    weak_kps: record.weak_kps,
    title: record.title,
    description: record.description || "",
    priority: record.priority,
    due_date: record.due_date ? record.due_date.slice(0, 10) : "",
    assignee_id: record.assignee_id || undefined,
  });
  modalVisible.value = true;
}

async function handleSubmit() {
  if (!formData.student_id) {
    message.warning("请选择学员");
    return;
  }
  if (!formData.title.trim()) {
    message.warning("请输入工单标题");
    return;
  }
  if (!formData.syllabus_target.trim()) {
    message.warning("请输入目标大纲");
    return;
  }
  if (!formData.weak_kps.trim()) {
    message.warning("请输入薄弱知识点");
    return;
  }
  formLoading.value = true;
  try {
    if (modalMode.value === "create") {
      await createWorkOrder({
        student_id: formData.student_id,
        syllabus_target: formData.syllabus_target,
        weak_kps: formData.weak_kps,
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        due_date: formData.due_date || undefined,
        assignee_id: formData.assignee_id,
      });
      message.success("创建成功");
    } else if (editingId.value !== null) {
      const updateData: WorkOrderUpdate = {
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        due_date: formData.due_date || undefined,
        weak_kps: formData.weak_kps,
      };
      // admin 可以重新分配
      if (isAdmin.value && formData.assignee_id) {
        updateData.assignee_id = formData.assignee_id;
      }
      await updateWorkOrder(editingId.value, updateData);
      message.success("更新成功");
    }
    modalVisible.value = false;
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "操作失败"));
  } finally {
    formLoading.value = false;
  }
}

// ---------- 分配弹窗（仅 admin） ----------
const assignModalVisible = ref(false);
const assignLoading = ref(false);
const assigningRecord = ref<WorkOrderOut | null>(null);
const assignTargetId = ref<number | undefined>(undefined);

function openAssign(record: WorkOrderOut) {
  assigningRecord.value = record;
  assignTargetId.value = record.assignee_id || undefined;
  assignModalVisible.value = true;
}

async function handleAssign() {
  if (!assigningRecord.value) return;
  assignLoading.value = true;
  try {
    await updateWorkOrder(assigningRecord.value.id, {
      assignee_id: assignTargetId.value,
    });
    message.success("分配成功");
    assignModalVisible.value = false;
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "分配失败"));
  } finally {
    assignLoading.value = false;
  }
}

// ---------- 操作 ----------
function handleCancelOrder(record: WorkOrderOut) {
  Modal.confirm({
    title: "确认取消工单？",
    content: `工单「${record.title}」将被取消，取消后不可恢复。`,
    okText: "确认取消",
    okType: "danger",
    cancelText: "返回",
    onOk: async () => {
      try {
        await cancelWorkOrder(record.id);
        message.success("已取消");
        fetchData();
      } catch (e) {
        message.error(extractErrorMessage(e, "操作失败"));
      }
    },
  });
}

function handleComplete(record: WorkOrderOut) {
  Modal.confirm({
    title: "确认标记完成？",
    content: `工单「${record.title}」将标记为已完成。`,
    okText: "确认完成",
    cancelText: "返回",
    onOk: async () => {
      try {
        await completeWorkOrder(record.id);
        message.success("已完成");
        fetchData();
      } catch (e) {
        message.error(extractErrorMessage(e, "操作失败"));
      }
    },
  });
}

// ---------- 详情弹窗 ----------
const detailVisible = ref(false);
const detailRecord = ref<WorkOrderOut | null>(null);

function handleView(record: WorkOrderOut) {
  detailRecord.value = record;
  detailVisible.value = true;
}

onMounted(async () => {
  await Promise.all([fetchData(), loadStudents(), loadTeachers()]);
});
</script>

<template>
  <div class="teacher-work-orders">
    <div class="filter-bar teacher-card">
      <a-space wrap>
        <a-input
          v-model:value="filters.keyword"
          placeholder="搜索标题 / 知识点"
          allow-clear
          style="width: 240px"
          @press-enter="onSearch"
        />
        <a-select
          v-model:value="filters.status"
          placeholder="全部状态"
          allow-clear
          style="width: 140px"
          :options="[
            { value: 'pending', label: '待处理' },
            { value: 'in_progress', label: '进行中' },
            { value: 'completed', label: '已完成' },
            { value: 'cancelled', label: '已取消' },
          ]"
        />
        <a-select
          v-model:value="filters.priority"
          placeholder="全部优先级"
          allow-clear
          style="width: 140px"
          :options="[
            { value: 'low', label: '低' },
            { value: 'medium', label: '中' },
            { value: 'high', label: '高' },
          ]"
        />
        <a-input
          v-model:value="filters.syllabus_target"
          placeholder="课件等级 / 大纲"
          allow-clear
          style="width: 180px"
          @press-enter="onSearch"
        />
        <a-button type="primary" @click="onSearch">查询</a-button>
        <a-button @click="onReset">重置</a-button>
      </a-space>
    </div>

    <div class="table-wrap teacher-card">
      <div class="table-header">
        <div class="table-title">
          补课工单
          <span v-if="!isAdmin" class="sub-title">（仅显示分配给我的）</span>
        </div>
        <a-button v-if="isAdmin" type="primary" @click="openCreate">新建工单</a-button>
      </div>
      <a-table
        row-key="id"
        :columns="columns"
        :data-source="dataSource"
        :loading="loading"
        :pagination="pagination"
        @change="onTableChange"
        size="middle"
        :scroll="{ x: 1100 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'weak_kps'">
            {{ formatWeakKps(record.weak_kps) }}
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="statusMap[record.status]?.color || 'default'">
              {{ statusMap[record.status]?.text || record.status }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'priority'">
            <a-tag :color="priorityMap[record.priority]?.color || 'default'">
              {{ priorityMap[record.priority]?.text || record.priority }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'assignee_name'">
            <span v-if="record.assignee_name">{{ record.assignee_name }}</span>
            <span v-else class="unassigned">待分配</span>
          </template>
          <template v-else-if="column.key === 'created_at'">
            {{ formatDate(record.created_at) }}
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <a-button size="small" type="link" @click="handleView(record)">
                查看
              </a-button>
              <!-- admin 可以分配 -->
              <a-button
                v-if="isAdmin"
                size="small"
                type="link"
                @click="openAssign(record)"
              >
                分配
              </a-button>
              <!-- 编辑：admin 都能编辑；teacher 只能编辑自己的未完成工单 -->
              <a-button
                size="small"
                type="link"
                @click="openEdit(record)"
                :disabled="record.status === 'completed' || record.status === 'cancelled'"
              >
                编辑
              </a-button>
              <a-button
                size="small"
                type="link"
                danger
                @click="handleCancelOrder(record)"
                :disabled="record.status === 'completed' || record.status === 'cancelled'"
              >
                取消
              </a-button>
              <a-button
                size="small"
                type="link"
                @click="handleComplete(record)"
                :disabled="record.status === 'completed' || record.status === 'cancelled'"
              >
                完成
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 新建/编辑弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalMode === 'create' ? '新建工单' : '编辑工单'"
      :confirm-loading="formLoading"
      @ok="handleSubmit"
      ok-text="确认"
      cancel-text="取消"
      :mask-closable="false"
      width="560px"
    >
      <a-form layout="vertical" :model="formData">
        <a-form-item label="学员" required>
          <a-select
            v-model:value="formData.student_id"
            placeholder="请选择学员"
            :loading="studentsLoading"
            show-search
            option-filter-prop="label"
            :disabled="modalMode === 'edit'"
          >
            <a-select-option
              v-for="s in students"
              :key="s.id"
              :value="s.id"
              :label="s.name"
            >
              {{ s.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="工单标题" required>
          <a-input v-model:value="formData.title" placeholder="请输入工单标题" />
        </a-form-item>
        <a-form-item label="目标大纲" required>
          <a-input v-model:value="formData.syllabus_target" placeholder="例如：scratch-l1" />
        </a-form-item>
        <a-form-item label="薄弱知识点" required>
          <a-textarea
            v-model:value="formData.weak_kps"
            placeholder="多个知识点用英文逗号分隔"
            :rows="2"
          />
        </a-form-item>
        <!-- 仅 admin 可以分配 -->
        <a-form-item v-if="isAdmin" label="分配给">
          <a-select
            v-model:value="formData.assignee_id"
            placeholder="请选择处理老师（留空则待分配）"
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
          <a-textarea
            v-model:value="formData.description"
            placeholder="请输入工单描述"
            :rows="3"
          />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="优先级">
              <a-select v-model:value="formData.priority">
                <a-select-option value="low">低</a-select-option>
                <a-select-option value="medium">中</a-select-option>
                <a-select-option value="high">高</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="截止日期">
              <a-date-picker
                v-model:value="formData.due_date"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>

    <!-- 分配弹窗（仅 admin） -->
    <a-modal
      v-model:open="assignModalVisible"
      title="分配工单"
      :confirm-loading="assignLoading"
      @ok="handleAssign"
      ok-text="确认分配"
      cancel-text="取消"
      width="400px"
    >
      <a-form layout="vertical">
        <a-form-item label="选择处理老师">
          <a-select
            v-model:value="assignTargetId"
            placeholder="请选择老师（留空取消分配）"
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
      </a-form>
    </a-modal>

    <!-- 详情弹窗 -->
    <a-modal
      v-model:open="detailVisible"
      title="工单详情"
      :footer="null"
      width="600px"
    >
      <div v-if="detailRecord" class="detail-content">
        <a-descriptions :column="2" bordered size="small">
          <a-descriptions-item label="ID">{{ detailRecord.id }}</a-descriptions-item>
          <a-descriptions-item label="学员">{{ detailRecord.student_name || "-" }}</a-descriptions-item>
          <a-descriptions-item label="标题" :span="2">{{ detailRecord.title }}</a-descriptions-item>
          <a-descriptions-item label="目标大纲" :span="2">{{ detailRecord.syllabus_target }}</a-descriptions-item>
          <a-descriptions-item label="薄弱知识点" :span="2">{{ detailRecord.weak_kps || "-" }}</a-descriptions-item>
          <a-descriptions-item label="描述" :span="2">{{ detailRecord.description || "-" }}</a-descriptions-item>
          <a-descriptions-item label="处理老师" :span="2">
            <span v-if="detailRecord.assignee_name">{{ detailRecord.assignee_name }}</span>
            <span v-else class="unassigned">待分配</span>
          </a-descriptions-item>
          <a-descriptions-item label="优先级">
            <a-tag :color="priorityMap[detailRecord.priority]?.color || 'default'">
              {{ priorityMap[detailRecord.priority]?.text || detailRecord.priority }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="状态">
            <a-tag :color="statusMap[detailRecord.status]?.color || 'default'">
              {{ statusMap[detailRecord.status]?.text || detailRecord.status }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="创建时间" :span="2">
            {{ formatDate(detailRecord.created_at) }}
          </a-descriptions-item>
        </a-descriptions>
      </div>
    </a-modal>
  </div>
</template>

<style scoped>
.teacher-work-orders {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.filter-bar {
  padding: 16px 20px;
}
.table-wrap {
  padding: 12px 20px 20px;
}
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.table-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
}
.sub-title {
  font-size: 13px;
  color: var(--color-text-sub);
  font-weight: 400;
  margin-left: 8px;
}
.detail-content {
  line-height: 1.6;
}
.unassigned {
  color: #faad14;
  font-style: italic;
}
</style>
