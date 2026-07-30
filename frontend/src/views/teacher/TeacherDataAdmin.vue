<script setup lang="ts">
import { ref, reactive } from "vue";
import { message } from "ant-design-vue";
import { useRouter } from "vue-router";
import {
  importQuestions,
  importMappings,
  importStudents,
  exportQuestions,
  exportMappings,
  exportStudents,
  type ImportResult,
} from "@/api/adminData";
import { extractErrorMessage } from "@/api/client";

const router = useRouter();
const activeTab = ref("questions");

// ---------- 题库导入 ----------
const questionImportText = ref("");
const questionImportLoading = ref(false);
const questionImportResult = ref<ImportResult | null>(null);

const questionTemplate = `[
  {
    "knowledge_point": "循环结构",
    "q_type": "single",
    "content": "以下哪个是正确的循环积木？",
    "options": ["重复执行", "如果那么", "等待", "广播"],
    "answer": "A",
    "difficulty": 2,
    "syllabus_version": "Scratch一级"
  }
]`;

async function handleQuestionImport() {
  if (!questionImportText.value.trim()) {
    message.warning("请粘贴题目 JSON 数据");
    return;
  }
  let data: any[];
  try {
    const parsed = JSON.parse(questionImportText.value);
    data = Array.isArray(parsed) ? parsed : [parsed];
  } catch {
    message.error("JSON 格式不正确，请检查");
    return;
  }
  questionImportLoading.value = true;
  try {
    const result = await importQuestions(data);
    questionImportResult.value = result;
    message.success(`导入完成：成功 ${result.success} 条，失败 ${result.failed} 条`);
  } catch (e) {
    message.error(extractErrorMessage(e, "导入失败"));
  } finally {
    questionImportLoading.value = false;
  }
}

