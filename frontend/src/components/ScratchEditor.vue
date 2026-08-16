<script setup lang="ts">
/**
 * Scratch 编程大题编辑器组件。
 *
 * 两种模式：
 *   1. 在线编辑（默认）：页面内嵌入 TurboWarp iframe，做好后一键获取作品
 *   2. 上传文件：直接选择本地 .sb3 文件（备用）
 *
 * 通过 emit("update:sb3", base64String) 向父组件传递 base64 编码的 sb3 内容。
 */
import { ref, onMounted, onUnmounted } from "vue";
import { message } from "ant-design-vue";

const props = defineProps<{
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
const iframeRef = ref<HTMLIFrameElement | null>(null);
const iframeLoaded = ref(false);
const exportPending = ref(false);
const exportTimer = ref<ReturnType<typeof setTimeout> | null>(null);

const MAX_FILE_SIZE = 5 * 1024 * 1024;
const turbowarpEmbedUrl = "https://turbowarp.org/editor?embed=true";

function onIframeLoad() {
  iframeLoaded.value = true;
}

function requestExport() {
  if (!iframeLoaded.value) {
    message.warning("编辑器还在加载，请稍等一下再试～");
    return;
  }

  exportPending.value = true;
  const iframe = iframeRef.value;
  if (iframe && iframe.contentWindow) {
    iframe.contentWindow.postMessage(
      { type: "tw-request-export" },
      "https://turbowarp.org",
    );
  }

  message.loading({ content: "正在获取作品…", key: "export", duration: 0 });

  exportTimer.value = setTimeout(() => {
    if (exportPending.value) {
      exportPending.value = false;
      message.destroy("export");
      message.warning(
        "自动获取需要新版编辑器支持。请手动导出：点编辑器左上角「文件」→「保存到电脑」，然后切到「上传作品」上传～",
        8,
      );
    }
  }, 5000);
}

function handlePostMessage(event: MessageEvent) {
  if (event.origin !== "https://turbowarp.org") return;
  const data = event.data;
  if (!data) return;

  let sb3Data: ArrayBuffer | string | null = null;

  if (
    (data.type === "tw-exported" || data.type === "sb3-export") &&
    data.sb3
  ) {
    sb3Data = data.sb3;
  }

  if (!sb3Data || !exportPending.value) return;

  exportPending.value = false;
  if (exportTimer.value) clearTimeout(exportTimer.value);
  message.destroy("export");

  let base64 = "";
  if (sb3Data instanceof ArrayBuffer) {
    const bytes = new Uint8Array(sb3Data);
    const chunkSize = 0x8000;
    let binary = "";
    for (let i = 0; i < bytes.length; i += chunkSize) {
      binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
    }
    base64 = btoa(binary);
  } else if (typeof sb3Data === "string") {
    base64 = sb3Data.includes(",") ? sb3Data.split(",")[1] : sb3Data;
  }

  if (base64) {
    sb3Base64.value = base64;
    fileName.value = "在线编辑作品.sb3";
    emit("update:sb3", base64);
    message.success("作品获取成功！点击「提交判题」按钮～");
  }
}

function switchToUpload() {
  mode.value = "upload";
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

onMounted(() => {
  window.addEventListener("message", handlePostMessage);
});

onUnmounted(() => {
  window.removeEventListener("message", handlePostMessage);
  if (exportTimer.value) clearTimeout(exportTimer.value);
});
</script>

<template>
  <div class="scratch-editor">
    <!-- 判题规则提示 -->
    <div v-if="props.checkCount" class="rules-hint">
      🔍 老师 say：这道题有 {{ props.checkCount }} 条检查规则，认真做好每一步哦～
    </div>

    <!-- 作品状态指示器 -->
    <div v-if="fileName" class="work-ready-banner">
      <span class="ready-icon">✅</span>
      <span class="ready-text">作品「{{ fileName }}」已准备好，点击下方「提交判题」按钮～</span>
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

    <!-- 在线编辑模式（默认） -->
    <div v-if="mode === 'editor'" class="editor-mode">
      <div class="iframe-wrap">
        <div v-if="!iframeLoaded" class="iframe-loading">
          <div class="loading-spinner">⏳</div>
          <div class="loading-text">Scratch 编辑器加载中…</div>
          <div class="loading-hint">第一次打开可能需要 10-20 秒，请耐心等待</div>
        </div>
        <iframe
          ref="iframeRef"
          :src="turbowarpEmbedUrl"
          class="turbowarp-iframe"
          allow="fullscreen; autoplay; microphone; camera"
          allowfullscreen
          @load="onIframeLoad"
        />
      </div>

      <button class="export-btn" :disabled="!iframeLoaded" @click="requestExport">
        📥 获取作品并提交
      </button>

      <div class="manual-tip">
        <div class="tip-title">💡 如果「获取作品」按钮没反应：</div>
        <div class="tip-steps">
          1. 在编辑器里点左上角「文件」→「保存到电脑」<br />
          2. 切到上方「📁 上传作品」<br />
          3. 选择刚才保存的 .sb3 文件
        </div>
        <button class="switch-upload-btn" @click="switchToUpload">
          切到上传作品 →
        </button>
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

.work-ready-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  border-radius: 12px;
}
.ready-icon {
  font-size: 18px;
}
.ready-text {
  font-size: 14px;
  color: #389e0d;
  font-weight: 600;
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

/* 在线编辑模式 */
.editor-mode {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.iframe-wrap {
  position: relative;
  border-radius: var(--radius-lg);
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
  color: #888;
  z-index: 1;
}
.loading-spinner {
  font-size: 48px;
  animation: spin 2s linear infinite;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.loading-text {
  font-size: 16px;
  color: #ccc;
}
.loading-hint {
  font-size: 13px;
  color: #666;
}

.export-btn {
  width: 100%;
  padding: 14px;
  border-radius: var(--radius-lg);
  border: none;
  background: linear-gradient(90deg, #ff7a45, #faad14);
  color: #fff;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.15s ease-out, box-shadow 0.2s ease-out;
}
.export-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 122, 69, 0.3);
}
.export-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.manual-tip {
  padding: 12px 14px;
  background: #fafafa;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.tip-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-sub);
}
.tip-steps {
  font-size: 13px;
  color: var(--color-text-sub);
  line-height: 1.8;
  padding-left: 4px;
}
.switch-upload-btn {
  align-self: flex-start;
  background: none;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-family: inherit;
  margin-top: 4px;
}
.switch-upload-btn:hover {
  background: #fff2e8;
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
