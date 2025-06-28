---
description: harper.blog 的版本说明
hideReply: true
menu:
    footer:
        name: 版本说明
        weight: 3
nofeed: true
slug: colophon
title: 版本说明
translationKey: colophon
type: special
url: colophon
weight: 6
---

[harper.blog](https://harper.blog) 是 Harper Reed 的个人博客，采用现代 Web 技术与静态站点生成相关技术构建。

## 技术栈

- **静态站点生成器**：[Hugo](https://gohugo.io/)
- **托管平台**：[Netlify](https://www.netlify.com/)
- **版本控制**：Git（托管于 GitHub）

## 设计与布局

- 本网站采用基于 [Bear Cub](https://github.com/clente/hugo-bearcub) 的定制主题 ᕦʕ •ᴥ•ʔᕤ
- ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•！
- 排版：使用系统字体，以获得最佳性能和原生外观
- 响应式设计确保在各类设备和屏幕尺寸上均能良好呈现

## 内容管理

- 所有内容均采用 Markdown 编写

## 构建与部署

- 已在 Netlify 上配置持续部署
- 当代码推送至主分支时，网站将自动构建并部署
- 自定义构建命令与设置写入 `netlify.toml`

## 性能优化

- 图片已优化，并在可能的情况下以 WebP 格式提供
- 生产环境中对 CSS 进行压缩
- 借助 Hugo 内置的资源管线（asset pipeline）进行资源优化

## 附加功能

- 提供 RSS 订阅源，便于聚合阅读
- 实现社交媒体 meta 标签，便于在 Twitter、Facebook 等平台分享
- 通过自定义短代码（shortcode）增强内容排版（例如 Kit.co 集成）

## 开发工具

- 使用 `Makefile` 简化常见开发任务
- 项目采用 Go 模块（Go Modules）进行依赖管理

## 可访问性与标准

- 本网站致力于无障碍访问，并遵循现代 Web 标准
- 全站采用语义化 HTML

## 分析

- 本网站使用 [tinylytics](https://tinylytics.app/) 追踪各类访问数据（bits & hits）。你可以在[此处](https://tinylytics.app/public/cw1YY9KSGSE4XkEeXej7)查看公开统计。
- 本网站已收到（recieved） {{< ta_hits >}} 次访问，访问者来自以下国家：{{< ta_countries >}}。

## 作者与维护

本网站由 Harper Reed 维护。如有疑问，请联系 [harper@modest.com](mailto:harper@modest.com)。

最后更新：2024年9月

## 变更日志

以下为本次迭代的 Git 提交记录：

{{< readfile file="gitlog.md" markdown="true" >}}

---

本网站 ❤️ 由 Hugo 构建，借助 Netlify 部署。
