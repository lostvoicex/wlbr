import { createApp } from "vue";
import { createPinia } from "pinia";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";

import App from "./App.vue";
import router from "./router";
import "./styles/global.css";

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(Antd);
app.mount("#app");

// 应用挂载完后异步拉一次 KP 童趣化标签（免鉴权，失败不阻塞界面）
import("./stores/kpLabels").then(({ useKpLabelsStore }) => {
  useKpLabelsStore(pinia).loadOnce();
});

// 同步拉一次展示文案（徽章 / 复测提醒 / 老师催办）
import("./stores/copyTexts").then(({ useCopyTextsStore }) => {
  useCopyTextsStore(pinia).loadOnce();
});
