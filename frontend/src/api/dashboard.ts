import client from "./client";

export interface SessionTypeStat {
  session_type: string;
  count: number;
}

export interface WorkOrderStat {
  status: string;
  count: number;
}

export interface MasteryStat {
  mastery_level: string;
  count: number;
}

export interface RecentActivity {
  session_id: number;
  student_id: number;
  student_name: string;
  session_type: string;
  syllabus_target: string;
  correct_count: number;
  total_count: number;
  status: string;
  suspicious_flag: boolean;
  started_at: string;
}

export interface DashboardResp {
  student_total: number;
  student_new_this_week: number;
  session_total: number;
  session_finished: number;
  session_in_progress: number;
  suspicious_count: number;
  work_order_pending: number;
  work_order_in_progress: number;
  work_order_completed: number;
  session_type_stats: SessionTypeStat[];
  work_order_stats: WorkOrderStat[];
  mastery_stats: MasteryStat[];
  recent_activities: RecentActivity[];
}

export function fetchDashboardStats() {
  return client
    .get<DashboardResp>("/dashboard/stats")
    .then((r) => r.data);
}
