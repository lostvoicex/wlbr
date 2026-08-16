<script setup lang="ts">
/**
 * 代码编辑器组件（Python / C++）— 基于 CodeMirror 6。
 *
 * 特性：
 *   - 专业语法高亮（CodeMirror 语言包）
 *   - 括号匹配、自动缩进、代码折叠
 *   - 撤销/重做、搜索替换（Ctrl+F）
 *   - Tab 缩进 4 空格
 *   - VS Code 风格暗色主题
 *   - 通过 v-model 双向绑定代码内容
 */
import { ref, computed, watch } from "vue";
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
import { cpp } from "@codemirror/lang-cpp";
import { oneDark } from "@codemirror/theme-one-dark";
import { indentUnit } from "@codemirror/language";
import { EditorView } from "@codemirror/view";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    language: "python" | "cpp";
    testCaseCount?: number;
    timeLimit?: number;
    placeholder?: string;
  }>(),
  {
    modelValue: "",
    placeholder: "在这里写代码～",
    testCaseCount: 0,
    timeLimit: 2,
  },
);

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const code = ref(props.modelValue);

watch(
  () => props.modelValue,
  (val) => {
    if (val !== code.value) {
      code.value = val;
    }
  },
);

watch(code, (val) => {
  emit("update:modelValue", val);
});

const langLabel = computed(() => (props.language === "python" ? "Python" : "C++"));
const langIcon = computed(() => (props.language === "python" ? "🐍" : "⚡"));

const extensions = computed(() => [
  props.language === "python" ? python() : cpp(),
  oneDark,
  indentUnit.of("    "),
  EditorView.theme({
    "&": {
      fontSize: "14px",
      borderRadius: "0 0 8px 8px",
      height: "280px",
      maxHeight: "400px",
    },
    ".cm-scroller": {
      fontFamily: "'Courier New', Consolas, 'Fira Code', monospace",
      lineHeight: "1.6",
    },
    ".cm-gutters": {
      borderRadius: "0 0 0 8px",
      borderRight: "1px solid #3a3a3a",
    },
    ".cm-content": {
      paddingBottom: "12px",
    },
    ".cm-activeLine": {
      backgroundColor: "rgba(255,255,255,0.04)",
    },
    ".cm-activeLineGutter": {
      backgroundColor: "rgba(255,255,255,0.04)",
    },
  }),
]);
</script>

<template>
  <div class="code-editor">
    <!-- 测试用例提示 -->
    <div v-if="props.testCaseCount" class="test-hint">
      🔍 这道题有 {{ props.testCaseCount }} 个测试用例，
      时间限制 {{ props.timeLimit }} 秒，认真写哦～
    </div>

    <!-- 编辑器头部 -->
    <div class="editor-header">
      <span class="lang-badge">
        {{ langIcon }} {{ langLabel }}
      </span>
      <span class="char-count">{{ code.length }} 字符</span>
    </div>

    <!-- CodeMirror 编辑器 -->
    <div class="editor-body">
      <Codemirror
        v-model="code"
        :placeholder="props.placeholder"
        :extensions="extensions"
        :autoDestroy="true"
        :style="{ height: '280px', maxHeight: '400px' }"
      />
    </div>

    <!-- 测试用例输入预览 -->
    <div v-if="props.testCaseCount" class="test-preview">
      <div class="preview-title">📋 测试用例输入预览（隐藏了答案哦）：</div>
      <div class="preview-hint">
        程序运行后，输出要和老师预设的正确答案一样才算通过～
      </div>
    </div>
  </div>
</template>

<style scoped>
.code-editor {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.test-hint {
  background: #fff9db;
  padding: 10px 14px;
  border-radius: 12px;
  color: #664c00;
  font-size: 15px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #282c34;
  border-radius: 8px 8px 0 0;
}
.lang-badge {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}
.char-count {
  color: #848484;
  font-size: 13px;
  font-family: monospace;
}

.editor-body {
  border-radius: 0 0 8px 8px;
  overflow: hidden;
}

.editor-body :deep(.cm-editor) {
  border-radius: 0 0 8px 8px;
}

.editor-body :deep(.cm-focused) {
  outline: none;
}

.test-preview {
  background: #f0f5ff;
  padding: 10px 14px;
  border-radius: 12px;
}
.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: #1677ff;
  margin-bottom: 4px;
}
.preview-hint {
  font-size: 13px;
  color: var(--color-text-sub);
}
</style>
