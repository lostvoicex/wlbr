<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { message, Modal } from "ant-design-vue";
import type { TablePaginationConfig } from "ant-design-vue";
import {
  listMappings,
  createMapping,
  updateMapping,
  deleteMapping,
  reviewMapping,
  listMappingReviews,
  type KpMappingOut,
  type MappingCreate,
  type MappingUpdate,
  type MappingReviewInput,
  type MappingReviewOut,
} from "@/api/kpMappings";
import { importMappings, type ImportResult } from "@/api/adminData";
import { extractErrorMessage } from "@/api/client";

const loading = ref(false);
const dataSource = ref<KpMappingOut[]>([]);
const total = ref(0);

const filters = reactive({
  syllabus_version: undefined as string | undefined,
  knowledge_point: "",
  courseware_name: "",
  review_status: undefined as string | undefined,
});

const pagination = reactive<TablePaginationConfig>({
  current: 1,
  pageSize: 10,
  showSizeChanger: true,
  showTotal: (t: number) => `共 ${t} 条映射`,
});

const reviewStatusMap: Record<string, { text: string; color: string }> = {
  pending: { text: "待审核", color: "orange" },
  approved: { text: "已通过", color: "green" },
  rejected: { text: "已拒绝", color: "red" },
  needs_review: { text: "需复审", color: "blue" },
};

const sourceMap: Record<string, string> = {
  ai: "AI生成",
  manual: "手动添加",
  import: "批量导入",
};

const columns = [
  { title: "ID", dataIndex: "id", width: 70 },
  { title: "知识点", dataIndex: "knowledge_point", key: "knowledge_point", width: 180, ellipsis: true },
  { title: "课件名称", dataIndex: "courseware_name", key: "courseware_name", width: 180, ellipsis: true },
  { title: "章节", dataIndex: "chapter", width: 120 },
  { title: "页码", dataIndex: "page_ref", key: "page_ref", width: 80 },
  { title: "匹配度", dataIndex: "match_score", key: "match_score", width: 90 },
  { title: "来源", dataIndex: "source", key: "source", width: 90 },
  { title: "审核状态", dataIndex: "review_status", key: "review_status", width: 110 },
  { title: "审核等级", dataIndex: "review_level", key: "review_level", width: 90 },
  { title: "操作", key: "action", width: 240, fixed: "right" as const },
];

function formatMatchScore(score: number): { pct: number; color: string } {
  const pct = Math.round((score || 0) * 100);
  const color = pct >= 80 ? "green" : pct >= 60 ? "orange" : "red";
  return { pct, color };
}

function formatStars(level: number): string {
  if (!level) return "—";
  return "★".repeat(level) + "☆".repeat(5 - level);
}

function formatDate(text: string): string {
  return text ? text.slice(0, 19).replace("T", " ") : "";
}

