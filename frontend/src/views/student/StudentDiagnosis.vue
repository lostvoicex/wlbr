<script setup lang="ts">
import { ref, computed, onBeforeUnmount, onMounted, defineAsyncComponent } from "vue";
import { useRoute, useRouter, onBeforeRouteLeave } from "vue-router";
import { Modal, message } from "ant-design-vue";
import {
  startSession,
  submitAnswer,
  finishSession,
  reportTabSwitch,
  type QuestionForStudent,
} from "@/api/diagnosis";
import { submitCode, type OjSubmitResponse } from "@/api/oj";
import { useKpLabelsStore } from "@/stores/kpLabels";
import BrandLogo from "@/components/BrandLogo.vue";
import brand from "@/config/brand";

// 异步加载大型编辑器组件，减少主 chunk 体积
const ScratchEditor = defineAsyncComponent(() => import("@/components/ScratchEditor.vue"));
const CodeEditor = defineAsyncComponent(() => import("@/components/CodeEditor.vue"));

const route = useRoute();
const router = useRouter();
const kpStore = useKpLabelsStore();

const syllabus = String(route.params.syllabus_target || "scratch-l1");
const sessionType = String(route.query.type || "diagnosis");
const SYLLABIS_LABELS: Record<string, string> = {
  "scratch-l1": "Scratch 一级", "scratch-l2": "Scratch 二级", "scratch-l3": "Scratch 三级", "scratch-l4": "Scratch 四级",
  "python-l1": "Python 一级", "python-l2": "Python 二级", "python-l3": "Python 三级",
  "python-l4": "Python 四级", "python-l5": "Python 五级", "python-l6": "Python 六级",
  "cpp-l1": "C++ 一级", "cpp-l2": "C++ 二级", "cpp-l3": "C++ 三级",
  "cpp-l4": "C++ 四级", "cpp-l5": "C++ 五级", "cpp-l6": "C++ 六级",
  "cpp-l7": "C++ 七级", "cpp-l8": "C++ 八级",
};
const syllabusLabel = SYLLABIS_LABELS[syllabus] || syllabus;
const typeLabel =
  sessionType === "retest_t1"
    ? "复测一"
    : sessionType === "retest_t2"
      ? "复测二"
      : "诊断闯关";

const loading = ref(true);
const submitting = ref(false);
const sessionId = ref<number | null>(null);
const questions = ref<QuestionForStudent[]>([]);
const total = computed(() => questions.value.length);
const current = ref(0);

// 每题的选中答案缓存
const answers = ref<Record<number, string>>({});
// 编程题（积木排序）的暂存：questionId -> 已选积木顺序数组
const codingPicks = ref<Record<number, string[]>>({});
// 编程大题（program）的代码/sb3 暂存：questionId -> 内容
const programCode = ref<Record<number, string>>({});
// 编程大题的判题结果：questionId -> 最新结果
const programResults = ref<Record<number, OjSubmitResponse | null>>({});
// 判题中
const judging = ref(false);
// 是否允许无提示离开（完成后离开时不弹拦截）
const finishedGuard = ref(false);

// 反作弊：每题开始作答时间戳（毫秒）
const questionStartTime = ref<number>(0);
// 反作弊：切走时的时间戳
let hideAt = 0;
// 反作弊：切屏次数（本地显示用）
const tabSwitchCount = ref(0);
// 反作弊：切屏警告是否显示
const tabSwitchWarning = ref(false);

const currentQ = computed<QuestionForStudent | undefined>(
  () => questions.value[current.value],
);

const answered = computed(() => {
  const q = currentQ.value;
  if (!q) return false;
  if (q.q_type === "program") {
    // 编程大题：已提交过判题即可
    return !!programResults.value[q.id];
  }
  const a = answers.value[q.id];
  if (q.q_type === "coding") {
    const picks = codingPicks.value[q.id] || [];
    return picks.length > 0;
  }
  return !!a;
});

const isLast = computed(() => current.value === total.value - 1);

