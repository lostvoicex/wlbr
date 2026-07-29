import axios, { AxiosError } from "axios";
import { useAuthStore } from "@/stores/auth";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api/v1";
const client = axios.create({
  baseURL,
  timeout: 15000,
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

client.interceptors.response.use(
  (resp) => resp,
  (error: AxiosError<{ detail?: string }>) => {
    if (error && error.response && error.response.status === 401) {
      const auth = useAuthStore();
      auth.clear();
    }
    return Promise.reject(error);
  },
);

export function extractErrorMessage(err: unknown, fallback = "请求失败"): string {
  const ax = err as AxiosError<{ detail?: string }> | undefined;
  if (ax && ax.response && ax.response.data && ax.response.data.detail) {
    return ax.response.data.detail;
  }
  if (ax && ax.message) return ax.message;
  return fallback;
}

export default client;