async function fetchData() {
  loading.value = true;
  try {
    const data = await listMappings({
      syllabus_version: filters.syllabus_version,
      knowledge_point: filters.knowledge_point || undefined,
      courseware_name: filters.courseware_name || undefined,
      review_status: filters.review_status,
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
  filters.syllabus_version = undefined;
  filters.knowledge_point = "";
  filters.courseware_name = "";
  filters.review_status = undefined;
  pagination.current = 1;
  fetchData();
}

function onTableChange(p: TablePaginationConfig) {
  pagination.current = p.current || 1;
  pagination.pageSize = p.pageSize || 10;
  fetchData();
}

// ---------- 新建/编辑弹窗 ----------
const editModalVisible = ref(false);
const editMode = ref<"create" | "edit">("create");
const editingId = ref<number | null>(null);
const editLoading = ref(false);

const editForm = reactive<MappingCreate>({
  syllabus_version: "",
  knowledge_point: "",
  courseware_name: "",
  chapter: "",
  page_ref: "",
  chapter_title: "",
  match_score: 0.8,
  source: "manual",
  sort_order: 0,
});

function openCreate() {
  editMode.value = "create";
  editingId.value = null;
  Object.assign(editForm, {
    syllabus_version: "",
    knowledge_point: "",
    courseware_name: "",
    chapter: "",
    page_ref: "",
    chapter_title: "",
    match_score: 0.8,
    source: "manual",
    sort_order: 0,
  });
  editModalVisible.value = true;
}

function openEdit(record: KpMappingOut) {
  editMode.value = "edit";
  editingId.value = record.id;
  Object.assign(editForm, {
    syllabus_version: record.syllabus_version,
    knowledge_point: record.knowledge_point,
    courseware_name: record.courseware_name,
    chapter: record.chapter,
    page_ref: record.page_ref || "",
    chapter_title: record.chapter_title || "",
    match_score: record.match_score,
    source: record.source,
    sort_order: record.sort_order,
  });
  editModalVisible.value = true;
}

async function handleEditSubmit() {
  if (!editForm.syllabus_version.trim()) {
    message.warning("请输入课件版本");
    return;
  }
  if (!editForm.knowledge_point.trim()) {
    message.warning("请输入知识点");
    return;
  }
  if (!editForm.courseware_name.trim()) {
    message.warning("请输入课件名称");
    return;
  }
  if (!editForm.chapter.trim()) {
    message.warning("请输入章节");
    return;
  }
  editLoading.value = true;
  try {
    if (editMode.value === "create") {
      await createMapping({ ...editForm });
      message.success("创建成功");
    } else if (editingId.value !== null) {
      const updateData: MappingUpdate = { ...editForm };
      await updateMapping(editingId.value, updateData);
      message.success("更新成功");
    }
    editModalVisible.value = false;
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "操作失败"));
  } finally {
    editLoading.value = false;
  }
}

// ---------- 审核弹窗 ----------
const reviewModalVisible = ref(false);
const reviewingId = ref<number | null>(null);
const reviewLoading = ref(false);

const reviewForm = reactive<MappingReviewInput>({
  result: "approved",
  review_level: 3,
  note: "",
});

function openReview(record: KpMappingOut) {
  reviewingId.value = record.id;
  reviewForm.result = "approved";
  reviewForm.review_level = record.review_level || 3;
  reviewForm.note = "";
  reviewModalVisible.value = true;
}

async function handleReviewSubmit() {
  if (reviewingId.value === null) return;
  if (!reviewForm.review_level || reviewForm.review_level < 1 || reviewForm.review_level > 5) {
    message.warning("请选择审核等级（1-5）");
    return;
  }
  reviewLoading.value = true;
  try {
    await reviewMapping(reviewingId.value, { ...reviewForm });
    message.success("审核成功");
    reviewModalVisible.value = false;
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "审核失败"));
  } finally {
    reviewLoading.value = false;
  }
}

// ---------- 详情弹窗 ----------
const detailModalVisible = ref(false);
const detailRecord = ref<KpMappingOut | null>(null);
const reviewRecords = ref<MappingReviewOut[]>([]);
const detailLoading = ref(false);

async function openDetail(record: KpMappingOut) {
  detailRecord.value = record;
  reviewRecords.value = [];
  detailModalVisible.value = true;
  detailLoading.value = true;
  try {
    const reviews = await listMappingReviews(record.id);
    reviewRecords.value = reviews;
  } catch (e) {
    message.error(extractErrorMessage(e, "加载审核记录失败"));
  } finally {
    detailLoading.value = false;
  }
}

// ---------- 删除 ----------
function handleDelete(record: KpMappingOut) {
  Modal.confirm({
    title: "确认删除映射？",
    content: `知识点「${record.knowledge_point}」的映射将被删除，删除后不可恢复。`,
    okText: "确认删除",
    okType: "danger",
    cancelText: "取消",
    onOk: async () => {
      try {
        await deleteMapping(record.id);
        message.success("已删除");
        fetchData();
      } catch (e) {
        message.error(extractErrorMessage(e, "删除失败"));
      }
    },
  });
}

// ---------- 批量导入弹窗 ----------
const importModalVisible = ref(false);
const importText = ref("");
const importLoading = ref(false);
const importResult = ref<ImportResult | null>(null);

function openImport() {
  importText.value = "";
  importResult.value = null;
  importModalVisible.value = true;
}

