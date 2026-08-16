import client from "./client";

export interface QuestionForStudent {
  id: number;
  knowledge_point: string;
  q_type: "single" | "judge" | "coding" | "program";
  content: string;
  difficulty: number;
  /** 编程题（积木排序）的候选积木块列表（后端按答案顺序给出，前端负责打乱展示） */
  blocks?: string[] | null;
  /** program 题（编程大题）的判题规则（脱敏后，学员端只看到检查数量/测试用例输入） */
  grading_rules_parsed?: unknown;
  /** program 题的编程语言：scratch / python / cpp */
  program_lang?: "scratch" | "python" | "cpp" | null;
}

export interface StartPayload {
  syllabus_target: string;
  count?: number;
  /** 会话类型：diagnosis（诊断） / retest_t1（复测一） / retest_t2（复测二） */
  session_type?: string;
}

export interface StartResponse {
  session_id: number;
  total_count: number;
  syllabus_target: string;
  session_type: string;
  questions: QuestionForStudent[];
}

export interface AnswerResponse {
  is_correct: boolean;
  correct_count: number;
  total_count: number;
}

export interface FinishResponse {
  session_id: number;
  result_url: string;
  total_rate: number;
}

export interface PerKpResult {
  knowledge_point: string;
  correct_count: number;
  total_count: number;
  correct_rate: number;
  mastery_level: "mastered" | "need_review" | "need_repair";
  low_confidence: boolean;
  /** 关联的奇码课件章节，如 "奇码教材 · 第3章 · P25-28" */
  ppt_ref: string | null;
}

export interface RetestPlan {
  /** 复测T1日期，ISO格式如 "2026-07-27" */
  t1_at: string | null;
  /** 复测T2日期，ISO格式如 "2026-07-31" */
  t2_at: string | null;
  t1_days: number;
  t2_days: number;
  t1_hint: string;
  t2_hint: string;
}

export interface ResultResponse {
  session_id: number;
  student_id: number;
  syllabus_target: string;
  /** 本次会话类型：diagnosis / retest_t1 / retest_t2 */
  session_type: string;
  total_count: number;
  correct_count: number;
  total_rate: number;
  badge: "champion" | "cheer" | "together";
  started_at: string;
  finished_at: string | null;
  per_kp: PerKpResult[];
  retest_plan: RetestPlan;
}

export interface WeightedKpItem {
  knowledge_point: string;
  correct_count: number;
  total_count: number;
  weighted_rate: number;
  mastery_level: string;
  sources: string[];
  ppt_ref: string | null;
}

export interface WeightedResultResponse {
  student_id: number;
  syllabus_target: string;
  total_kp: number;
  items: WeightedKpItem[];
}

export function startSession(payload: StartPayload) {
  return client
    .post<StartResponse>("/diagnosis-sessions/start", payload)
    .then((r) => r.data);
}

export function submitAnswer(
  sessionId: number,
  payload: { question_id: number; student_answer: string; answer_duration_sec?: number },
) {
  return client
    .post<AnswerResponse>(`/diagnosis-sessions/${sessionId}/answer`, payload)
    .then((r) => r.data);
}

/** 上报切屏事件（反作弊） */
export function reportTabSwitch(
  sessionId: number,
  payload: { event_type: "hide" | "show"; away_duration_sec?: number; page_info?: string },
) {
  return client
    .post(`/diagnosis-sessions/${sessionId}/tab-switch`, payload)
    .then((r) => r.data);
}

export function finishSession(sessionId: number) {
  return client
    .post<FinishResponse>(`/diagnosis-sessions/${sessionId}/finish`)
    .then((r) => r.data);
}

export function getResult(sessionId: number) {
  return client
    .get<ResultResponse>(`/diagnosis-sessions/${sessionId}/result`)
    .then((r) => r.data);
}

/** 获取学员加权掌握度总览（T1×0.3 + T2×0.7） */
export function getWeightedResult(syllabus_target: string) {
  return client
    .get<WeightedResultResponse>("/diagnosis-sessions/weighted-result", {
      params: { syllabus_target },
    })
    .then((r) => r.data);
}

/** 学员把诊断报告分享给老师（创建补课工单） */
export function shareReportToTeacher(sessionId: number) {
  return client
    .post<{ ok: boolean; work_order_id: number; message: string }>(
      `/diagnosis-sessions/${sessionId}/share-to-teacher`,
    )
    .then((r) => r.data);
}

/** 学员查看自己的诊断历史 */
export function getMyHistory() {
  return client
    .get<{
      total: number;
      items: Array<{
        id: number;
        session_type: string;
        syllabus_target: string;
        total_count: number;
        correct_count: number;
        status: string;
        started_at: string;
        finished_at: string | null;
        suspicious_flag: boolean;
        suspicious_reason: string | null;
        kp_snapshots: Array<{
          knowledge_point: string;
          correct_count: number;
          total_count: number;
          correct_rate: number;
          mastery_level: string;
        }>;
      }>;
    }>("/diagnosis-sessions/my-history")
    .then((r) => r.data);
}
