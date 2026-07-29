<script setup lang="ts">
/**
 * Scratch 编程大题编辑器组件。
 *
 * 提供两种方式提交 .sb3 作品：
 *   1. 在线编辑：内嵌 TurboWarp 编辑器（iframe），做完后导出 .sb3 再上传
 *   2. 上传文件：直接选择本地 .sb3 文件
 *
 * 通过 emit("update:sb3", base64String) 向父组件传递 base64 编码的 sb3 内容。
 */
import { ref, onMounted, onUnmounted } from "vue";
import { message } from "ant-design-vue";

const props = defineProps<{
  /** 判题规则数量（展示用） */
  checkCount?: number;
}>();

const emit = defineEmits<{
  (e: "update:sb3", value: string): void;
}>();

const mode = ref<"editor" | "upload">("editor");
const fileName = ref<string>("");
const sb3Base64 = ref<string>("");
const fileInput = ref<HTMLInputElement | null>(null);
const dragOver = ref(false);
const uploadError = ref<string>("");

// 文件大小限制 5MB
const MAX_FILE_SIZE = 5 * 1024 * 1024;

// TurboWarp 编辑器 URL（支持 iframe 嵌入）
const turbowarpUrl = "https://turbowarp.org/editor?fullscreen";

// iframe 加载状态
const iframeLoaded = ref(false);
const iframeRef = ref<HTMLIFrameElement | null>(null);

function onIframeLoad() {
  iframeLoaded.value = true;
}

function triggerUpload() {
  fileInput.value?.click();
}

function handleFile(file: File) {
  uploadError.value = "";
  if (!file) return;
  if (!file.name.endsWith(".sb3")) {
    uploadError.value = "请选择 .sb3 格式的 Scratch 作品文件～";
    message.warning(uploadError.value);
    return;
  }
  if (file.size > MAX_FILE_SIZE) {
    uploadError.value = `文件太大了（${(file.size / 1024 / 1024).toFixed(1)}MB），请压缩到 5MB 以内～`;
    message.warning(uploadError.value);
    return;
  }
  fileName.value = file.name;
  const reader = new FileReader();
  reader.onload = () => {
    const result = reader.result;
    if (typeof result === "string") {
      const base64 = result.split(",")[1] || "";
      if (!base64) {
        uploadError.value = "文件读取失败，请重新选择～";
        message.error(uploadError.value);
        return;
      }
      sb3Base64.value = base64;
      emit("update:sb3", base64);
      message.success(`作品 "${file.name}" 已准备好！`);
    }
  };
  reader.onerror = () => {
    uploadError.value = "文件读取出错，请重试～";
    message.error(uploadError.value);
  };
  reader.readAsDataURL(file);
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    handleFile(target.files[0]);
  }
}

function onDrop(e: DragEvent) {
  e.preventDefault();
  dragOver.value = false;
  if (e.dataTransfer && e.dataTransfer.files[0]) {
    handleFile(e.dataTransfer.files[0]);
  }
}

function onDragOver(e: DragEvent) {
  e.preventDefault();
  dragOver.value = true;
}

function onDragLeave() {
  dragOver.value = false;
}

function clearFile() {
  fileName.value = "";
  sb3Base64.value = "";
  uploadError.value = "";
  emit("update:sb3", "");
  if (fileInput.value) fileInput.value.value = "";
}

// 监听 TurboWarp 的 postMessage（如果支持导出回调）
function handleMessage(event: MessageEvent) {
  if (event.origin !== "https://turbowarp.org") return;
  const data = event.data;
  if (data && data.type === "sb3-export" && data.sb3) {
    sb3Base64.value = data.sb3;
    fileName.value = "从编辑器导出的作品.sb3";
    emit("update:sb3", data.sb3);
    message.success("作品已从编辑器导出！");
  }
}

onMounted(() => {
  window.addEventListener("message", handleMessage);
});

onUnmounted(() => {
  window.removeEventListener("message", handleMessage);
});
</script>

