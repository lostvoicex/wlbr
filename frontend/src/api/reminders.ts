import apiClient from "./client";

export interface StudentReminderItem {
  kp_original: string;
  mastery_level: string;
  retest_type: string;
  days_ago: number;
  last_snapshot_at: string;
  correct_rate: number;
  syllabus_target: string;
}

export interface StudentRemindersResp {
  student_id: number;
  total: number;
  t1_items: StudentReminderItem[];
  t2_items: StudentReminderItem[];
}

export interface TeacherAlertItem {
  student_id: number;
  student_name: string;
  kp_original: string;
  mastery_level: string;
  retest_type: string;
  days_ago: number;
  last_snapshot_at: string;
}

export interface TeacherAlertsResp {
  total: number;
  items: TeacherAlertItem[];
}

export async function fetchStudentReminders(): Promise<StudentRemindersResp> {
  const resp = await apiClient.get<StudentRemindersResp>(
    "/student-reminders",
  );
  return resp.data;
}

export async function fetchTeacherAlerts(
  limit = 50,
): Promise<TeacherAlertsResp> {
  const resp = await apiClient.get<TeacherAlertsResp>(
    "/teacher-alerts",
    { params: { limit } },
  );
  return resp.data;
}