// ---------- 单选题选项解析 ----------
function parseSingleOptions(content: string): { text: string; letter: string }[] {
  // 支持 "A.xxx B.yyy C.zzz" 或 换行
  const re = /([A-D])[\.．、]\s*([^A-D\n]+)/g;
  const list: { text: string; letter: string }[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(content)) !== null) {
    list.push({ letter: m[1], text: m[2].trim() });
  }
  return list;
}

function questionStem(content: string): string {
  const idx = content.search(/[A-D][\.．、]/);
  if (idx > 0) return content.slice(0, idx).trim();
  return content.trim();
}

// ---------- 编程题（积木排序）候选块 ----------
// 老数据兜底：从 content 里提取 "候选块：块1 / 块2 / 块3"
function parseCodingBlocksFromContent(content: string): string[] {
  const m = content.match(/候选[块积木]*[:：]\s*([^\n]+)/);
  if (m) {
    return m[1]
      .split(/[\/／,，、]/)
      .map((x) => x.trim())
      .filter(Boolean);
  }
  return [];
}

// 取当前题的候选积木：优先用后端返回的 blocks 字段；否则从 content 解析
function candidateBlocks(q: QuestionForStudent | undefined): string[] {
  if (!q) return [];
  if (q.blocks && q.blocks.length) return q.blocks;
  return parseCodingBlocksFromContent(q.content);
}

// Fisher-Yates 洗牌；按 q.id 缓存，切进切出不重洗，换题才洗一次
const shuffledCache = new Map<number, string[]>();
function shuffledBlocks(q: QuestionForStudent | undefined): string[] {
  if (!q) return [];
  const cached = shuffledCache.get(q.id);
  if (cached) return cached;
  const src = candidateBlocks(q);
  const arr = src.slice();
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  shuffledCache.set(q.id, arr);
  return arr;
}

// ---------- 数据加载 ----------
onMounted(async () => {
  try {
    const res = await startSession({
      syllabus_target: syllabus,
      count: 27,
      session_type: sessionType,
    });
    sessionId.value = res.session_id;
    questions.value = res.questions;
    questionStartTime.value = Date.now();
    if (!res.questions.length) {
      message.warning("这个等级还没有题目哦，先联系老师～");
    }
    // 监听页面可见性变化（反作弊：切屏检测）
    document.addEventListener("visibilitychange", handleVisibilityChange);
  } catch (e) {
    message.error("加载题目失败，先回主页试试吧～");
    router.replace("/student/home");
  } finally {
    loading.value = false;
  }
});

// ---------- 反作弊：切屏检测 ----------
function handleVisibilityChange() {
  if (!sessionId.value || finishedGuard.value) return;
  if (document.hidden) {
    hideAt = Date.now();
    // 上报切走事件
    reportTabSwitch(sessionId.value, {
      event_type: "hide",
      page_info: document.title,
    }).catch(() => {
      // 静默失败，不影响答题
    });
  } else {
    const awayMs = hideAt ? Date.now() - hideAt : 0;
    const awaySec = Math.round(awayMs / 1000);
    hideAt = 0;
    tabSwitchCount.value += 1;
    // 上报切回事件
    reportTabSwitch(sessionId.value, {
      event_type: "show",
      away_duration_sec: awaySec,
      page_info: document.title,
    }).catch(() => {});
    // 切屏超过 3 次弹提醒
    if (tabSwitchCount.value >= 3) {
      tabSwitchWarning.value = true;
      setTimeout(() => {
        tabSwitchWarning.value = false;
      }, 3000);
    }
  }
}

// ---------- 交互 ----------
function pickOption(letter: string) {
  const q = currentQ.value;
  if (!q) return;
  answers.value[q.id] = letter;
}

function pickJudge(v: "T" | "F") {
  const q = currentQ.value;
  if (!q) return;
  answers.value[q.id] = v;
}

