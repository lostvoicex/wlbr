<script setup lang="ts">
import { onMounted, reactive, ref, computed } from "vue";
import { message } from "ant-design-vue";
import type { TablePaginationConfig } from "ant-design-vue";
import { listStudents, createStudent, type StudentOut, type StudentCreate } from "@/api/students";
import { extractErrorMessage } from "@/api/client";
import { useKpLabelsStore } from "@/stores/kpLabels";
import { useCopyTextsStore } from "@/stores/copyTexts";
import { fetchTeacherAlerts, type TeacherAlertItem } from "@/api/reminders";

const loading = ref(false);
const dataSource = ref<StudentOut[]>([]);
const total = ref(0);

const kpLabels = useKpLabelsStore();
const copyTexts = useCopyTextsStore();

const alerts = ref<TeacherAlertItem[]>([]);
const alertsLoading = ref(false);
const alertsCollapsed = ref(false);

const filters = reactive({
  keyword: "",
});

const pagination = reactive<TablePaginationConfig>({
  current: 1,
  pageSize: 10,
  showSizeChanger: true,
  showTotal: (t: number) => `共 ${t} 名学员`,
});

// 添加学员弹窗
const modalVisible = ref(false);
const modalLoading = ref(false);
const formRef = ref<any>(null);
const formState = reactive<StudentCreate>({
  name: "",
  grade: 3,
  phone: "",
  syllabus_target: "",
  password: "",
});

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

const columns = [
  { title: "ID", dataIndex: "id", width: 80 },
  { title: "姓名", dataIndex: "name" },
  { title: "手机号", dataIndex: "phone" },
  {
    title: "目标大纲",
    dataIndex: "syllabus_target",
    customRender: ({ text }: { text: string | null }) =>
      text !== null && text !== undefined && text !== "" ? text : "—",
  },
  {
    title: "注册时间",
    dataIndex: "created_at",
    customRender: ({ text }: { text: string }) => (text ? text.slice(0, 19).replace("T", " ") : ""),
  },
  { title: "操作", key: "action", width: 200 },
];

