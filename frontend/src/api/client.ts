import axios, { AxiosError } from "axios";
import { useAuthStore } from "@/stores/auth";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api/v1";

// 生产环境（Render 免费版）有冷启动休眠机制，首次请求可能需要 30-60 秒唤醒
const isProd = baseURL.startsWith("https://");
const REQUEST_TIMEOUT = isProd ? 60000 : 15000;

const client = axios.create({
  baseURL,
  timeout: REQUEST_TIMEOUT,
});

client.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.accessToken) {
    if (!config.headers) {
      config.headers = {} as typeof config.headers;
    }
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
});

// 生产环境：网络超时自动重试一次（应对 Render 冷启动）
client.interceptors.response.use(
  (resp) => resp,
  async (error: AxiosError) => {
    // 401 清理登录态
    if (error && error.response && error.response.status === 401) {
      const auth = useAuthStore();
      auth.clear();
      return Promise.reject(error);
    }

    // 超时或网络错误：生产环境自动重试一次
    const isTimeout =
      error.code === "ECONNABORTED" ||
      error.code === "ETIMEDOUT" ||
      error.message?.includes("timeout") ||
      error.message?.includes("Network Error");

    if (isTimeout && isProd && error.config) {
      // 标记已重试，避免无限循环
      const cfg = error.config as typeof error.config & { _retried?: boolean };
      if (!cfg._retried) {
        cfg._retried = true;
        console.log("[API] 请求超时，正在重试（服务器可能正在唤醒）...");
        return client.request(cfg);
      }
    }

    return Promise.reject(error);
  },
);

export function extractErrorMessage(err: unknown, fallback = "请求失败"): string {
  const ax = err as AxiosError<{ detail?: string }> | undefined;
  if (ax && ax.response && ax.response.data && ax.response.data.detail) {
    return ax.response.data.detail;
  }
  if (ax && ax.message) {
    if (ax.code === "ECONNABORTED" || ax.code === "ETIMEDOUT") {
      return "服务器唤醒中，请等几秒再试一次～";
    }
    return ax.message;
  }
  return fallback;
}

export default client;
