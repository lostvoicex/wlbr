<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { message, Modal } from "ant-design-vue";
import { useAuthStore } from "@/stores/auth";
import { useKpLabelsStore } from "@/stores/kpLabels";
import { useCopyTextsStore } from "@/stores/copyTexts";
import BrandLogo from "@/components/BrandLogo.vue";
import brand from "@/config/brand";
import {
  fetchStudentReminders,
  type StudentReminderItem,
} from "@/api/reminders";

const router = useRouter();
const auth = useAuthStore();
const kpLabels = useKpLabelsStore();
const copyTexts = useCopyTextsStore();

interface LevelCard {
  key: string;
  syllabus: string;
  gradeLevel: number;
  emoji: string;
  title: string;
  subtitle: string;
  tag: string;
  desc: string;
}

const levels: LevelCard[] = [
  // ---- Scratch ----
  { key: "scratch-l1", syllabus: "scratch-l1", gradeLevel: 1, emoji: "🧩", title: "Scratch 一级", subtitle: "认识软件，让小猫动起来", tag: "图形化入门", desc: "界面操作、角色背景、声音导入、逻辑推理" },
  { key: "scratch-l2", syllabus: "scratch-l2", gradeLevel: 2, emoji: "🚀", title: "Scratch 二级", subtitle: "分支循环，侦测运算", tag: "图形化进阶", desc: "多角色、画笔、选择循环、侦测、运算" },
  { key: "scratch-l3", syllabus: "scratch-l3", gradeLevel: 3, emoji: "🎯", title: "Scratch 三级", subtitle: "变量随机数、广播克隆", tag: "图形化进阶", desc: "变量、随机数、循环嵌套、广播、克隆" },
  { key: "scratch-l4", syllabus: "scratch-l4", gradeLevel: 4, emoji: "🏆", title: "Scratch 四级", subtitle: "链表函数、程序优化", tag: "图形化高阶", desc: "字符串、函数、链表、程序优化、递归" },
  // ---- Python ----
  { key: "python-l1", syllabus: "python-l1", gradeLevel: 1, emoji: "🐍", title: "Python 一级", subtitle: "认识 Python，Turtle 画图", tag: "Python 入门", desc: "开发环境、变量类型、输入输出、Turtle" },
  { key: "python-l2", syllabus: "python-l2", gradeLevel: 2, emoji: "📐", title: "Python 二级", subtitle: "分支循环、列表字符串", tag: "Python 入门", desc: "if/for/while、列表、字符串、调试" },
  { key: "python-l3", syllabus: "python-l3", gradeLevel: 3, emoji: "📊", title: "Python 三级", subtitle: "列表进阶、函数入门", tag: "Python 进阶", desc: "列表推导、元组、字符串处理、函数、Turtle" },
  { key: "python-l4", syllabus: "python-l4", gradeLevel: 4, emoji: "📚", title: "Python 四级", subtitle: "函数进阶、字典文件", tag: "Python 进阶", desc: "函数高阶、字典集合、文件读写、异常处理" },
  { key: "python-l5", syllabus: "python-l5", gradeLevel: 5, emoji: "🔧", title: "Python 五级", subtitle: "面向对象、标准库", tag: "Python 高阶", desc: "类与对象、继承多态、math/random/time" },
  { key: "python-l6", syllabus: "python-l6", gradeLevel: 6, emoji: "🤖", title: "Python 六级", subtitle: "算法、递归、数据结构", tag: "Python 高阶", desc: "算法基础、递归、排序查找、综合应用" },
  // ---- C++ ----
  { key: "cpp-l1", syllabus: "cpp-l1", gradeLevel: 1, emoji: "⚡", title: "C++ 一级", subtitle: "顺序结构、变量运算", tag: "C++ 入门", desc: "变量类型、cin/cout、算术关系运算" },
  { key: "cpp-l2", syllabus: "cpp-l2", gradeLevel: 2, emoji: "🔀", title: "C++ 二级", subtitle: "分支结构、逻辑运算", tag: "C++ 入门", desc: "if/else、switch、逻辑运算、char 字符串" },
  { key: "cpp-l3", syllabus: "cpp-l3", gradeLevel: 3, emoji: "🔁", title: "C++ 三级", subtitle: "循环语句、一维数组", tag: "C++ 进阶", desc: "for/while、break/continue、数组、循环嵌套" },
  { key: "cpp-l4", syllabus: "cpp-l4", gradeLevel: 4, emoji: "📦", title: "C++ 四级", subtitle: "二维数组、函数递归", tag: "C++ 进阶", desc: "多维数组、函数参数传递、递归、排序" },
  { key: "cpp-l5", syllabus: "cpp-l5", gradeLevel: 5, emoji: "📝", title: "C++ 五级", subtitle: "string 类、算法进阶", tag: "C++ 高阶", desc: "STL string、快排归并、二分查找、结构体" },
  { key: "cpp-l6", syllabus: "cpp-l6", gradeLevel: 6, emoji: "🏗️", title: "C++ 六级", subtitle: "数据结构、动态规划", tag: "C++ 高阶", desc: "栈、队列、链表、贪心、DP 入门" },
  { key: "cpp-l7", syllabus: "cpp-l7", gradeLevel: 7, emoji: "🌳", title: "C++ 七级", subtitle: "STL、二叉树、图论", tag: "C++ 竞赛", desc: "STL 容器、DFS/BFS、DP 进阶、图遍历" },
  { key: "cpp-l8", syllabus: "cpp-l8", gradeLevel: 8, emoji: "👑", title: "C++ 八级", subtitle: "算法综合、工程化", tag: "C++ 竞赛", desc: "面向对象、最短路、高级 DP、代码优化" },
];

