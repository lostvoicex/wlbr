import client from "./client";

export interface TeacherOut {
  id: number;
  teacher_no: string;
  name: string;
  role: string; // teacher / admin
  phone: string | null;
  email: string | null;
  status: string; // active / disabled
  created_at: string;
  updated_at: string;
}

export interface TeacherListResp {
  total: number;
  page: number;
  page_size: number;
  items: TeacherOut[];
}

export interface TeacherCreate {
  teacher_no: string;
  name: string;
  password: string;
  role?: string;
  phone?: string;
  email?: string;
}

export interface TeacherUpdate {
  name?: string;
  role?: string;
  phone?: string;
  email?: string;
  status?: string;
  password?: string;
}

export function listTeachers(params: {
  keyword?: string;
  role?: string;
  status?: string;
  page?: number;
  page_size?: number;
}) {
  return client
    .get<TeacherListResp>("/teachers", { params })
    .then((r) => r.data);
}

export function getTeacher(id: number) {
  return client.get<TeacherOut>(`/teachers/${id}`).then((r) => r.data);
}

export function createTeacher(data: TeacherCreate) {
  return client.post<TeacherOut>("/teachers", data).then((r) => r.data);
}

export function updateTeacher(id: number, data: TeacherUpdate) {
  return client.put<TeacherOut>(`/teachers/${id}`, data).then((r) => r.data);
}

export function deleteTeacher(id: number) {
  return client.delete<void>(`/teachers/${id}`).then((r) => r.data);
}
