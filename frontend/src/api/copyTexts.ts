import apiClient from "./client";

export interface BadgeCopy {
  tier: string;
  emoji: string;
  title: string;
  subtitle: string;
}

export interface ReminderCopy {
  type: string;
  days: number;
  target_level: string;
  title: string;
  body_template: string;
}

export interface TeacherAlertsCopy {
  template: string;
  empty_hint: string;
  status_labels: Record<string, string>;
  retest_type_labels: Record<string, string>;
}

export interface CopyTextsResponse {
  badges: Record<string, BadgeCopy>;
  low_confidence_suffix: string;
  reminders: {
    t1: ReminderCopy;
    t2: ReminderCopy;
  };
  teacher_alerts: TeacherAlertsCopy;
}

export async function fetchCopyTexts(): Promise<CopyTextsResponse> {
  const resp = await apiClient.get<CopyTextsResponse>("/copy-texts");
  return resp.data;
}