const levelGroups = computed(() => {
  const groups: { label: string; items: LevelCard[] }[] = [];
  let cur: { label: string; items: LevelCard[] } | null = null;
  for (const lv of levels) {
    const prefix = lv.syllabus.split("-")[0];
    const langLabel = prefix === "scratch" ? "Scratch 图形化编程" : prefix === "python" ? "Python 编程" : "C++ 编程";
    if (!cur || cur.label !== langLabel) {
      cur = { label: langLabel, items: [] };
      groups.push(cur);
    }
    cur.items.push(lv);
  }
  return groups;
});

const selected = ref<string>("");

const remindersT1 = ref<StudentReminderItem[]>([]);
const remindersT2 = ref<StudentReminderItem[]>([]);
const remindersLoading = ref(false);

onMounted(async () => {
  kpLabels.loadOnce();
  copyTexts.loadOnce();
  await loadReminders();
});

async function loadReminders() {
  remindersLoading.value = true;
  try {
    const resp = await fetchStudentReminders();
    remindersT1.value = resp.t1_items || [];
    remindersT2.value = resp.t2_items || [];
  } catch {
    // 静默失败：拉不到就不显示提醒卡
    remindersT1.value = [];
    remindersT2.value = [];
  } finally {
    remindersLoading.value = false;
  }
}

const t1Cards = computed(() =>
  remindersT1.value.map((r) => {
    const kpName = kpLabels.getDisplay(r.kp_original);
    const rendered = copyTexts.renderReminderT1(kpName);
    return { ...r, kpName, title: rendered.title, body: rendered.body };
  }),
);
const t2Cards = computed(() =>
  remindersT2.value.map((r) => {
    const kpName = kpLabels.getDisplay(r.kp_original);
    const rendered = copyTexts.renderReminderT2(kpName);
    return { ...r, kpName, title: rendered.title, body: rendered.body };
  }),
);
const hasReminders = computed(
  () => t1Cards.value.length + t2Cards.value.length > 0,
);

function pick(key: string) {
  selected.value = key;
}

function start() {
  if (!selected.value) {
    message.info("先选一个闯关等级吧～");
    return;
  }
  const lv = levels.find((x) => x.key === selected.value)!;
  Modal.confirm({
    title: `准备好挑战「${lv.title}」了吗？`,
    content: "答题过程可以随时暂停，别紧张哦～",
    okText: "开始！",
    cancelText: "再看看",
    onOk() {
      router.push(`/student/diagnosis/${lv.syllabus}`);
    },
  });
}

function retestNow(syllabus: string, type: string) {
  const typeLabel = type === "retest_t2" ? "复测二" : "复测一";
  message.success(`准备好${typeLabel}了吗？加油！`);
  router.push(`/student/diagnosis/${syllabus}?type=${type}`);
}

function logout() {
  auth.clear();
  router.replace("/student/login");
}
</script>