async function handleQuestionExport() {
  try {
    const data = await exportQuestions();
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `questions-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    message.success("导出成功");
  } catch (e) {
    message.error(extractErrorMessage(e, "导出失败"));
  }
}

function copyQuestionTemplate() {
  navigator.clipboard.writeText(questionTemplate).then(() => {
    message.success("已复制模板到剪贴板");
  }).catch(() => {
    message.info("复制失败，请手动复制");
  });
}

// ---------- 映射导入 ----------
const mappingImportText = ref("");
const mappingImportLoading = ref(false);
const mappingImportResult = ref<ImportResult | null>(null);

const mappingTemplate = `[
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

async function handleMappingImport() {
  if (!mappingImportText.value.trim()) {
    message.warning("请粘贴映射 JSON 数据");
    return;
  }
  let data: any[];
  try {
    const parsed = JSON.parse(mappingImportText.value);
    data = Array.isArray(parsed) ? parsed : [parsed];
  } catch {
    message.error("JSON 格式不正确，请检查");
    return;
  }
  mappingImportLoading.value = true;
  try {
    const result = await importMappings(data);
    mappingImportResult.value = result;
    message.success(`导入完成：成功 ${result.success} 条，失败 ${result.failed} 条`);
  } catch (e) {
    message.error(extractErrorMessage(e, "导入失败"));
  } finally {
    mappingImportLoading.value = false;
  }
}

async function handleMappingExport() {
  try {
    const data = await exportMappings();
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `mappings-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    message.success("导出成功");
  } catch (e) {
    message.error(extractErrorMessage(e, "导出失败"));
  }
}

function copyMappingTemplate() {
  navigator.clipboard.writeText(mappingTemplate).then(() => {
    message.success("已复制模板到剪贴板");
  }).catch(() => {
    message.info("复制失败，请手动复制");
  });
}

function goToMappings() {
  router.push({ name: "TeacherMappings" });
}

// ---------- 学员导入 ----------
const studentImportText = ref("");
const studentImportLoading = ref(false);
const studentImportResult = ref<ImportResult | null>(null);

const studentTemplate = `[
  {
    "name": "张三",
    "grade": 3,
    "phone": "13800138000",
    "syllabus_target": "Scratch一级"
  }
]`;

async function handleStudentImport() {
  if (!studentImportText.value.trim()) {
    message.warning("请粘贴学员 JSON 数据");
    return;
  }
  let data: any[];
  try {
    const parsed = JSON.parse(studentImportText.value);
    data = Array.isArray(parsed) ? parsed : [parsed];
  } catch {
    message.error("JSON 格式不正确，请检查");
    return;
  }
  studentImportLoading.value = true;
  try {
    const result = await importStudents(data);
    studentImportResult.value = result;
    message.success(`导入完成：成功 ${result.success} 条，失败 ${result.failed} 条`);
  } catch (e) {
    message.error(extractErrorMessage(e, "导入失败"));
  } finally {
    studentImportLoading.value = false;
  }
}

async function handleStudentExport() {
  try {
    const data = await exportStudents();
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `students-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    message.success("导出成功");
  } catch (e) {
    message.error(extractErrorMessage(e, "导出失败"));
  }
}

function copyStudentTemplate() {
  navigator.clipboard.writeText(studentTemplate).then(() => {
    message.success("已复制模板到剪贴板");
  }).catch(() => {
    message.info("复制失败，请手动复制");
  });
}

function goToStudents() {
  router.push({ name: "TeacherStudents" });
}
</script>

<template>
  <div class="teacher-data-admin">
    <div class="page-header teacher-card">
      <div class="page-title">资料管理</div>
      <div class="page-subtitle">题库、映射、学员的批量导入导出通道</div>
    </div>

    <div class="tabs-card teacher-card">
      <a-tabs v-model:activeKey="activeTab" size="large">
        <!-- 题库管理 -->
        <a-tab-pane key="questions" tab="题库管理">
          <div class="tab-content">
            <div class="section-head">
              <div class="section-title">题库导入导出</div>
              <a-space>
                <a-button @click="handleQuestionExport">全部导出</a-button>
                <a-button type="primary" :loading="questionImportLoading" @click="handleQuestionImport">
                  开始导入
                </a-button>
              </a-space>
            </div>

            <div class="import-hint">
              <span>请粘贴 JSON 格式的题目数组，支持 single / judge / coding 题型</span>
              <a-button type="link" size="small" @click="copyQuestionTemplate">复制导入模板</a-button>
            </div>

            <a-textarea
              v-model:value="questionImportText"
              placeholder='[{"knowledge_point": "循环结构", "q_type": "single", "content": "...", ...}]'
              :rows="12"
              class="import-textarea"
            />

            <div v-if="questionImportResult" class="import-result">
              <a-alert
                :message="`导入结果：共 ${questionImportResult.total} 条，成功 ${questionImportResult.success} 条，失败 ${questionImportResult.failed} 条`"
                :type="questionImportResult.failed > 0 ? 'warning' : 'success'"
                show-icon
              />
              <div v-if="questionImportResult.errors && questionImportResult.errors.length" class="import-errors">
                <div class="errors-title">错误详情：</div>
                <ul>
                  <li v-for="(err, idx) in questionImportResult.errors" :key="idx">{{ err }}</li>
                </ul>
              </div>
            </div>

            <div class="preview-section">
              <div class="preview-title">导入字段说明</div>
              <a-descriptions :column="2" bordered size="small">
                <a-descriptions-item label="knowledge_point">知识点名称（必填）</a-descriptions-item>
                <a-descriptions-item label="q_type">题型：single / judge / coding（必填）</a-descriptions-item>
                <a-descriptions-item label="content">题目内容（必填）</a-descriptions-item>
                <a-descriptions-item label="options">选项数组（单选题必填）</a-descriptions-item>
                <a-descriptions-item label="answer">正确答案（必填）</a-descriptions-item>
                <a-descriptions-item label="difficulty">难度：1-5（选填）</a-descriptions-item>
                <a-descriptions-item label="syllabus_version">大纲版本（选填）</a-descriptions-item>
                <a-descriptions-item label="blocks">编程题积木块列表（选填）</a-descriptions-item>
              </a-descriptions>
            </div>
          </div>
        </a-tab-pane>

        <!-- 映射管理 -->
        <a-tab-pane key="mappings" tab="映射管理">
          <div class="tab-content">
            <div class="section-head">
              <div class="section-title">知识点映射导入导出</div>
              <a-space>
                <a-button @click="goToMappings">前往映射管理页</a-button>
                <a-button @click="handleMappingExport">全部导出</a-button>
                <a-button type="primary" :loading="mappingImportLoading" @click="handleMappingImport">
                  开始导入
                </a-button>
              </a-space>
            </div>

            <div class="import-hint">
              <span>请粘贴 JSON 格式的映射数组</span>
              <a-button type="link" size="small" @click="copyMappingTemplate">复制导入模板</a-button>
            </div>

            <a-textarea
              v-model:value="mappingImportText"
              placeholder='[{"syllabus_version": "Scratch一级", "knowledge_point": "循环结构", ...}]'
              :rows="12"
              class="import-textarea"
            />

            <div v-if="mappingImportResult" class="import-result">
              <a-alert
                :message="`导入结果：共 ${mappingImportResult.total} 条，成功 ${mappingImportResult.success} 条，失败 ${mappingImportResult.failed} 条`"
                :type="mappingImportResult.failed > 0 ? 'warning' : 'success'"
                show-icon
              />
              <div v-if="mappingImportResult.errors && mappingImportResult.errors.length" class="import-errors">
                <div class="errors-title">错误详情：</div>
                <ul>
                  <li v-for="(err, idx) in mappingImportResult.errors" :key="idx">{{ err }}</li>
                </ul>
              </div>
            </div>

            <div class="preview-section">
              <div class="preview-title">导入字段说明</div>
              <a-descriptions :column="2" bordered size="small">
                <a-descriptions-item label="syllabus_version">课件/大纲版本（必填）</a-descriptions-item>
                <a-descriptions-item label="knowledge_point">知识点名称（必填）</a-descriptions-item>
                <a-descriptions-item label="courseware_name">课件名称（必填）</a-descriptions-item>
                <a-descriptions-item label="chapter">章节（必填）</a-descriptions-item>
                <a-descriptions-item label="page_ref">页码引用（选填）</a-descriptions-item>
                <a-descriptions-item label="chapter_title">章节标题（选填）</a-descriptions-item>
                <a-descriptions-item label="match_score">匹配度 0-1（选填，默认 0.8）</a-descriptions-item>
                <a-descriptions-item label="sort_order">排序（选填，默认 0）</a-descriptions-item>
              </a-descriptions>
            </div>
          </div>
        </a-tab-pane>

        <!-- 学员管理 -->
        <a-tab-pane key="students" tab="学员管理">
          <div class="tab-content">
            <div class="section-head">
              <div class="section-title">学员批量导入导出</div>
              <a-space>
                <a-button @click="goToStudents">前往学员列表</a-button>
                <a-button @click="handleStudentExport">全部导出</a-button>
                <a-button type="primary" :loading="studentImportLoading" @click="handleStudentImport">
                  开始导入
                </a-button>
              </a-space>
            </div>

            <div class="import-hint">
              <span>请粘贴 JSON 格式的学员数组</span>
              <a-button type="link" size="small" @click="copyStudentTemplate">复制导入模板</a-button>
            </div>

            <a-textarea
              v-model:value="studentImportText"
              placeholder='[{"name": "张三", "grade": 3, "phone": "13800138000", ...}]'
              :rows="12"
              class="import-textarea"
            />

            <div v-if="studentImportResult" class="import-result">
              <a-alert
                :message="`导入结果：共 ${studentImportResult.total} 条，成功 ${studentImportResult.success} 条，失败 ${studentImportResult.failed} 条`"
                :type="studentImportResult.failed > 0 ? 'warning' : 'success'"
                show-icon
              />
              <div v-if="studentImportResult.errors && studentImportResult.errors.length" class="import-errors">
                <div class="errors-title">错误详情：</div>
                <ul>
                  <li v-for="(err, idx) in studentImportResult.errors" :key="idx">{{ err }}</li>
                </ul>
              </div>
            </div>

            <div class="preview-section">
              <div class="preview-title">导入字段说明</div>
              <a-descriptions :column="2" bordered size="small">
                <a-descriptions-item label="name">学员姓名（必填）</a-descriptions-item>
                <a-descriptions-item label="grade">年级（必填）</a-descriptions-item>
                <a-descriptions-item label="phone">手机号（选填）</a-descriptions-item>
                <a-descriptions-item label="syllabus_target">目标大纲（选填）</a-descriptions-item>
                <a-descriptions-item label="password">初始密码（选填，默认 123456）</a-descriptions-item>
                <a-descriptions-item label="student_no">学号（选填）</a-descriptions-item>
              </a-descriptions>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>

<style scoped>
.teacher-data-admin {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.page-header {
  padding: 20px 24px;
}
.page-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
}
.page-subtitle {
  font-size: 13px;
  color: var(--color-text-sub);
  margin-top: 4px;
}
.tabs-card {
  padding: 0;
  overflow: hidden;
}
.tabs-card :deep(.ant-tabs) {
  padding: 0 20px;
}
.tabs-card :deep(.ant-tabs-content-holder) {
  padding: 0 4px 20px;
}
.tab-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
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
  margin-top: 4px;
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
.preview-section {
  background: #fafafa;
  padding: 16px;
  border-radius: 6px;
}
.preview-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--color-text);
}
</style>