async function fetchData() {
  loading.value = true;
  try {
    const data = await listStudents({
      keyword: filters.keyword || undefined,
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

async function loadAlerts() {
  alertsLoading.value = true;
  try {
    const resp = await fetchTeacherAlerts(50);
    alerts.value = resp.items || [];
  } catch {
    alerts.value = [];
  } finally {
    alertsLoading.value = false;
  }
}

const alertLines = computed(() =>
  alerts.value.map((a) => {
    const kpName = kpLabels.getDisplay(a.kp_original);
    const line = copyTexts.renderTeacherAlert({
      student_name: a.student_name,
      kp_display_name: kpName,
      retest_type: a.retest_type,
      days_ago: a.days_ago,
      mastery_level: a.mastery_level,
    });
    return {
      ...a,
      kpName,
      line,
    };
  }),
);

const emptyHint = computed(
  () => copyTexts.getTeacherAlerts().empty_hint,
);

function onSearch() {
  pagination.current = 1;
  fetchData();
}

function onReset() {
  filters.keyword = "";
  pagination.current = 1;
  fetchData();
}

function onTableChange(p: TablePaginationConfig) {
  pagination.current = p.current || 1;
  pagination.pageSize = p.pageSize || 10;
  fetchData();
}

function openModal() {
  modalVisible.value = true;
  formState.name = "";
  formState.grade = 3;
  formState.phone = "";
  formState.syllabus_target = "";
  formState.password = "";
}

function closeModal() {
  modalVisible.value = false;
}

async function handleSubmit() {
  try {
    await formRef.value.validate();
  } catch {
    return;
  }
  modalLoading.value = true;
  try {
    const payload: StudentCreate = {
      name: formState.name.trim(),
      grade: formState.grade,
      phone: formState.phone?.trim() || undefined,
      syllabus_target: formState.syllabus_target || undefined,
      password: formState.password || undefined,
    };
    await createStudent(payload);
    message.success("学员添加成功");
    closeModal();
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "添加失败"));
  } finally {
    modalLoading.value = false;
  }
}

onMounted(async () => {
  kpLabels.loadOnce();
  copyTexts.loadOnce();
  await Promise.all([fetchData(), loadAlerts()]);
});
</script>

<template>
  <div class="teacher-students">
    <!-- 复测催办栏 -->
    <div class="alert-bar teacher-card" v-if="!alertsLoading">
      <div class="alert-head">
        <span class="alert-title">
          🔔 复测催办
          <span v-if="alertLines.length" class="alert-count">
            {{ alertLines.length }}
          </span>
        </span>
        <a-button
          v-if="alertLines.length"
          type="link"
          size="small"
          @click="alertsCollapsed = !alertsCollapsed"
        >
          {{ alertsCollapsed ? "展开" : "收起" }}
        </a-button>
      </div>
      <div v-if="!alertLines.length" class="alert-empty">
        {{ emptyHint }}
      </div>
      <div v-else-if="!alertsCollapsed" class="alert-list">
        <div
          v-for="a in alertLines"
          :key="a.student_id + '-' + a.kp_original"
          class="alert-item"
          :class="['type-' + a.retest_type]"
        >
          <span class="alert-badge" :class="['badge-' + a.retest_type]">
            {{ a.retest_type.toUpperCase() }}
          </span>
          <span class="alert-line">{{ a.line }}</span>
        </div>
      </div>
    </div>

    <div class="filter-bar teacher-card">
      <a-space wrap style="justify-content: space-between; width: 100%">
        <a-space wrap>
          <a-input
            v-model:value="filters.keyword"
            placeholder="搜索姓名 / 手机号"
            allow-clear
            style="width: 240px"
            @press-enter="onSearch"
          />
          <a-button type="primary" @click="onSearch">查询</a-button>
          <a-button @click="onReset">重置</a-button>
        </a-space>
        <a-button type="primary" @click="openModal">添加学员</a-button>
      </a-space>
    </div>

    <div class="table-wrap teacher-card">
      <a-table
        row-key="id"
        :columns="columns"
        :data-source="dataSource"
        :loading="loading"
        :pagination="pagination"
        @change="onTableChange"
        size="middle"
      >
        <template #bodyCell="{ column, record: _record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button size="small" type="link" :disabled="true">查看诊断</a-button>
              <a-button size="small" type="link" :disabled="true">推补课工单</a-button>
            </a-space>
            <div class="hint">（后续批次接入）</div>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 添加学员弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      title="添加学员"
      :confirm-loading="modalLoading"
      @ok="handleSubmit"
      @cancel="closeModal"
      ok-text="确认添加"
      cancel-text="取消"
      :width="480"
    >
      <a-form
        ref="formRef"
        :model="formState"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
        style="margin-top: 16px"
      >
        <a-form-item
          label="姓名"
          name="name"
          :rules="[{ required: true, message: '请输入学员姓名', trigger: 'blur' }]"
        >
          <a-input v-model:value="formState.name" placeholder="学员真实姓名" :maxlength="64" />
        </a-form-item>
        <a-form-item
          label="年级"
          name="grade"
          :rules="[{ required: true, message: '请选择年级', trigger: 'change' }]"
        >
          <a-select v-model:value="formState.grade" :options="gradeOptions" placeholder="请选择" />
        </a-form-item>
        <a-form-item label="手机号" name="phone">
          <a-input v-model:value="formState.phone" placeholder="选填，可用于登录" :maxlength="20" />
        </a-form-item>
        <a-form-item label="目标大纲" name="syllabus_target">
          <a-select
            v-model:value="formState.syllabus_target"
            :options="syllabusOptions"
            placeholder="选填，默认诊断时选择"
            allow-clear
          />
        </a-form-item>
        <a-form-item label="登录密码" name="password">
          <a-input-password
            v-model:value="formState.password"
            placeholder="选填，默认使用学号登录"
            :maxlength="64"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.teacher-students {
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
.hint {
  color: var(--color-text-sub);
  font-size: 12px;
  margin-top: 2px;
}

/* ---------- 催办栏 ---------- */
.alert-bar {
  padding: 12px 20px 14px;
  border-left: 4px solid #faad14;
  background: #fffbe6;
}
.alert-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.alert-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.alert-count {
  background: #ff4d4f;
  color: #fff;
  font-size: 12px;
  padding: 1px 8px;
  border-radius: 999px;
  font-weight: 700;
}
.alert-empty {
  margin-top: 6px;
  color: var(--color-text-sub);
  font-size: 13px;
}
.alert-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 240px;
  overflow-y: auto;
}
.alert-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  color: var(--color-text);
  background: #fff;
  border: 1px solid #ffe58f;
}
.alert-item.type-t2 {
  border-color: #ffbb96;
  background: #fff2e8;
}
.alert-badge {
  display: inline-block;
  padding: 1px 8px;
  font-size: 11px;
  font-weight: 700;
  border-radius: 999px;
  color: #fff;
  flex-shrink: 0;
}
.badge-t1 {
  background: #faad14;
}
.badge-t2 {
  background: #ff7a45;
}
.alert-line {
  line-height: 1.5;
}
</style>