function pickBlock(block: string) {
  const q = currentQ.value;
  if (!q) return;
  const list = codingPicks.value[q.id] ? [...codingPicks.value[q.id]] : [];
  list.push(block);
  codingPicks.value[q.id] = list;
  answers.value[q.id] = list.join("→");
}

function undoBlock() {
  const q = currentQ.value;
  if (!q) return;
  const list = codingPicks.value[q.id] ? [...codingPicks.value[q.id]] : [];
  list.pop();
  codingPicks.value[q.id] = list;
  answers.value[q.id] = list.join("→");
}

async function commitCurrent(): Promise<boolean> {
  const q = currentQ.value;
  if (!q || !sessionId.value) return false;
  // 编程大题：判题时已通过 OJ submit 写入 LearningRecord，这里直接放行
  if (q.q_type === "program") {
    if (!programResults.value[q.id]) {
      message.info('先点「提交判题」看看成绩吧～');
      return false;
    }
    return true;
  }
  const ans = answers.value[q.id];
  if (!ans) {
    message.info("先选一个答案吧～");
    return false;
  }
  // 计算答题耗时（秒）
  const answerDurationSec = Math.round((Date.now() - questionStartTime.value) / 1000);
  try {
    submitting.value = true;
    await submitAnswer(sessionId.value, {
      question_id: q.id,
      student_answer: ans,
      answer_duration_sec: answerDurationSec,
    });
    return true;
  } catch {
    message.error("提交没成功，再试一次～");
    return false;
  } finally {
    submitting.value = false;
  }
}

// ---------- 编程大题判题 ----------
async function submitProgram() {
  const q = currentQ.value;
  if (!q || !sessionId.value || q.q_type !== "program") return;
  const code = programCode.value[q.id];
  if (!code || !code.trim()) {
    message.info("先写好代码或上传作品再提交哦～");
    return;
  }
  const lang = q.program_lang || "python";
  try {
    judging.value = true;
    const result = await submitCode({
      question_id: q.id,
      session_id: sessionId.value,
      language: lang,
      code: code,
    });
    programResults.value[q.id] = result;
    // 记录答案摘要（供答题进度展示）
    answers.value[q.id] = `[OJ] score=${result.score}`;
    // 提示
    if (result.verdict === "accepted") {
      message.success(`太棒了！满分通过 🎉 得分 ${result.score}`);
    } else if (result.score >= 60) {
      message.success(`不错哦！得分 ${result.score}，再优化一下更好～`);
    } else {
      message.warning(`得分 ${result.score}，继续加油！可以再试一次～`);
    }
  } catch (e) {
    message.error("判题没成功，再试一次～");
  } finally {
    judging.value = false;
  }
}

function updateProgramCode(val: string) {
  const q = currentQ.value;
  if (!q) return;
  programCode.value[q.id] = val;
}

// 从脱敏后的判题规则里取展示字段（模板里不能写 `as` 断言，统一走这里）
function gradingField(field: "check_count" | "test_case_count" | "time_limit", fallback: number): number {
  const q = currentQ.value;
  if (!q || !q.grading_rules_parsed) return fallback;
  const rules = q.grading_rules_parsed as Record<string, unknown>;
  const v = rules[field];
  return typeof v === "number" ? v : fallback;
}

// verdict 对应的中文标签和颜色
const verdictMap: Record<string, { label: string; color: string }> = {
  accepted: { label: "✅ 完全通过", color: "#52c41a" },
  partial: { label: "🔶 部分通过", color: "#faad14" },
  wrong_answer: { label: "❌ 答案不对", color: "#ff4d4f" },
  compile_error: { label: "🛑 编译失败", color: "#ff4d4f" },
  runtime_error: { label: "💥 运行出错", color: "#ff4d4f" },
  time_limit: { label: "⏰ 超时了", color: "#ff4d4f" },
};

async function next() {
  const ok = await commitCurrent();
  if (!ok) return;
  if (current.value < total.value - 1) {
    current.value += 1;
    questionStartTime.value = Date.now();
  }
}

function prev() {
  if (current.value > 0) {
    current.value -= 1;
    questionStartTime.value = Date.now();
  }
}

