<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { message } from "ant-design-vue";
import type { TablePaginationConfig } from "ant-design-vue";
import {
  listTeachers,
  createTeacher,
  updateTeacher,
  deleteTeacher,
  type TeacherOut,
  type TeacherCreate,
  type TeacherUpdate,
} from "@/api/teachers";
import { extractErrorMessage } from "@/api/client";

const loading = ref(false);
const dataSource = ref<TeacherOut[]>([]);
const total = ref(0);

const filters = reactive({
  keyword: "",
  role: undefined as string | undefined,
});

const pagination = reactive<TablePaginationConfig>({
  current: 1,
  pageSize: 10,
  showSizeChanger: true,
  showTotal: (t: number) => `共 ${t} 名教师`,
});

const columns = [
  { title: "ID", dataIndex: "id", width: 80 },
  { title: "工号", dataIndex: "teacher_no", width: 120 },
  { title: "姓名", dataIndex: "name", width: 120 },
  {
    title: "角色",
    dataIndex: "role",
    width: 100,
    customRender: ({ text }: { text: string }) =>
      text === "admin" ? "管理员" : "教师",
  },
  { title: "手机号", dataIndex: "phone", width: 140 },
  { title: "邮箱", dataIndex: "email", width: 180 },
  {
    title: "状态",
    dataIndex: "status",
    width: 100,
    customRender: ({ text }: { text: string }) =>
      text === "active"
        ? "正常"
        : "已禁用",
  },
  {
    title: "注册时间",
    dataIndex: "created_at",
    width: 170,
    customRender: ({ text }: { text: string }) =>
      text ? text.slice(0, 19).replace("T", " ") : "",
  },
  { title: "操作", key: "action", width: 200, fixed: "right" },
];

async function fetchData() {
  loading.value = true;
  try {
    const data = await listTeachers({
      keyword: filters.keyword || undefined,
      role: filters.role,
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

function onSearch() {
  pagination.current = 1;
  fetchData();
}

function onReset() {
  filters.keyword = "";
  filters.role = undefined;
  pagination.current = 1;
  fetchData();
}

function onTableChange(p: TablePaginationConfig) {
  pagination.current = p.current || 1;
  pagination.pageSize = p.pageSize || 10;
  fetchData();
}

// 添加/编辑弹窗
const modalVisible = ref(false);
const modalLoading = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);
const formRef = ref<any>(null);
const formState = reactive<TeacherCreate & { status?: string }>({
  teacher_no: "",
  name: "",
  password: "",
  role: "teacher",
  phone: "",
  email: "",
  status: "active",
});

const roleOptions = [
  { label: "教师", value: "teacher" },
  { label: "管理员", value: "admin" },
];

function openAddModal() {
  isEdit.value = false;
  editId.value = null;
  formState.teacher_no = "";
  formState.name = "";
  formState.password = "";
  formState.role = "teacher";
  formState.phone = "";
  formState.email = "";
  formState.status = "active";
  modalVisible.value = true;
}

function openEditModal(record: TeacherOut) {
  isEdit.value = true;
  editId.value = record.id;
  formState.teacher_no = record.teacher_no;
  formState.name = record.name;
  formState.password = "";
  formState.role = record.role;
  formState.phone = record.phone || "";
  formState.email = record.email || "";
  formState.status = record.status;
  modalVisible.value = true;
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
    if (isEdit.value && editId.value !== null) {
      const payload: TeacherUpdate = {
        name: formState.name.trim(),
        role: formState.role,
        phone: formState.phone?.trim() || undefined,
        email: formState.email?.trim() || undefined,
        status: formState.status,
      };
      if (formState.password && formState.password.trim()) {
        payload.password = formState.password.trim();
      }
      await updateTeacher(editId.value, payload);
      message.success("教师信息更新成功");
    } else {
      const payload: TeacherCreate = {
        teacher_no: formState.teacher_no.trim(),
        name: formState.name.trim(),
        password: formState.password.trim(),
        role: formState.role,
        phone: formState.phone?.trim() || undefined,
        email: formState.email?.trim() || undefined,
      };
      await createTeacher(payload);
      message.success("教师添加成功");
    }
    closeModal();
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, isEdit.value ? "更新失败" : "添加失败"));
  } finally {
    modalLoading.value = false;
  }
}

async function handleDisable(record: TeacherOut) {
  try {
    await updateTeacher(record.id, { status: "disabled" });
    message.success("已禁用");
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "操作失败"));
  }
}

async function handleEnable(record: TeacherOut) {
  try {
    await updateTeacher(record.id, { status: "active" });
    message.success("已启用");
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "操作失败"));
  }
}

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="teacher-teachers">
    <div class="filter-bar teacher-card">
      <a-space wrap style="justify-content: space-between; width: 100%">
        <a-space wrap>
          <a-input
            v-model:value="filters.keyword"
            placeholder="搜索工号 / 姓名"
            allow-clear
            style="width: 240px"
            @press-enter="onSearch"
          />
          <a-select
            v-model:value="filters.role"
            placeholder="全部角色"
            allow-clear
            style="width: 120px"
            :options="roleOptions"
            @change="onSearch"
          />
          <a-button type="primary" @click="onSearch">查询</a-button>
          <a-button @click="onReset">重置</a-button>
        </a-space>
        <a-button type="primary" @click="openAddModal">添加教师</a-button>
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
        :scroll="{ x: 900 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button size="small" type="link" @click="openEditModal(record)">
                编辑
              </a-button>
              <a-button
                v-if="record.status === 'active'"
                size="small"
                type="link"
                danger
                @click="handleDisable(record)"
              >
                禁用
              </a-button>
              <a-button
                v-else
                size="small"
                type="link"
                @click="handleEnable(record)"
              >
                启用
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 添加/编辑教师弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="isEdit ? '编辑教师' : '添加教师'"
      :confirm-loading="modalLoading"
      @ok="handleSubmit"
      @cancel="closeModal"
      :ok-text="isEdit ? '保存' : '确认添加'"
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
          label="工号"
          name="teacher_no"
          :rules="[{ required: true, message: '请输入工号', trigger: 'blur' }]"
        >
          <a-input
            v-model:value="formState.teacher_no"
            placeholder="唯一工号"
            :maxlength="32"
            :disabled="isEdit"
          />
        </a-form-item>
        <a-form-item
          label="姓名"
          name="name"
          :rules="[{ required: true, message: '请输入姓名', trigger: 'blur' }]"
        >
          <a-input v-model:value="formState.name" placeholder="真实姓名" :maxlength="64" />
        </a-form-item>
        <a-form-item
          label="角色"
          name="role"
          :rules="[{ required: true, message: '请选择角色', trigger: 'change' }]"
        >
          <a-select v-model:value="formState.role" :options="roleOptions" placeholder="请选择" />
        </a-form-item>
        <a-form-item
          v-if="!isEdit"
          label="登录密码"
          name="password"
          :rules="[{ required: !isEdit, message: '请输入密码', trigger: 'blur' }]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="至少 4 位"
            :maxlength="64"
          />
        </a-form-item>
        <a-form-item v-else label="重置密码" name="password">
          <a-input-password
            v-model:value="formState.password"
            placeholder="留空则不修改"
            :maxlength="64"
          />
        </a-form-item>
        <a-form-item label="手机号" name="phone">
          <a-input v-model:value="formState.phone" placeholder="选填" :maxlength="20" />
        </a-form-item>
        <a-form-item label="邮箱" name="email">
          <a-input v-model:value="formState.email" placeholder="选填" :maxlength="128" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.teacher-teachers {
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
</style>
