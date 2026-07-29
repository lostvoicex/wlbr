import client from "./client";

export interface WorkOrderOut {
  id: number;
  student_id: number;
  session_id: number | null;
  teacher_id: number | null;
  assignee_id: number | null;
  syllabus_target: string;
  weak_kps: string;
  title: string;
  description: string | null;
  chapters_json: string | null;
  status: string; // pending / in_progress / completed / cancelled
  priority: string; // low / medium / high
  due_date: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
  student_name?: string;
  teacher_name?: string;
  assignee_name?: string;
}

export interface WorkOrderListResp {
  total: number;
  page: number;
  page_size: number;
  items: WorkOrderOut[];
}

export interface WorkOrderCreate {
  student_id: number;
  session_id?: number;
  syllabus_target: string;
  weak_kps: string;
  title: string;
  description?: string;
  priority?: string;
  due_date?: string;
  assignee_id?: number;
}

export interface WorkOrderUpdate {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  due_date?: string;
  weak_kps?: string;
  assignee_id?: number;
}

export function listWorkOrders(params: {
  keyword?: string;
  student_id?: number;
  status?: string;
  priority?: string;
  syllabus_target?: string;
  page?: number;
  page_size?: number;
}) {
  return client
    .get<WorkOrderListResp>("/work-orders", { params })
    .then((r) => r.data);
}

export function getWorkOrder(id: number) {
  return client.get<WorkOrderOut>(`/work-orders/${id}`).then((r) => r.data);
}

export function createWorkOrder(data: WorkOrderCreate) {
  return client.post<WorkOrderOut>("/work-orders", data).then((r) => r.data);
}

export function updateWorkOrder(id: number, data: WorkOrderUpdate) {
  return client.put<WorkOrderOut>(`/work-orders/${id}`, data).then((r) => r.data);
}

export function cancelWorkOrder(id: number) {
  return client
    .post<WorkOrderOut>(`/work-orders/${id}/cancel`)
    .then((r) => r.data);
}

export function completeWorkOrder(id: number) {
  return client
    .post<WorkOrderOut>(`/work-orders/${id}/complete`)
    .then((r) => r.data);
}