async function finish() {
  const ok = await commitCurrent();
  if (!ok) return;
  if (!sessionId.value) return;
  try {
    submitting.value = true;
    const res = await finishSession(sessionId.value);
    finishedGuard.value = true;
    message.success("答完啦！去看看你的成绩吧 🎉");
    router.replace(`/student/result/${res.session_id}`);
  } catch {
    message.error("交卷没成功，再点一次～");
  } finally {
    submitting.value = false;
  }
}

// ---------- 退出拦截 ----------
function beforeUnloadHandler(e: BeforeUnloadEvent) {
  if (finishedGuard.value) return;
  e.preventDefault();
  e.returnValue = "";
}
onMounted(() => window.addEventListener("beforeunload", beforeUnloadHandler));
onBeforeUnmount(() => {
  window.removeEventListener("beforeunload", beforeUnloadHandler);
  document.removeEventListener("visibilitychange", handleVisibilityChange);
});

onBeforeRouteLeave((_to, _from, nextFn) => {
  if (finishedGuard.value) return nextFn();
  Modal.confirm({
    title: "现在退出的话，答题就要重新来一遍哦",
    content: "确定要离开吗？",
    okText: "先离开",
    cancelText: "再答一会儿",
    okButtonProps: { danger: true },
    onOk() {
      nextFn();
    },
    onCancel() {
      nextFn(false);
    },
  });
});
</script>

