import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "node:path";

// 前端端口取自 DEPLOY_RUN_PORT（沙箱主仓固定 5000；worktree 由沙箱注入）
const FRONTEND_PORT = Number(process.env.DEPLOY_RUN_PORT || 5000);
const BACKEND_PORT = Number(process.env.BACKEND_PORT || 8000);

export default defineConfig(({ mode }) => {
  loadEnv(mode, process.cwd(), "");
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
    server: {
      host: "0.0.0.0",
      port: FRONTEND_PORT,
      strictPort: true,
      proxy: {
        "/api": {
          target: `http://127.0.0.1:${BACKEND_PORT}`,
          changeOrigin: true,
        },
      },
    },
    preview: {
      host: "0.0.0.0",
      port: FRONTEND_PORT,
      strictPort: true,
      // 生产模式下同样把 /api 转发到后端 FastAPI（沙箱内部 8000）
      proxy: {
        "/api": {
          target: `http://127.0.0.1:${BACKEND_PORT}`,
          changeOrigin: true,
        },
      },
      // 允许沙箱公网域名做 Host 头（vite preview 6.x 默认只白名单 localhost）
      allowedHosts: true,
    },
    // 生产构建降级到 ES2015 兼容老浏览器；开发模式保持 esnext 避免 esbuild
    // 错误替换 import.meta（Vite HMR 依赖 import.meta.hot）
    build: {
      target: "es2015",
      rollupOptions: {
        output: {
          manualChunks(id) {
            // Windows 路径可能使用反斜杠，统一处理
            const normalizedId = id.replace(/\\/g, "/");
            // 将 node_modules 中的第三方库拆分为 vendor chunk
            if (normalizedId.includes("/node_modules/")) {
              if (
                normalizedId.includes("/vue/") ||
                normalizedId.includes("vue-router") ||
                normalizedId.includes("pinia")
              ) {
                return "vendor-vue";
              }
              if (
                normalizedId.includes("ant-design-vue") ||
                normalizedId.includes("@ant-design")
              ) {
                return "vendor-antdv";
              }
              // 其他第三方库统一放一个 chunk
              return "vendor";
            }
          },
        },
      },
      // 大 chunk 报警阈值（字节），超过会在构建日志提示
      chunkSizeWarningLimit: 500,
    },
    esbuild: {
      target: mode === "production" ? "es2015" : "esnext",
    },
    optimizeDeps: {
      esbuildOptions: {
        target: mode === "production" ? "es2015" : "esnext",
      },
    },
  };
});
