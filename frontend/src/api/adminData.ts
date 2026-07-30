import client from "./client";

export interface ImportResult {
  total: number;
  success: number;
  failed: number;
  errors: string[];
  imported_ids: number[];
}

export function importQuestions(data: any[]) {
  return client
    .post<ImportResult>("/admin/questions/import", { items: data })
    .then((r) => r.data);
}

export function exportQuestions() {
  return client.get<any[]>("/admin/questions/export").then((r) => r.data);
}

export function importMappings(data: any[]) {
  return client
    .post<ImportResult>("/admin/mappings/import", { items: data })
    .then((r) => r.data);
}

export function exportMappings() {
  return client.get<any[]>("/admin/mappings/export").then((r) => r.data);
}

export function importStudents(data: any[]) {
  return client
    .post<ImportResult>("/admin/students/import", { items: data })
    .then((r) => r.data);
}

export function exportStudents() {
  return client.get<any[]>("/admin/students/export").then((r) => r.data);
}
