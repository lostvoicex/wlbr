import client from "./client";

export type LoginMode = "student_phone" | "student_id" | "teacher";

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
  role: string;
  subject: string;
}

export function login(payload: {
  mode: LoginMode;
  account: string;
  credential: string;
}) {
  return client.post<TokenPair>("/auth/login", payload).then((r) => r.data);
}

export function refresh(refresh_token: string) {
  return client
    .post<TokenPair>("/auth/refresh", { refresh_token })
    .then((r) => r.data);
}
