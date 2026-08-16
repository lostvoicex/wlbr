import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import brand from "@/config/brand";

function requireAdmin(_to: any, _from: any, next: (arg?: string) => void) {
  const auth = useAuthStore();
  if (auth.role === "admin") {
    next();
  } else {
    next("/teacher/students");
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/student/login",
  },
  // ---------- 学员端 ----------
  {
    path: "/student/login",
    name: "StudentLogin",
    component: () => import("@/views/student/StudentLogin.vue"),
    meta: { side: "kid" },
  },
  {
    path: "/student/home",
    name: "StudentHome",
    component: () => import("@/views/student/StudentHome.vue"),
    meta: { side: "kid", requiresRole: "student" },
  },
  {
    path: "/student/diagnosis/:syllabus_target",
    name: "StudentDiagnosis",
    component: () => import("@/views/student/StudentDiagnosis.vue"),
    meta: { side: "kid", requiresRole: "student" },
  },
  {
    path: "/student/result/:session_id",
    name: "StudentResult",
    component: () => import("@/views/student/StudentResult.vue"),
    meta: { side: "kid", requiresRole: "student" },
  },
  {
    path: "/student/history",
    name: "StudentHistory",
    component: () => import("@/views/student/StudentHistory.vue"),
    meta: { side: "kid", requiresRole: "student" },
  },
  // ---------- 老师端 ----------
  {
    path: "/teacher/login",
    name: "TeacherLogin",
    component: () => import("@/views/teacher/TeacherLogin.vue"),
    meta: { side: "teacher" },
  },
  {
    path: "/teacher",
    component: () => import("@/views/teacher/TeacherLayout.vue"),
    meta: { side: "teacher", requiresRole: "staff" },
    children: [
      {
        path: "",
        redirect: "/teacher/dashboard",
      },
      {
        path: "dashboard",
        name: "TeacherDashboard",
        component: () => import("@/views/teacher/TeacherDashboard.vue"),
      },
      {
        path: "students",
        name: "TeacherStudents",
        component: () => import("@/views/teacher/TeacherStudents.vue"),
      },
      {
        path: "students/:id",
        name: "TeacherStudentDetail",
        component: () => import("@/views/teacher/TeacherStudentDetail.vue"),
      },
      {
        path: "work-orders",
        name: "TeacherWorkOrders",
        component: () => import("@/views/teacher/TeacherWorkOrders.vue"),
      },
      {
        path: "mappings",
        name: "TeacherMappings",
        component: () => import("@/views/teacher/TeacherMappings.vue"),
      },
      {
        path: "teachers",
        name: "TeacherTeachers",
        component: () => import("@/views/teacher/TeacherTeachers.vue"),
        beforeEnter: requireAdmin,
      },
      {
        path: "data-admin",
        name: "TeacherDataAdmin",
        component: () => import("@/views/teacher/TeacherDataAdmin.vue"),
        beforeEnter: requireAdmin,
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/student/login",
  },
];

// GitHub Pages 部署在子路径 /wlbr/ 下，需要同步 router base
const routerBase = import.meta.env.BASE_URL;

const router = createRouter({
  history: createWebHistory(routerBase),
  routes,
});

router.beforeEach((to) => {
  // 按端动态设置浏览器标题
  const side = to.meta && to.meta.side;
  if (side === "kid") {
    document.title = brand.platformNameStudent;
  } else if (side === "teacher") {
    document.title = brand.platformNameTeacher;
  }

  const auth = useAuthStore();
  const required = (to.meta && to.meta.requiresRole) as string | undefined;
  if (!required) return true;

  if (required === "student") {
    if (!auth.isLoggedIn || !auth.isStudent) return "/student/login";
  } else if (required === "staff") {
    if (!auth.isLoggedIn || !auth.isStaff) return "/teacher/login";
  }
  return true;
});

export default router;