<template>
  <div class="kid-app diag-app">
    <header class="diag-header">
      <div class="brand">
        <BrandLogo which="student" :size="32" />
        <span class="brand-title">{{ brand.platformNameStudent }}</span>
        <span class="brand-sub">· {{ syllabusLabel }} · {{ typeLabel }}</span>
      </div>
      <div class="progress-wrap" v-if="total > 0">
        <div class="progress-txt">
          第 <b>{{ current + 1 }}</b> / {{ total }} 题
        </div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: `${((current + 1) / total) * 100}%` }"
          />
        </div>
      </div>
    </header>

    <!-- 切屏警告 -->
    <transition name="fade">
      <div v-if="tabSwitchWarning" class="tab-switch-warning">
        ⚠️ 答题时请不要切换页面哦，认真答题才能测出真实水平～
      </div>
    </transition>

    <main class="diag-main">
      <div v-if="loading" class="loading-box">🐣 题目正在飞来，稍等一下…</div>

      <div v-else-if="!currentQ" class="loading-box">还没有题目呢～</div>

      <div v-else class="q-card">
        <div class="q-tag">
          <span class="q-kp" :title="kpStore.getDescription(currentQ.knowledge_point)">🧠 {{ kpStore.getDisplay(currentQ.knowledge_point) }}</span>
          <span class="q-type">{{
            currentQ.q_type === "single"
              ? "选一个"
              : currentQ.q_type === "judge"
              ? "对还是错"
              : currentQ.q_type === "coding"
              ? "拼积木"
              : "编程大题"
          }}</span>
        </div>
        <div class="q-stem">{{ questionStem(currentQ.content) }}</div>

        <!-- 单选 -->
        <div v-if="currentQ.q_type === 'single'" class="options options-single">
          <button
            v-for="opt in parseSingleOptions(currentQ.content)"
            :key="opt.letter"
            :class="[
              'opt-card',
              { picked: answers[currentQ.id] === opt.letter },
            ]"
            @click="pickOption(opt.letter)"
          >
            <span class="opt-letter">{{ opt.letter }}</span>
            <span class="opt-text">{{ opt.text }}</span>
          </button>
        </div>

        <!-- 判断 -->
        <div v-else-if="currentQ.q_type === 'judge'" class="options options-judge">
          <button
            :class="['judge-btn', 'jt', { picked: answers[currentQ.id] === 'T' }]"
            @click="pickJudge('T')"
          >
            ✅ 正确
          </button>
          <button
            :class="['judge-btn', 'jf', { picked: answers[currentQ.id] === 'F' }]"
            @click="pickJudge('F')"
          >
            ❌ 错误
          </button>
        </div>

        <!-- 编程题：积木排序 -->
        <div v-else-if="currentQ.q_type === 'coding'" class="coding-wrap">
          <div class="coding-tips">
            💡 从下面的候选积木里，按顺序点一点，拼出正确的顺序哦～
          </div>
          <div class="coding-picked">
            <div class="picked-title">你的拼装：</div>
            <div class="picked-blocks">
              <template v-if="(codingPicks[currentQ.id] || []).length">
                <span
                  v-for="(b, i) in codingPicks[currentQ.id]"
                  :key="i"
                  class="block picked-block"
                >
                  {{ i + 1 }}. {{ b }}
                </span>
              </template>
              <span v-else class="picked-empty">还没拼哦 👀</span>
            </div>
            <button
              class="undo-btn"
              :disabled="!(codingPicks[currentQ.id] || []).length"
              @click="undoBlock"
            >
              撤回上一步
            </button>
          </div>
          <div class="coding-choices">
            <div class="picked-title">候选积木：</div>
            <div class="choice-blocks">
              <button
                v-for="b in shuffledBlocks(currentQ)"
                :key="b"
                :disabled="(codingPicks[currentQ.id] || []).includes(b)"
                class="block choice-block"
                @click="pickBlock(b)"
              >
                🧩 {{ b }}
              </button>
            </div>
          </div>
        </div>

        <!-- 编程大题（program） -->
        <div v-else class="program-wrap">
          <div class="program-tips">
            💻 这是一道编程大题！做好后点"提交判题"，
            系统会自动帮你打分哦～可以多次提交取最高分。
          </div>

          <!-- Scratch 编辑器 -->
          <ScratchEditor
            v-if="currentQ.program_lang === 'scratch'"
            :check-count="gradingField('check_count', 0)"
            @update:sb3="updateProgramCode"
          />

          <!-- Python / C++ 代码编辑器 -->
          <CodeEditor
            v-else
            :model-value="programCode[currentQ.id] || ''"
            :language="currentQ.program_lang || 'python'"
            :test-case-count="gradingField('test_case_count', 0)"
            :time-limit="gradingField('time_limit', 2)"
            @update:model-value="updateProgramCode"
          />

          <!-- 提交判题按钮 -->
          <div class="program-actions">
            <button
              class="judge-btn"
              :disabled="judging || !programCode[currentQ.id]"
              @click="submitProgram"
            >
              {{ judging ? "🔮 判题中…" : "🚀 提交判题" }}
            </button>
          </div>

          <!-- 判题结果 -->
          <div
            v-if="programResults[currentQ.id]"
            class="judge-result"
          >
            <div class="result-header">
              <span class="result-verdict">
                {{ verdictMap[programResults[currentQ.id]!.verdict]?.label || programResults[currentQ.id]!.verdict }}
              </span>
              <span
                class="result-score"
                :style="{
                  color: programResults[currentQ.id]!.score >= 60 ? '#52c41a' : '#ff4d4f'
                }"
              >
                {{ programResults[currentQ.id]!.score }} 分
              </span>
            </div>
            <div class="result-stats">
              通过 {{ programResults[currentQ.id]!.passed_cases }} /
              {{ programResults[currentQ.id]!.total_cases }} 项检查
              <span v-if="programResults[currentQ.id]!.judge_duration_ms">
                · 耗时 {{ programResults[currentQ.id]!.judge_duration_ms }}ms
              </span>
            </div>

            <!-- 详细反馈（Scratch 规则 / 测试用例） -->
            <div
              v-if="Array.isArray(programResults[currentQ.id]!.details)"
              class="result-details"
            >
              <div class="details-title">📋 详细检查结果：</div>
              <div
                v-for="(d, i) in (programResults[currentQ.id]!.details as Array<{passed?: boolean; desc?: string; msg?: string; rule?: string}>)"
                :key="i"
                :class="['detail-item', d.passed ? 'pass' : 'fail']"
              >
                <span class="detail-icon">{{ d.passed ? "✅" : "❌" }}</span>
                <span class="detail-text">
                  <span v-if="d.desc" class="detail-desc">{{ d.desc }}</span>
                  <span class="detail-msg">{{ d.msg || d.rule }}</span>
                </span>
              </div>
            </div>

            <!-- 错误信息 -->
            <div v-if="programResults[currentQ.id]!.stderr" class="result-stderr">
              <div class="stderr-title">⚠️ 错误信息：</div>
              <pre class="stderr-content">{{ programResults[currentQ.id]!.stderr }}</pre>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="diag-footer" v-if="!loading && currentQ">
      <button
        class="foot-btn secondary"
        :disabled="current === 0 || submitting"
        @click="prev"
      >
        ⬅️ 上一题
      </button>
      <button
        v-if="!isLast"
        class="foot-btn primary"
        :disabled="!answered || submitting"
        @click="next"
      >
        下一题 ➡️
      </button>
      <button
        v-else
        class="foot-btn finish"
        :disabled="!answered || submitting"
        @click="finish"
      >
        完成答题 🎉
      </button>
    </footer>
  </div>
