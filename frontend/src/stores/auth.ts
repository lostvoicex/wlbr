import { defineStore } from "pinia";
import { computed, ref } from "vue";

type Role = "student" | "teacher" | "admin" | "";

const STORAGE_KEY = "wali_bell_auth";

interface Persisted {
  access: string;
  refresh: string;
  role: Role;
  subject: string;
}

function loadFromStorage(): Persisted | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as Persisted;
  } catch {
    return null;
  }
}

export const useAuthStore = defineStore("auth", () => {
  const persisted = loadFromStorage();
  const accessToken = ref<string>((persisted && persisted.access) || "");
  const refreshToken = ref<string>((persisted && persisted.refresh) || "");
  const role = ref<Role>(((persisted && persisted.role) || "") as Role);
  const subject = ref<string>((persisted && persisted.subject) || "");

  const isLoggedIn = computed(() => !!accessToken.value);
  const isStudent = computed(() => role.value === "student");
  const isStaff = computed(
    () => role.value === "teacher" || role.value === "admin",
  );

  function setAuth(payload: {
    access_token: string;
    refresh_token: string;
    role: string;
    subject: string;
  }) {
    accessToken.value = payload.access_token;
    refreshToken.value = payload.refresh_token;
    role.value = payload.role as Role;
    subject.value = payload.subject;
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        access: payload.access_token,
        refresh: payload.refresh_token,
        role: payload.role,
        subject: payload.subject,
      }),
    );
  }

  function clear() {
    accessToken.value = "";
    refreshToken.value = "";
    role.value = "";
    subject.value = "";
    localStorage.removeItem(STORAGE_KEY);
  }

  return {
    accessToken,
    refreshToken,
    role,
    subject,
    isLoggedIn,
    isStudent,
    isStaff,
    setAuth,
    clear,
  };
});
