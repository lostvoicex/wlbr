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
    .post<ImportResult>("/admin-data/questions/import", data)
    .then((r) => r.data);
}

export function exportQuestions() {
  return client.get<any[]>("/admin-data/questions/export").then((r) => r.data);
}

export function importMappings(data: any[]) {
  return client
    .post<ImportResult>("/admin-data/mappings/import", data)
    .then((r) => r.data);
}

export function exportMappings() {
  return client.get<any[]>("/admin-data/mappings/export").then((r) => r.data);
}

export function importStudents(data: any[]) {
  return client
    .post<ImportResult>("/admin-data/students/import", data)
    .then((r) => r.data);
}

export function exportStudents() {
  return client.get<any[]>("/admin-data/students/export").then((r) => r.data);
}
        