</template>

<style scoped>
.diag-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.diag-header {
  padding: 16px 20px 12px;
  background: #fff;
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(255, 122, 69, 0.06);
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 16px;
  color: var(--color-text);
  flex-wrap: wrap;
}
.brand-title {
  font-weight: 700;
}
.brand-sub {
  color: var(--color-text-sub);
  font-weight: 500;
  font-size: 14px;
}
.logo-mini {
  display: none;
}
.progress-wrap {
  margin-top: 12px;
}
.progress-txt {
  font-size: 15px;
  color: var(--color-text-sub);
  margin-bottom: 6px;
}
.progress-txt b {
  color: var(--color-primary);
  font-size: 18px;
}
.progress-bar {
  height: 12px;
  border-radius: 8px;
  background: #ffe7d6;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 8px;
  background: linear-gradient(90deg, #ffb890, #ff7a45);
  transition: width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.diag-main {
  flex: 1;
  padding: 20px 16px 96px;
  max-width: 640px;
  width: 100%;
  margin: 0 auto;
}
.loading-box {
  padding: 60px 12px;
  text-align: center;
  font-size: 18px;
  color: var(--color-text-sub);
}
.q-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 20px 20px 24px;
  border-left: 4px solid var(--color-primary);
  box-shadow: 0 6px 20px rgba(255, 122, 69, 0.1);
  animation: pop 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes pop {
  from {
    transform: translateY(8px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.q-tag {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.q-kp {
  background: #fff2e8;
  color: #d4380d;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}
.q-type {
  background: #e6f4ff;
  color: #1677ff;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}
.q-stem {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.5;
  color: var(--color-text);
  margin-bottom: 20px;
}

.options-single {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.opt-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: #fffbf7;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: transform 0.15s ease-out, border-color 0.2s ease-out,
    box-shadow 0.2s ease-out;
  text-align: left;
  font-family: inherit;
}
.opt-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 122, 69, 0.12);
}
.opt-card.picked {
  border-color: var(--color-primary);
  background: #fff2e8;
  transform: scale(1.02);
  box-shadow: 0 6px 20px rgba(255, 122, 69, 0.2);
}
.opt-letter {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: var(--color-primary);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 18px;
  flex-shrink: 0;
}
.opt-text {
  font-size: 17px;
  color: var(--color-text);
  line-height: 1.5;
}

.options-judge {
  display: flex;
  gap: 12px;
}
.judge-btn {
  flex: 1;
  padding: 22px 12px;
  border-radius: var(--radius-lg);
  border: 3px solid var(--color-border);
  background: #fffbf7;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.15s ease-out, border-color 0.2s ease-out;
  font-family: inherit;
}
.judge-btn.jt.picked {
  border-color: var(--color-pass);
  background: #f6ffed;
  transform: scale(1.04);
}
.judge-btn.jf.picked {
  border-color: var(--color-weak);
  background: #fff1f0;
  transform: scale(1.04);
}
.judge-btn:hover {
  transform: translateY(-2px);
}

.coding-wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.coding-tips {
  background: #fff9db;
  padding: 10px 14px;
  border-radius: 12px;
  color: #664c00;
  font-size: 15px;
}
.picked-title {
  font-size: 14px;
  color: var(--color-text-sub);
  margin-bottom: 6px;
}
.picked-blocks {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-height: 44px;
  padding: 10px;
  background: #fffbf7;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  align-items: center;
}
.picked-empty {
  color: #b6b0a8;
}
.block {
  padding: 8px 14px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}
.picked-block {
  background: #ffd8a8;
  color: #7a3a00;
}
.choice-block {
  background: #ffe7d6;
  color: #7a3a00;
  transition: transform 0.15s ease-out;
}
.choice-block:hover {
  transform: translateY(-2px);
  background: #ffd8a8;
}
.choice-blocks {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.undo-btn {
  margin-top: 8px;
  background: none;
  border: none;
  color: var(--color-secondary);
  cursor: pointer;
  font-size: 14px;
  font-family: inherit;
}
.undo-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.diag-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px 16px;
  background: rgba(255, 249, 242, 0.96);
  backdrop-filter: blur(8px);
  border-top: 1px solid var(--color-border);
  display: flex;
  gap: 10px;
  max-width: 640px;
  margin: 0 auto;
}
.foot-btn {
  flex: 1;
  min-height: 52px;
  border-radius: var(--radius-lg);
  border: none;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.12s ease-out, box-shadow 0.2s ease-out;
  font-family: inherit;
}
.foot-btn.secondary {
  background: #fff;
  color: var(--color-text);
  border: 2px solid var(--color-border);
}
.foot-btn.primary {
  background: var(--color-primary);
  color: #fff;
}
.foot-btn.finish {
  background: linear-gradient(90deg, #ffb890, #ff7a45);
  color: #fff;
}
.foot-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 122, 69, 0.2);
}
.foot-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* 编程大题 */
.program-wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.program-tips {
  background: #f0f5ff;
  padding: 10px 14px;
  border-radius: 12px;
  color: #1677ff;
  font-size: 15px;
}
.program-actions {
  display: flex;
  justify-content: center;
}
.judge-btn {
  padding: 14px 36px;
  border-radius: var(--radius-lg);
  border: none;
  background: linear-gradient(90deg, #1677ff, #4096ff);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.15s ease-out, box-shadow 0.2s ease-out;
}
.judge-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(22, 119, 255, 0.3);
}
.judge-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* 判题结果 */
.judge-result {
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  background: #fafafa;
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.result-verdict {
  font-size: 18px;
  font-weight: 700;
}
.result-score {
  font-size: 24px;
  font-weight: 800;
}
.result-stats {
  font-size: 14px;
  color: var(--color-text-sub);
  margin-bottom: 12px;
}
.result-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.details-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}
.detail-item {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 14px;
}
.detail-item.pass {
  background: #f6ffed;
}
.detail-item.fail {
  background: #fff1f0;
}
.detail-icon {
  flex-shrink: 0;
}
.detail-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.detail-desc {
  font-weight: 600;
}
.detail-msg {
  color: var(--color-text-sub);
  font-size: 13px;
}
.result-stderr {
  margin-top: 8px;
  padding: 10px;
  background: #2d2d2d;
  border-radius: 8px;
}
.stderr-title {
  color: #ff7875;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}
.stderr-content {
  color: #d4d4d4;
  font-family: "Courier New", Consolas, monospace;
  font-size: 13px;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}

/* 切屏警告 */
.tab-switch-warning {
  position: fixed;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff2e8;
  color: #d4380d;
  padding: 10px 20px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(255, 122, 69, 0.2);
  z-index: 100;
  border: 1px solid #ffbb96;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -10px);
}
</style>
