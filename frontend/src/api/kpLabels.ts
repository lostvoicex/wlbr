import apiClient from "./client";

export interface KpLabel {
  original_name: string;
  display_name: string;
  description: string;
}

export interface KpLabelsResponse {
  total: number;
  items: KpLabel[];
  map: Record<string, KpLabel>;
}

export async function fetchKpLabels(): Promise<KpLabelsResponse> {
  const resp = await apiClient.get<KpLabelsResponse>("/kp-labels");
  return resp.data;
}