<template>
  <div class="scratch-editor">
    <!-- 判题规则提示 -->
    <div v-if="props.checkCount" class="rules-hint">
      🔍 老师 say：这道题有 {{ props.checkCount }} 条检查规则，认真做好每一步哦～
    </div>

    <!-- 模式切换 -->
    <div class="mode-tabs">
      <button
        :class="['tab-btn', { active: mode === 'editor' }]"
        @click="mode = 'editor'"
      >
        🎮 在线编辑
      </button>
      <button
        :class="['tab-btn', { active: mode === 'upload' }]"
        @click="mode = 'upload'"
      >
        📁 上传作品
      </button>
    </div>

    <!-- 内嵌编辑器模式 -->
    <div v-if="mode === 'editor'" class="editor-mode">
      <div class="editor-hint-bar">
        <div class="hint-text">
          🐱 在下面的编辑器里搭积木，做完后点编辑器左上角的
          <strong>「文件」→「保存到电脑」</strong>
          导出 .sb3 文件，然后切到「上传作品」提交～
        </div>
      </div>
      <div class="iframe-wrapper">
        <iframe
          ref="iframeRef"
          :src="turbowarpUrl"
          class="turbowarp-iframe"
          allow="fullscreen; autoplay; camera; microphone"
          allowfullscreen
          @load="onIframeLoad"
        ></iframe>
        <div v-if="!iframeLoaded" class="iframe-loading">
          <div class="loading-icon">⏳</div>
          <div>正在加载 Scratch 编辑器...</div>
          <div class="loading-sub">首次加载可能需要 5-10 秒</div>
        </div>
      </div>
      <div class="editor-steps">
        <div class="step"><span class="step-num">1</span> 在上方编辑器里按题目要求搭积木</div>
        <div class="step"><span class="step-num">2</span> 点编辑器左上角「文件」→「保存到电脑」</div>
        <div class="step"><span class="step-num">3</span> 切到「上传作品」上传你的 .sb3 文件</div>
      </div>
    </div>

    <!-- 上传模式 -->
    <div v-if="mode === 'upload'" class="upload-mode">
      <div
        :class="['drop-zone', { 'drag-over': dragOver, 'has-file': !!fileName }]"
        @click="triggerUpload"
        @drop="onDrop"
        @dragover="onDragOver"
        @dragleave="onDragLeave"
      >
        <input
          ref="fileInput"
          type="file"
          accept=".sb3"
          style="display: none"
          @change="onFileChange"
        />
        <template v-if="!fileName">
          <div class="drop-icon">📦</div>
          <div class="drop-text">点击选择 .sb3 文件</div>
          <div class="drop-hint">或者把文件拖到这里～</div>
          <div class="drop-limit">文件大小限制：5MB</div>
        </template>
        <template v-else>
          <div class="drop-icon done">✅</div>
          <div class="drop-file-name">{{ fileName }}</div>
          <div class="drop-file-hint">作品已准备好，点击下方"提交判题"按钮～</div>
        </template>
      </div>
      <!-- 错误提示 -->
      <div v-if="uploadError" class="upload-error">
        ⚠️ {{ uploadError }}
      </div>
      <button v-if="fileName" class="clear-btn" @click.stop="clearFile">
        重新选择文件
      </button>
    </div>
  </div>
</template>

<style scoped>
.scratch-editor {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.rules-hint {
  background: #fff9db;
  padding: 10px 14px;
  border-radius: 12px;
  color: #664c00;
  font-size: 15px;
}

.mode-tabs {
  display: flex;
  gap: 8px;
}
.tab-btn {
  flex: 1;
  padding: 10px 12px;
  border-radius: 12px;
  border: 2px solid var(--color-border);
  background: #fffbf7;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s ease-out;
}
.tab-btn.active {
  border-color: var(--color-primary);
  background: #fff2e8;
  color: var(--color-primary);
}

/* 内嵌编辑器模式 */
.editor-mode {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.editor-hint-bar {
  background: #f0f5ff;
  padding: 12px 14px;
  border-radius: var(--radius-md);
}
.hint-text {
  font-size: 14px;
  color: #1d39c4;
  line-height: 1.6;
}
.hint-text strong {
  color: var(--color-primary);
  font-weight: 700;
}
.iframe-wrapper {
  position: relative;
  width: 100%;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px solid var(--color-border);
  background: #1e1e1e;
}
.turbowarp-iframe {
  width: 100%;
  height: 500px;
  border: none;
  display: block;
}
.iframe-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #1e1e1e;
  color: #fff;
  font-size: 16px;
}
.loading-icon {
  font-size: 40px;
  animation: spin 1.5s linear infinite;
}
.loading-sub {
  font-size: 13px;
  color: #888;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.editor-steps {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background: #fafafa;
  border-radius: var(--radius-md);
}
.step {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: var(--color-text-sub);
}
.step-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

/* 上传模式 */
.upload-mode {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.drop-zone {
  width: 100%;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  padding: 32px 16px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s ease-out, background 0.2s ease-out;
}
.drop-zone.drag-over {
  border-color: var(--color-primary);
  background: #fff2e8;
}
.drop-zone.has-file {
  border-color: var(--color-pass);
  background: #f6ffed;
  border-style: solid;
}
.drop-icon {
  font-size: 48px;
  margin-bottom: 8px;
}
.drop-icon.done {
  color: var(--color-pass);
}
.drop-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 4px;
}
.drop-hint {
  font-size: 14px;
  color: var(--color-text-sub);
}
.drop-limit {
  font-size: 12px;
  color: #aaa;
  margin-top: 6px;
}
.drop-file-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-pass);
  margin-bottom: 4px;
  word-break: break-all;
}
.drop-file-hint {
  font-size: 14px;
  color: var(--color-text-sub);
}
.upload-error {
  width: 100%;
  padding: 10px 14px;
  background: #fff1f0;
  border: 1px solid #ffccc7;
  border-radius: 8px;
  color: #cf1322;
  font-size: 14px;
}
.clear-btn {
  margin-top: 8px;
  background: none;
  border: none;
  color: var(--color-secondary);
  cursor: pointer;
  font-size: 14px;
  font-family: inherit;
}
</style>
