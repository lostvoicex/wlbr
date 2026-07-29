/**
 * 品牌视觉常量集中配置。
 *
 * 所有页面读取此处的常量，禁止在业务代码里硬编码颜色 / 平台名 / logo URL。
 * 后续需要更换品牌（例如更换 logo、微调主色），只需要改这一处。
 */
export const brand = {
  // 平台名（按端区分）
  platformNameStudent: "瓦力贝尔·成长小助手",
  platformNameTeacher: "瓦力贝尔编程薄弱定位平台",

  // 品牌配色（Scratch 官方色系）
  primaryColor: "#FF7E1A", // Scratch 官方橙：主按钮 / 进度条 / 徽章 / CTA
  accentColor: "#4C97FF", // Scratch 官方蓝：二级按钮 / 链接 / 信息标签
  neutralGray: "#6B7280", // 正文次要文字 / 边框 / 禁用态

  // Logo URL（空字符串走占位组件；老师后续上传后填 URL）
  logoStudent: "",
  logoTeacher: "",
};

export default brand;
