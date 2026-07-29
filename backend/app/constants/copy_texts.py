"""文案常量：结果报告徽章 + 学生端复测提醒 + 老师端催办话术。

所有含 KP 名的模板都用 {kp_display_name} 变量占位。渲染时前端从 kp_labels
store 拿童趣化名后再嵌入；数据库层保持存原名不变。
"""
from typing import Any, Dict


# ---------- 1. 结果报告页 · 3 档徽章卡文案 ----------
BADGES: Dict[str, Dict[str, str]] = {
    "champion": {
        "tier": "champion",
        "emoji": "🏆",
        "title": "小小编程家",
        "subtitle": "哇塞！这个知识点你已经玩得飞起～小猫都想拜你为师啦！",
    },
    "cheer": {
        "tier": "cheer",
        "emoji": "💪",
        "title": "加油小勇士",
        "subtitle": "就差一点点就掌握啦！我们过 3 天再来玩一次，肯定就搞定～",
    },
    "together": {
        "tier": "together",
        "emoji": "🌟",
        "title": "一起来突破",
        "subtitle": "这个知识点有点小挑战，别怕～老师和小猫都在这里陪你，7 天后再战！",
    },
}

# low_confidence（≤2 题）时徽章档位不变，但副标题追加此后缀
LOW_CONFIDENCE_SUFFIX = "（这个结果只做参考，题目太少啦～）"


# ---------- 2. 复测到期提醒（学生端） ----------
REMINDERS_T1: Dict[str, Any] = {
    "type": "t1",
    "days": 3,
    "target_level": "need_review",
    "title": "小猫在等你复习～",
    # 模板变量：{kp_display_name}
    "body_template": "上次学的【{kp_display_name}】你还记得吗？3 天没见啦，来做几道题给小猫看看吧！",
}

REMINDERS_T2: Dict[str, Any] = {
    "type": "t2",
    "days": 7,
    "target_level": "need_repair",
    "title": "这次一定拿下～",
    "body_template": "【{kp_display_name}】上次差一点点，休息 7 天了，现在再来试试，肯定不一样！",
}


# ---------- 3. 老师后台 · 复测催办话术 ----------
# 模板变量：
#   {student_name}     学员昵称
#   {kp_display_name}  KP 童趣化名（前端读 kp_labels 映射）
#   {retest_type}      T1 / T2
#   {days_ago}         距上次做题天数
#   {mastery_status}   need_review / need_repair 的中文描述
TEACHER_ALERT_TEMPLATE = (
    "{student_name} 的【{kp_display_name}】{retest_type} 复测到期"
    "（{days_ago} 天前 {mastery_status}），建议今天推一次复测题"
)

TEACHER_ALERTS: Dict[str, Any] = {
    "template": TEACHER_ALERT_TEMPLATE,
    "empty_hint": "暂无待催办的复测，学员们都还在稳步学习中～",
    "status_labels": {
        "need_review": "待巩固",
        "need_repair": "需加练",
    },
    "retest_type_labels": {
        "t1": "T1",
        "t2": "T2",
    },
}


def get_all_copy_texts() -> Dict[str, Any]:
    """打包全量文案给 /api/v1/copy-texts 接口。"""
    return {
        "badges": BADGES,
        "low_confidence_suffix": LOW_CONFIDENCE_SUFFIX,
        "reminders": {
            "t1": REMINDERS_T1,
            "t2": REMINDERS_T2,
        },
        "teacher_alerts": TEACHER_ALERTS,
    }