async function handleImport() {
  if (!importText.value.trim()) {
    message.warning("请粘贴 JSON 数据");
    return;
  }
  let data: any[];
  try {
    const parsed = JSON.parse(importText.value);
    data = Array.isArray(parsed) ? parsed : [parsed];
  } catch {
    message.error("JSON 格式不正确，请检查");
    return;
  }
  importLoading.value = true;
  try {
    const result = await importMappings(data);
    importResult.value = result;
    message.success(`导入完成：成功 ${result.success} 条，失败 ${result.failed} 条`);
    fetchData();
  } catch (e) {
    message.error(extractErrorMessage(e, "导入失败"));
  } finally {
    importLoading.value = false;
  }
}

const importTemplate = `[
  {
    "syllabus_version": "Scratch一级",
    "knowledge_point": "循环结构",
    "courseware_name": "Scratch入门课件",
    "chapter": "第3章",
    "page_ref": "P15",
    "chapter_title": "循环的使用",
    "match_score": 0.85,
    "sort_order": 1
  }
]`;

function copyTemplate() {
  navigator.clipboard.writeText(importTemplate).then(() => {
    message.success("已复制模板到剪贴板");
  }).catch(() => {
    message.info("复制失败，请手动复制");
  });
}

// ---------- 导出 ----------
async function handleExport() {
  try {
    const data = await listMappings({
      syllabus_version: filters.syllabus_version,
      knowledge_point: filters.knowledge_point || undefined,
      courseware_name: filters.courseware_name || undefined,
      review_status: filters.review_status,
      page_size: 9999,
    });
    const json = JSON.stringify(data.items, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `kp-mappings-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    message.success("导出成功");
  } catch (e) {
    message.error(extractErrorMessage(e, "导出失败"));
  }
}

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="teacher-mappings">
    <div class="filter-bar teacher-card">
      <a-space wrap>
        <a-input
          v-model:value="filters.syllabus_version"
          placeholder="课件版本"
          allow-clear
          style="width: 160px"
          @press-enter="onSearch"
        />
        <a-input
          v-model:value="filters.knowledge_point"
          placeholder="知识点搜索"
          allow-clear
          style="width: 180px"
          @press-enter="onSearch"
        />
        <a-input
          v-model:value="filters.courseware_name"
          placeholder="课件名称搜索"
          allow-clear
          style="width: 180px"
          @press-enter="onSearch"
        />
        <a-select
          v-model:value="filters.review_status"
          placeholder="全部审核状态"
          allow-clear
          style="width: 140px"
          :options="[
            { value: 'pending', label: '待审核' },
            { value: 'approved', label: '已通过' },
            { value: 'rejected', label: '已拒绝' },
            { value: 'needs_review', label: '需复审' },
          ]"
        />
        <a-button type="primary" @click="onSearch">查询</a-button>
        <a-button @click="onReset">重置</a-button>
      </a-space>
    </div>

    <div class="table-wrap teacher-card">
      <div class="table-header">
        <div class="table-title">知识点映射</div>
        <a-space>
          <a-button @click="handleExport">导出</a-button>
          <a-button @click="openImport">批量导入</a-button>
          <a-button type="primary" @click="openCreate">新建映射</a-button>
        </a-space>
      </div>
      <a-table
        row-key="id"
        :columns="columns"
        :data-source="dataSource"
        :loading="loading"
        :pagination="pagination"
        @change="onTableChange"
        size="middle"
        :scroll="{ x: 1200 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'page_ref'">
            {{ record.page_ref || "—" }}
          </template>
          <template v-else-if="column.key === 'match_score'">
            <a-tag :color="formatMatchScore(record.match_score).color">
              {{ formatMatchScore(record.match_score).pct }}%
            </a-tag>
          </template>
          <template v-else-if="column.key === 'source'">
            {{ sourceMap[record.source] || record.source }}
          </template>
          <template v-else-if="column.key === 'review_status'">
            <a-tag :color="reviewStatusMap[record.review_status]?.color || 'default'">
              {{ reviewStatusMap[record.review_status]?.text || record.review_status }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'review_level'">
            {{ formatStars(record.review_level) }}
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <a-button size="small" type="link" @click="openDetail(record)">
                详情
              </a-button>
              <a-button size="small" type="link" @click="openReview(record)">
                审核
              </a-button>
              <a-button size="small" type="link" @click="openEdit(record)">
                编辑
              </a-button>
              <a-button size="small" type="link" danger @click="handleDelete(record)">
                删除
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 新建/编辑弹窗 -->
    <a-modal
      v-model:open="editModalVisible"
      :title="editMode === 'create' ? '新建映射' : '编辑映射'"
      :confirm-loading="editLoading"
      @ok="handleEditSubmit"
      ok-text="确认"
      cancel-text="取消"
      :mask-closable="false"
      width="560px"
    >
      <a-form layout="vertical" :model="editForm">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="课件版本" required>
              <a-input v-model:value="editForm.syllabus_version" placeholder="如：Scratch一级" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="来源">
              <a-select v-model:value="editForm.source">
                <a-select-option value="manual">手动添加</a-select-option>
                <a-select-option value="ai">AI生成</a-select-option>
                <a-select-option value="import">批量导入</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="知识点" required>
          <a-input v-model:value="editForm.knowledge_point" placeholder="请输入知识点名称" />
        </a-form-item>
        <a-form-item label="课件名称" required>
          <a-input v-model:value="editForm.courseware_name" placeholder="请输入课件名称" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="章节" required>
              <a-input v-model:value="editForm.chapter" placeholder="如：第3章" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="页码">
              <a-input v-model:value="editForm.page_ref" placeholder="如：P15" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="章节标题">
          <a-input v-model:value="editForm.chapter_title" placeholder="可选" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="匹配度 (0-1)">
              <a-input-number
                v-model:value="editForm.match_score"
                :min="0"
                :max="1"
                :step="0.05"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="排序">
              <a-input-number
                v-model:value="editForm.sort_order"
                :min="0"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>

    <!-- 审核弹窗 -->
    <a-modal
      v-model:open="reviewModalVisible"
      title="审核映射"
      :confirm-loading="reviewLoading"
      @ok="handleReviewSubmit"
      ok-text="提交审核"
      cancel-text="取消"
      :mask-closable="false"
      width="480px"
    >
      <a-form layout="vertical" :model="reviewForm">
        <a-form-item label="审核结果" required>
          <a-radio-group v-model:value="reviewForm.result">
            <a-radio value="approved">通过</a-radio>
            <a-radio value="rejected">拒绝</a-radio>
            <a-radio value="needs_review">需复审</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="审核等级 (1-5)" required>
          <a-rate v-model:value="reviewForm.review_level" :count="5" />
        </a-form-item>
        <a-form-item label="审核备注">
          <a-textarea
            v-model:value="reviewForm.note"
            placeholder="请输入审核备注（可选）"
            :rows="3"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 详情弹窗 -->
    <a-modal
      v-model:open="detailModalVisible"
      title="映射详情"
      :footer="null"
      width="640px"
    >
      <div v-if="detailRecord" class="detail-content">
        <a-descriptions :column="2" bordered size="small">
          <a-descriptions-item label="ID">{{ detailRecord.id }}</a-descriptions-item>
          <a-descriptions-item label="课件版本">{{ detailRecord.syllabus_version }}</a-descriptions-item>
          <a-descriptions-item label="知识点" :span="2">{{ detailRecord.knowledge_point }}</a-descriptions-item>
          <a-descriptions-item label="课件名称" :span="2">{{ detailRecord.courseware_name }}</a-descriptions-item>
          <a-descriptions-item label="章节">{{ detailRecord.chapter }}</a-descriptions-item>
          <a-descriptions-item label="页码">{{ detailRecord.page_ref || "—" }}</a-descriptions-item>
          <a-descriptions-item label="章节标题" :span="2">{{ detailRecord.chapter_title || "—" }}</a-descriptions-item>
          <a-descriptions-item label="匹配度">
            <a-tag :color="formatMatchScore(detailRecord.match_score).color">
              {{ formatMatchScore(detailRecord.match_score).pct }}%
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="来源">
            {{ sourceMap[detailRecord.source] || detailRecord.source }}
          </a-descriptions-item>
          <a-descriptions-item label="审核状态">
            <a-tag :color="reviewStatusMap[detailRecord.review_status]?.color || 'default'">
              {{ reviewStatusMap[detailRecord.review_status]?.text || detailRecord.review_status }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="审核等级">
            {{ formatStars(detailRecord.review_level) }}
          </a-descriptions-item>
          <a-descriptions-item label="创建时间" :span="2">
            {{ formatDate(detailRecord.created_at) }}
          </a-descriptions-item>
        </a-descriptions>

        <div class="review-timeline">
          <div class="timeline-title">审核记录</div>
          <a-spin v-if="detailLoading" />
          <a-timeline v-else-if="reviewRecords.length">
            <a-timeline-item v-for="r in reviewRecords" :key="r.id">
              <div class="review-item">
                <div class="review-head">
                  <span class="reviewer">{{ r.reviewer_name || "系统" }}</span>
                  <span class="review-round">第 {{ r.review_round }} 轮</span>
                  <a-tag v-if="r.result === 'approved'" color="green">通过</a-tag>
                  <a-tag v-else-if="r.result === 'rejected'" color="red">拒绝</a-tag>
                  <a-tag v-else-if="r.result === 'needs_review'" color="blue">需复审</a-tag>
                  <span class="review-level">等级：{{ "★".repeat(r.review_level) }}</span>
                </div>
                <div v-if="r.note" class="review-note">{{ r.note }}</div>
                <div class="review-time">
                  {{ formatDate(r.created_at) }}
                </div>
              </div>
            </a-timeline-item>
          </a-timeline>
          <div v-else class="empty-text">暂无审核记录</div>
        </div>
      </div>
    </a-modal>

    <!-- 批量导入弹窗 -->
    <a-modal
      v-model:open="importModalVisible"
      title="批量导入映射"
      :confirm-loading="importLoading"
      @ok="handleImport"
      ok-text="开始导入"
      cancel-text="取消"
      :mask-closable="false"
      width="640px"
    >
      <div class="import-section">
        <div class="import-hint">
          <span>请粘贴 JSON 格式的映射数据数组</span>
          <a-button type="link" size="small" @click="copyTemplate">复制模板</a-button>
        </div>
        <a-textarea
          v-model:value="importText"
          placeholder='[{"syllabus_version": "Scratch一级", "knowledge_point": "循环结构", ...}]'
          :rows="10"
          class="import-textarea"
        />
        <div v-if="importResult" class="import-result">
          <a-alert
            :message="`导入完成：共 ${importResult.total} 条，成功 ${importResult.success} 条，失败 ${importResult.failed} 条`"
            :type="importResult.failed > 0 ? 'warning' : 'success'"
            show-icon
          />
          <div v-if="importResult.errors && importResult.errors.length" class="import-errors">
            <div class="errors-title">错误详情：</div>
            <ul>
              <li v-for="(err, idx) in importResult.errors" :key="idx">{{ err }}</li>
            </ul>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<style scoped>
.teacher-mappings {
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
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.review-timeline {
  background: #fafafa;
  padding: 16px;
  border-radius: 6px;
}
.timeline-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--color-text);
}
.review-item {
  line-height: 1.6;
}
.review-head {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.reviewer {
  font-weight: 600;
  color: var(--color-text);
}
.review-round {
  color: var(--color-text-sub);
  font-size: 12px;
}
.review-level {
  color: var(--color-text-sub);
  font-size: 12px;
  margin-left: auto;
}
.review-note {
  color: var(--color-text);
  font-size: 13px;
  margin-top: 4px;
}
.review-time {
  color: var(--color-text-sub);
  font-size: 12px;
  margin-top: 4px;
}
.empty-text {
  color: var(--color-text-sub);
  font-size: 13px;
  text-align: center;
  padding: 20px;
}
.import-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.import-hint {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text-sub);
  font-size: 13px;
}
.import-textarea {
  font-family: "Consolas", "Monaco", monospace;
  font-size: 12px;
}
.import-result {
  margin-top: 8px;
}
.import-errors {
  margin-top: 8px;
  max-height: 120px;
  overflow-y: auto;
}
.errors-title {
  font-size: 12px;
  color: var(--color-text-sub);
  margin-bottom: 4px;
}
.import-errors ul {
  margin: 0;
  padding-left: 20px;
  font-size: 12px;
  color: #ff4d4f;
}
</style>
