import client from "./client";

/** 编程大题语言 */
export type ProgramLang = "scratch" | "python" | "cpp";

/** 判题结果 */
export type Verdict =
  | "pending"
  | "judging"
  | "accepted"
  | "wrong_answer"
  | "compile_error"
  | "runtime_error"
  | "time_limit"
  | "partial";

/** 脱敏后的判题规则（学员端展示用） */
export interface GradingRulesParsed {
  // Python/C++ 题：隐藏 expected 字段
  language?: string;
  time_limit?: number;
  memory_limit?: number;
  test_case_count?: number;
  test_cases?: { input: string; hint: string }[];
  // Scratch 题：只返回规则数量
  check_count?: number;
}

/** 编程大题信息 */
export interface OjProblemInfo {
  id: number;
  knowledge_point: string;
  content: string;
  program_lang: ProgramLang;
  grading_rules_parsed: GradingRulesParsed | null;
}

/** 提交请求 */
export interface OjSubmitPayload {
  question_id: number;
  session_id?: number | null;
  language: ProgramLang;
  code: string;
}

/** 提交响应（判题结果） */
export interface OjSubmitResponse {
  submission_id: number;
  question_id: number;
  language: ProgramLang;
  verdict: Verdict;
  score: number;
  passed_cases: number;
  total_cases: number;
  details: unknown | null;
  stderr: string | null;
  judge_duration_ms: number | null;
  created_at: string;
}

/** 获取编程大题信息（脱敏） */
export function getProblem(questionId: number) {
  return client
    .get<OjProblemInfo>(`/oj/problem/${questionId}`)
    .then((r) => r.data);
}

/** 提交编程大题并获取判题结果 */
export function submitCode(payload: OjSubmitPayload) {
  return client
    .post<OjSubmitResponse>("/oj/submit", payload, { timeout: 30000 })
    .then((r) => r.data);
}

/** 查询某次提交结果 */
export function getSubmission(submissionId: number) {
  return client
    .get<OjSubmitResponse>(`/oj/submissions/${submissionId}`)
    .then((r) => r.data);
}

/** 学员提交历史列表 */
export function listSubmissions(params: {
  question_id?: number;
  session_id?: number;
  page?: number;
  page_size?: number;
}) {
  return client
    .get("/oj/submissions", { params })
    .then((r) => r.data);
}

/** 学员在某道编程题的历史提交 */
export function getQuestionHistory(questionId: number, limit = 10) {
  return client
    .get(`/oj/history/${questionId}`, { params: { limit } })
    .then((r) => r.data);
}
