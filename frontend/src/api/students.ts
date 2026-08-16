import client from "./client";

export interface StudentOut {
  id: number;
  name: string;
  grade: number;
  phone: string | null;
  syllabus_target: string | null;
  learning_note: string | null;
  created_at: string;
  updated_at: string;
}

export interface StudentCreate {
  name: string;
  grade: number;
  phone?: string;
  syllabus_target?: string;
  password?: string;
}

export interface StudentUpdate {
  name?: string;
  grade?: number;
  phone?: string;
  syllabus_target?: string;
  learning_note?: string;
  password?: string;
}

export interface StudentListResp {
  total: number;
  page: number;
  page_size: number;
  items: StudentOut[];
}

export interface KpSnapshot {
  knowledge_point: string;
  correct_count: number;
  total_count: number;
  correct_rate: number;
  mastery_level: string;
}

export interface SessionHistoryItem {
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
  kp_snapshots: KpSnapshot[];
}

export interface SessionHistoryResp {
  total: number;
  items: SessionHistoryItem[];
}

export function listStudents(params: {
  keyword?: string;
  grade?: number;
  page?: number;
  page_size?: number;
}) {
  return client
    .get<StudentListResp>("/students", { params })
    .then((r) => r.data);
}

export function createStudent(data: StudentCreate) {
  return client.post<StudentOut>("/students", data).then((r) => r.data);
}

export function getStudent(id: number) {
  return client.get<StudentOut>(`/students/${id}`).then((r) => r.data);
}

export function updateStudent(id: number, data: StudentUpdate) {
  return client.put<StudentOut>(`/students/${id}`, data).then((r) => r.data);
}

export function getStudentSessions(id: number) {
  return client
    .get<SessionHistoryResp>(`/students/${id}/sessions`)
    .then((r) => r.data);
}
