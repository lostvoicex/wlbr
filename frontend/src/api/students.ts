import client from "./client";

export interface StudentOut {
  id: number;
  name: string;
  grade: number;
  phone: string | null;
  syllabus_target: string | null;
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

export interface StudentListResp {
  total: number;
  page: number;
  page_size: number;
  items: StudentOut[];
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
