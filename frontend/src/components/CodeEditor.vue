<script setup lang="ts">
/**
 * 代码编辑器组件（Python / C++）。
 *
 * 特性：
 *   - textarea + 行号 + Tab 缩进
 *   - 轻量级语法高亮（正则匹配，无外部依赖）
 *   - 通过 v-model 双向绑定代码内容
 */
import { ref, computed, watch, nextTick } from "vue";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    language: "python" | "cpp";
    /** 测试用例数量（展示用） */
    testCaseCount?: number;
    /** 时间限制（秒） */
    timeLimit?: number;
    /** 占位提示 */
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

const textareaRef = ref<HTMLTextAreaElement | null>(null);
const highlightRef = ref<HTMLPreElement | null>(null);
const lineHeight = 22; // px
const minLines = 8;

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

const lineCount = computed(() => {
  const n = code.value.split("\n").length;
  return Math.max(n, minLines);
});

const lineNumbers = computed(() => {
  return Array.from({ length: lineCount.value }, (_, i) => i + 1);
});

const langLabel = computed(() => {
  return props.language === "python" ? "Python" : "C++";
});

const langIcon = computed(() => {
  return props.language === "python" ? "🐍" : "⚡";
});

/* ---------- 轻量级语法高亮 ---------- */

const pythonKeywords =
  /\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|with|raise|finally|lambda|yield|assert|del|global|nonlocal|pass|break|continue|and|or|not|in|is|None|True|False|print|input|len|range|open|str|int|float|list|dict|tuple|set)\b/g;

