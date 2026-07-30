import client from "./client";

export interface KpMappingOut {
  id: number;
  syllabus_version: string;
  knowledge_point: string;
  courseware_name: string;
  chapter: string;
  page_ref: string | null;
  chapter_title: string | null;
  match_score: number;
  source: string; // ai / manual / import
  review_status: string; // pending / approved / rejected / needs_review
  review_level: number; // 1-5
  is_active: boolean;
  sort_order: number;
  reviewer1_id: number | null;
  reviewer2_id: number | null;
  review_note: string | null;
  created_at: string;
  updated_at: string;
}

export interface KpMappingListResp {
  total: number;
  page: number;
  page_size: number;
  items: KpMappingOut[];
}

export interface MappingReviewOut {
  id: number;
  mapping_id: number;
  reviewer_id: number | null;
  reviewer_name: string | null;
  review_round: number;
  result: string;
  review_level: number;
  note: string | null;
  created_at: string;
}

export interface MappingCreate {
  syllabus_version: string;
  knowledge_point: string;
  courseware_name: string;
  chapter: string;
  page_ref?: string;
  chapter_title?: string;
  match_score?: number;
  source?: string;
  sort_order?: number;
}

export interface MappingUpdate {
  syllabus_version?: string;
  knowledge_point?: string;
  courseware_name?: string;
  chapter?: string;
  page_ref?: string;
  chapter_title?: string;
  match_score?: number;
  is_active?: boolean;
  sort_order?: number;
}

export interface MappingReviewInput {
  result: string; // approved / rejected / needs_review
  review_level: number; // 1-5
  note?: string;
}

export function listMappings(params: {
  keyword?: string;
  syllabus_version?: string;
  knowledge_point?: string;
  courseware_name?: string;
  review_status?: string;
  source?: string;
  is_active?: boolean;
  page?: number;
  page_size?: number;
}) {
  return client
    .get<KpMappingListResp>("/kp-mappings", { params })
    .then((r) => r.data);
}

export function getMapping(id: number) {
  return client.get<KpMappingOut>(`/kp-mappings/${id}`).then((r) => r.data);
}

export function createMapping(data: MappingCreate) {
  return client.post<KpMappingOut>("/kp-mappings", data).then((r) => r.data);
}

export function updateMapping(id: number, data: MappingUpdate) {
  return client
    .put<KpMappingOut>(`/kp-mappings/${id}`, data)
    .then((r) => r.data);
}

export function deleteMapping(id: number) {
  return client.delete<void>(`/kp-mappings/${id}`).then((r) => r.data);
}

export function reviewMapping(id: number, data: MappingReviewInput) {
  return client
    .post<KpMappingOut>(`/kp-mappings/${id}/review`, data)
    .then((r) => r.data);
}

export function listMappingReviews(id: number) {
  return client
    .get<MappingReviewOut[]>(`/kp-mappings/${id}/reviews`)
    .then((r) => r.data);
}
