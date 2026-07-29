import { defineStore } from "pinia";
import { ref } from "vue";
import {
  fetchCopyTexts,
  type BadgeCopy,
  type CopyTextsResponse,
  type ReminderCopy,
  type TeacherAlertsCopy,
} from "@/api/copyTexts";

/**
 * 展示文案 store：徽章 / 复测提醒 / 老师催办的话术
 *
 * - 前端启动时 loadOnce() 拉一次并缓存
 * - 拉取失败时使用内置兜底文案，不 crash
 * - 所有含 KP 名的模板变量，页面渲染前需先用 kpLabels.getDisplay() 转成童趣名
 */

// 兜底文案：接口失败时使用，保证 UI 不空
const FALLBACK: CopyTextsResponse = {
  badges: {
    champion: {
      tier: "champion",
      emoji: "🏆",
      title: "小小编程家",
      subtitle: "哇塞！这个知识点你已经玩得飞起～",
    },
    cheer: {
      tier: "cheer",
      emoji: "💪",
      title: "加油小勇士",
      subtitle: "就差一点点就掌握啦！",
    },
    together: {
      tier: "together",
      emoji: "🌟",
      title: "一起来突破",
      subtitle: "别怕～老师和小猫都在这里陪你！",
    },
  },
  low_confidence_suffix: "（这个结果只做参考，题目太少啦～）",
  reminders: {
    t1: {
      type: "t1",
      days: 3,
      target_level: "need_review",
      title: "小猫在等你复习～",
      body_template:
        "上次学的【{kp_display_name}】你还记得吗？3 天没见啦，来做几道题给小猫看看吧！",
    },
    t2: {
      type: "t2",
      days: 7,
      target_level: "need_repair",
      title: "这次一定拿下～",
      body_template:
        "【{kp_display_name}】上次差一点点，休息 7 天了，现在再来试试，肯定不一样！",
    },
  },
  teacher_alerts: {
    template:
      "{student_name} 的【{kp_display_name}】{retest_type} 复测到期（{days_ago} 天前 {mastery_status}），建议今天推一次复测题",
    empty_hint: "暂无待催办的复测，学员们都还在稳步学习中～",
    status_labels: {
      need_review: "待巩固",
      need_repair: "需加练",
    },
    retest_type_labels: {
      t1: "T1",
      t2: "T2",
    },
  },
};

function render(template: string, vars: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (_, k: string) => {
    const v = vars[k];
    if (v === undefined || v === null || v === "") {
      // 兜底占位，避免露出 {var} 未替换的原文
      if (k === "student_name") return "这位小朋友";
      if (k === "kp_display_name") return "这个知识点";
      return "";
    }
    return String(v);
  });
}

export const useCopyTextsStore = defineStore("copyTexts", () => {
  const data = ref<CopyTextsResponse>(FALLBACK);
  const loaded = ref(false);
  const loading = ref(false);

  async function loadOnce(): Promise<void> {
    if (loaded.value || loading.value) return;
    loading.value = true;
    try {
      const resp = await fetchCopyTexts();
      // 后端字段齐全时全量替换；缺哪补哪，避免 undefined
      data.value = {
        badges: resp.badges || FALLBACK.badges,
        low_confidence_suffix:
          resp.low_confidence_suffix || FALLBACK.low_confidence_suffix,
        reminders: {
          t1: (resp.reminders && resp.reminders.t1) || FALLBACK.reminders.t1,
          t2: (resp.reminders && resp.reminders.t2) || FALLBACK.reminders.t2,
        },
        teacher_alerts: resp.teacher_alerts || FALLBACK.teacher_alerts,
      };
      loaded.value = true;
    } catch (e) {
      // eslint-disable-next-line no-console
      console.warn("[copyTexts] 拉取展示文案失败，使用兜底文案", e);
    } finally {
      loading.value = false;
    }
  }

  function getBadge(tier: string): BadgeCopy {
    const b = data.value.badges[tier];
    if (b) return b;
    return data.value.badges.together;
  }

  function getBadgeSubtitle(tier: string, lowConfidence: boolean): string {
    const b = getBadge(tier);
    if (lowConfidence) {
      return b.subtitle + data.value.low_confidence_suffix;
    }
    return b.subtitle;
  }

  function getReminderT1(): ReminderCopy {
    return data.value.reminders.t1;
  }
  function getReminderT2(): ReminderCopy {
    return data.value.reminders.t2;
  }

  function renderReminderT1(kpDisplayName: string): {
    title: string;
    body: string;
  } {
    const r = getReminderT1();
    return {
      title: r.title,
      body: render(r.body_template, { kp_display_name: kpDisplayName }),
    };
  }

  function renderReminderT2(kpDisplayName: string): {
    title: string;
    body: string;
  } {
    const r = getReminderT2();
    return {
      title: r.title,
      body: render(r.body_template, { kp_display_name: kpDisplayName }),
    };
  }

  function getTeacherAlerts(): TeacherAlertsCopy {
    return data.value.teacher_alerts;
  }

  function renderTeacherAlert(params: {
    student_name?: string;
    kp_display_name?: string;
    retest_type: string; // 't1' / 't2'
    days_ago: number;
    mastery_level: string; // 'need_review' / 'need_repair'
  }): string {
    const t = getTeacherAlerts();
    return render(t.template, {
      student_name: params.student_name || "",
      kp_display_name: params.kp_display_name || "",
      retest_type:
        t.retest_type_labels[params.retest_type] ||
        params.retest_type.toUpperCase(),
      days_ago: String(params.days_ago),
      mastery_status:
        t.status_labels[params.mastery_level] || params.mastery_level,
    });
  }

  return {
    data,
    loaded,
    loading,
    loadOnce,
    getBadge,
    getBadgeSubtitle,
    getReminderT1,
    getReminderT2,
    renderReminderT1,
    renderReminderT2,
    getTeacherAlerts,
    renderTeacherAlert,
  };
});