const cppKeywords =
  /\b(int|float|double|char|void|bool|string|if|else|for|while|do|return|break|continue|switch|case|default|goto|try|catch|throw|include|using|namespace|class|struct|enum|union|public|private|protected|virtual|override|static|const|constexpr|mutable|volatile|explicit|inline|friend|template|typename|auto|new|delete|this|true|false|null|nullptr|sizeof|typedef|using|namespace|std|cin|cout|endl|vector|map|set|string)\b/g;

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function highlightCode(text: string, lang: "python" | "cpp"): string {
  if (!text) return "";
  // 先转义 HTML
  let html = escapeHtml(text);
  // 匹配字符串（简单匹配单行字符串）
  html = html.replace(
    /(&quot;.*?&quot;|&#039;.*?&#039;)/g,
    '<span class="token-string">$1</span>',
  );
  // 匹配注释
  if (lang === "python") {
    html = html.replace(
      /(#.*$)/gm,
      '<span class="token-comment">$1</span>',
    );
  } else {
    html = html.replace(
      /(\/\/.*$)/gm,
      '<span class="token-comment">$1</span>',
    );
  }
  // 匹配关键字
  const kwRe = lang === "python" ? pythonKeywords : cppKeywords;
  html = html.replace(kwRe, '<span class="token-keyword">$1</span>');
  // 匹配数字
  html = html.replace(
    /\b(\d+(?:\.\d+)?)\b/g,
    '<span class="token-number">$1</span>',
  );
  // 末尾补一个换行，让 pre 和 textarea 高度对齐
  if (!html.endsWith("\n")) html += "\n";
  return html;
}

const highlightedCode = computed(() => highlightCode(code.value, props.language));

/* ---------- 事件处理 ---------- */

function onInput(e: Event) {
  const target = e.target as HTMLTextAreaElement;
  code.value = target.value;
}

function syncScroll() {
  const ta = textareaRef.value;
  const gutter = document.querySelector(".code-gutter") as HTMLElement | null;
  const pre = highlightRef.value;
  if (ta && gutter) {
    gutter.scrollTop = ta.scrollTop;
  }
  if (ta && pre) {
    pre.scrollTop = ta.scrollTop;
    pre.scrollLeft = ta.scrollLeft;
  }
}

// Tab 键缩进 + 括号自动补全
function onKeydown(e: KeyboardEvent) {
  const ta = e.target as HTMLTextAreaElement;
  const start = ta.selectionStart;
  const end = ta.selectionEnd;

  if (e.key === "Tab") {
    e.preventDefault();
    const indent = "    "; // 4 spaces
    code.value = code.value.slice(0, start) + indent + code.value.slice(end);
    emit("update:modelValue", code.value);
    nextTick(() => {
      ta.selectionStart = ta.selectionEnd = start + indent.length;
    });
    return;
  }

  // 括号自动补全
  const pairs: Record<string, string> = {
    "(": ")",
    "{": "}",
    "[": "]",
    '"': '"',
    "'": "'",
  };
  if (pairs[e.key] && !e.ctrlKey && !e.altKey && !e.metaKey) {
    e.preventDefault();
    const close = pairs[e.key];
    code.value =
      code.value.slice(0, start) + e.key + close + code.value.slice(end);
    emit("update:modelValue", code.value);
    nextTick(() => {
      ta.selectionStart = ta.selectionEnd = start + 1;
    });
    return;
  }

  // 回车自动缩进（简单版：复制上一行前缀空白）
  if (e.key === "Enter") {
    e.preventDefault();
    const lineStart = code.value.lastIndexOf("\n", start - 1) + 1;
    const linePrefix = code.value.slice(lineStart, start).match(/^\s*/)?.[0] || "";
    const insert = "\n" + linePrefix;
    code.value = code.value.slice(0, start) + insert + code.value.slice(end);
    emit("update:modelValue", code.value);
    nextTick(() => {
      ta.selectionStart = ta.selectionEnd = start + insert.length;
    });
  }
}
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

    <!-- 代码编辑区 -->
    <div class="editor-body">
      <div class="code-gutter">
        <div
          v-for="n in lineNumbers"
          :key="n"
          class="line-num"
          :style="{ height: lineHeight + 'px' }"
        >
          {{ n }}
        </div>
      </div>
      <div class="code-area">
        <!-- 高亮层 -->
        <pre
          ref="highlightRef"
          class="highlight-layer"
          :style="{ lineHeight: lineHeight + 'px' }"
          v-html="highlightedCode"
        ></pre>
        <!-- 编辑层 -->
        <textarea
          ref="textareaRef"
          class="code-textarea"
          :value="code"
          :placeholder="props.placeholder"
          :style="{ lineHeight: lineHeight + 'px' }"
          spellcheck="false"
          @input="onInput"
          @scroll="syncScroll"
          @keydown="onKeydown"
        ></textarea>
      </div>
    </div>

    <!-- 测试用例输入预览（如果有） -->
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
  background: #2d2d2d;
  border-radius: 8px 8px 0 0;
}
.lang-badge {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}
.char-count {
  color: #888;
  font-size: 13px;
  font-family: monospace;
}

.editor-body {
  display: flex;
  background: #1e1e1e;
  border-radius: 0 0 8px 8px;
  overflow: hidden;
  min-height: 200px;
}
.code-gutter {
  flex-shrink: 0;
  padding: 12px 8px 12px 12px;
  background: #2d2d2d;
  color: #858585;
  font-family: "Courier New", Consolas, monospace;
  font-size: 14px;
  text-align: right;
  overflow: hidden;
  user-select: none;
}
.line-num {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.code-area {
  position: relative;
  flex: 1;
  min-height: 176px;
}

/* 高亮层：与 textarea 完全重叠 */
.highlight-layer {
  position: absolute;
  inset: 0;
  margin: 0;
  padding: 12px 16px;
  background: #1e1e1e;
  color: #d4d4d4;
  border: none;
  font-family: "Courier New", Consolas, "Fira Code", monospace;
  font-size: 14px;
  tab-size: 4;
  white-space: pre;
  overflow: auto;
  pointer-events: none; /* 让点击穿透到 textarea */
  z-index: 1;
}

/* 语法高亮颜色 */
:deep(.token-keyword) {
  color: #569cd6;
  font-weight: 600;
}
:deep(.token-string) {
  color: #ce9178;
}
:deep(.token-comment) {
  color: #6a9955;
  font-style: italic;
}
:deep(.token-number) {
  color: #b5cea8;
}

.code-textarea {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  padding: 12px 16px;
  background: transparent;
  color: transparent; /* 文字透明，只保留光标 */
  caret-color: #d4d4d4; /* 光标颜色 */
  border: none;
  outline: none;
  resize: none;
  font-family: "Courier New", Consolas, "Fira Code", monospace;
  font-size: 14px;
  tab-size: 4;
  white-space: pre;
  overflow: auto;
  z-index: 2;
}
.code-textarea::placeholder {
  color: #666;
  caret-color: #d4d4d4;
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