<template>
  <div class="kid-app">
    <header class="kid-header">
      <div class="brand">
        <BrandLogo which="student" :size="32" />
        <span>{{ brand.platformNameStudent }}</span>
      </div>
      <div class="header-actions">
        <a-button type="link" @click="router.push('/student/history')">我的记录</a-button>
        <a-button type="link" @click="logout">退出</a-button>
      </div>
    </header>

    <main class="page">
      <section class="hero kid-card">
        <div class="hero-emoji">🌟</div>
        <div>
          <h1 class="kid-title">今天想挑战哪一关？</h1>
          <p class="kid-subtitle">
            选一个等级，开始 27 道闯关题（15 选择 + 10 判断 + 2 编程），找出你还没完全掌握的知识点！
          </p>
        </div>
      </section>

      <!-- 复测到期提醒卡（T1/T2） -->
      <section v-if="hasReminders" class="reminders">
        <div class="reminders-head">
          <span class="reminders-emoji">📮</span>
          <span class="reminders-title">小猫给你的小任务</span>
        </div>

        <div
          v-for="(r, idx) in t1Cards"
          :key="'t1-' + idx + '-' + r.kp_original"
          class="reminder-card t1"
        >
          <div class="reminder-head-row">
            <span class="reminder-tag tag-t1">T1 · 3 天</span>
            <span class="reminder-title">{{ r.title }}</span>
          </div>
          <div class="reminder-body">{{ r.body }}</div>
          <div class="reminder-foot">
            <span class="reminder-days">{{ r.days_ago }} 天前的记录</span>
            <button class="reminder-cta" @click="retestNow(r.syllabus_target, 'retest_t1')">现在就试试 →</button>
          </div>
        </div>

        <div
          v-for="(r, idx) in t2Cards"
          :key="'t2-' + idx + '-' + r.kp_original"
          class="reminder-card t2"
        >
          <div class="reminder-head-row">
            <span class="reminder-tag tag-t2">T2 · 7 天</span>
            <span class="reminder-title">{{ r.title }}</span>
          </div>
          <div class="reminder-body">{{ r.body }}</div>
          <div class="reminder-foot">
            <span class="reminder-days">{{ r.days_ago }} 天前的记录</span>
            <button class="reminder-cta" @click="retestNow(r.syllabus_target, 'retest_t2')">现在就试试 →</button>
          </div>
        </div>
      </section>

      <section
        v-for="group in levelGroups"
        :key="group.label"
        class="level-section"
      >
        <h2 class="group-title">{{ group.label }}</h2>
        <div class="level-grid">
          <div
            v-for="lv in group.items"
            :key="lv.key"
            class="level-card kid-card"
            :class="{ selected: selected === lv.key }"
            @click="pick(lv.key)"
          >
            <div class="level-emoji">{{ lv.emoji }}</div>
            <div class="level-title">{{ lv.title }}</div>
            <div class="level-sub">{{ lv.subtitle }}</div>
            <div class="level-tag">{{ lv.tag }}</div>
            <div class="level-desc">{{ lv.desc }}</div>
            <div class="check-dot" v-if="selected === lv.key">✓</div>
          </div>
        </div>
      </section>

      <div class="action">
        <a-button type="primary" size="large" :disabled="!selected" @click="start">
          开始闯关！
        </a-button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.kid-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 10;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: var(--color-text);
}
.logo-mini {
  display: none;
}
.page {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px 16px 48px;
}
.hero {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}
.hero-emoji {
  font-size: 48px;
  flex-shrink: 0;
}
.level-section {
  margin-bottom: 24px;
}
.group-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 12px;
  padding-left: 4px;
}
.level-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}
.level-card {
  cursor: pointer;
  transition: transform 200ms var(--ease-bounce),
    box-shadow 200ms ease-out, border-color 200ms ease-out;
  border: 2px solid transparent;
  position: relative;
}
.level-card:hover {
  transform: translateY(-4px);
}
.level-card.selected {
  border-color: var(--color-primary);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 10px 28px rgba(255, 122, 69, 0.22);
}
.level-emoji {
  font-size: 36px;
  margin-bottom: 8px;
}
.level-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
}
.level-sub {
  color: var(--color-text-sub);
  margin-bottom: 12px;
  font-size: 14px;
}
.level-tag {
  display: inline-block;
  background: #fff5eb;
  color: var(--color-primary);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
}
.level-desc {
  color: var(--color-text-sub);
  font-size: 13px;
}
.check-dot {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(255, 122, 69, 0.32);
  animation: pop 240ms var(--ease-bounce);
}
@keyframes pop {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}
.action {
  text-align: center;
}
.action .ant-btn {
  min-width: 220px;
}

/* ---------- 复测提醒卡 ---------- */
.reminders {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.reminders-head {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 4px;
}
.reminders-emoji {
  font-size: 22px;
}
.reminder-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 14px 16px 12px;
  border-left: 4px solid var(--color-secondary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.reminder-card.t1 {
  border-left-color: #faad14;
  background: #fffbe6;
}
.reminder-card.t2 {
  border-left-color: #ff7a45;
  background: #fff2e8;
}
.reminder-head-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.reminder-tag {
  font-size: 12px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  color: #fff;
}
.tag-t1 {
  background: #faad14;
}
.tag-t2 {
  background: #ff7a45;
}
.reminder-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text);
}
.reminder-body {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text);
  margin: 4px 0 8px;
}
.reminder-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.reminder-days {
  font-size: 12px;
  color: var(--color-text-sub);
}
.reminder-cta {
  background: none;
  border: none;
  color: var(--color-primary);
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  padding: 4px 6px;
  border-radius: 8px;
}
.reminder-cta:hover {
  background: rgba(255, 122, 69, 0.08);
}
</style>
