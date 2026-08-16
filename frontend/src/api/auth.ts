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
  captcha_id: string;
  captcha_code: string;
}) {
  return client.post<TokenPair>("/auth/login", payload).then((r) => r.data);
}

export function refresh(refresh_token: string) {
  return client
    .post<TokenPair>("/auth/refresh", { refresh_token })
    .then((r) => r.data);
}

export function getCaptchaImage(captchaId?: string): string {
  const baseURL = (client.defaults.baseURL || "/api/v1").replace(/\/$/, "");
  const idParam = captchaId ? `&captcha_id=${captchaId}` : "";
  return `${baseURL}/captcha/image?t=${Date.now()}${idParam}`;
}

export async function createCaptcha(): Promise<{ captcha_id: string; expires_in: number }> {
  return client.get("/captcha/new").then((r) => r.data);
}
