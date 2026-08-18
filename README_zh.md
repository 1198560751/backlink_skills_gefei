# 开源外链与产品目录提交 Skill

> 由 [Flaq.ai](https://flaq.ai/zh/) 创建，适用于 Codex、Claude Code 等 AI 编程 Agent。

这是一个可审计、可恢复的产品目录提交工作流，适合将产品、软件、创业项目、应用和网站提交到产品目录及其他公开发现渠道。它帮助 Agent 核查渠道资格、避免重复提交、遵守授权边界、保留人工验证步骤、仅提交真实信息，并生成可由其他执行者继续处理的证据记录。

目录收录可能带来品牌引用、引荐流量或外链，但本项目**不承诺**外链一定上线、链接属性、审核通过、搜索引擎收录、流量或排名提升。

**语言：** [English](README.md) · [简体中文](README_zh.md) · [繁體中文](README_tw.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [ไทย](README_th.md) · [Tiếng Việt](README_vi.md) · [Bahasa Indonesia](README_id.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Italiano](README_it.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md) · [हिन्दी](README_hi.md) · [Türkçe](README_tr.md) · [Nederlands](README_nl.md) · [Polski](README_pl.md)

## 支持的渠道

- 产品、软件、AI 工具、创业公司、企业、应用和网站目录
- `Request app`、推荐申请、认领条目和供应商申请
- 经授权的免费账号或公开资料创建
- 博客、文章、新闻、社区、邮件和联系表单投稿
- 资源页、合作伙伴目录及类似的公开发现渠道
- 渠道资格、费用、互链、账号、重复条目和验证要求检查
- 有证据支撑的状态跟踪与可恢复任务记录

## 核心安全边界

- 只使用已核实的产品、公司、创始人、价格、联系人、所有权和法律信息。
- 不绕过 CAPTCHA、Turnstile、2FA、Passkey、邮箱验证或其他安全机制。
- 不使用验证码代答、隐身技术、代理轮换或指纹规避。
- 未经单独授权，不付款、不启用续费、不添加互链、不修改网站或 DNS、不上传验证文件、不认领所有权。
- 不把注册账号、保存草稿、点击按钮或页面跳转当成已发布。
- 最终提交结果不明确时先调查，不重复提交，以免制造重复条目。

## 工作流程

1. 读取已批准的产品资料、描述版本、URL、素材、授权规则和已有记录。
2. 规范化并去重目标 URL。
3. 先核查可用性、适配度、费用、互链、账号、条款、重复条目和“认领/新建”条件。
4. 将验证码、邮箱、手机、2FA 等人工验证汇总成一个有序队列。
5. 验证完成后，只用已批准的事实和素材填写表单。
6. 最终操作前再次核对费用、品牌、规范 URL、分类、上传内容、协议、重复风险和授权。
7. 立即记录准确响应、时间、结果 URL 和证据。
8. 审计任务记录，并分别报告每种状态。

## 使用方法

将 `submit-product-directories-open-source/` 复制到 Agent 支持的 Skills 目录，或直接在项目中引用，然后输入：

```text
使用 $submit-product-directories-open-source 检查这批目录 URL，
并为我们的产品准备提交任务。

先完成资格与验证扫描。没有在授权矩阵中明确许可时，不发布、
不创建账号、不接受协议、不付款。保存可审计记录，并把所有需要
人工完成的验证集中到一个队列中。
```

Agent 应先读取 `SKILL.md`，再按需加载 `references/`。如果没有任务记录，应复制 `assets/submission-record-template.md`，不要另造格式。

## 状态、审计与测试

`submitted` 需要可靠回执；`awaiting email verification` 表示等待邮箱验证；`awaiting approval` 表示网站明确进入审核；`published` 需要公开且非预览的产品页；`submission outcome unknown` 必须先调查再重试；`submission failed` 需要明确失败证据。

不能仅凭点击、跳转、表单清空、按钮禁用或没有报错推断成功。

```bash
python3 submit-product-directories-open-source/scripts/audit_submission_record.py path/to/record.md
python3 submit-product-directories-open-source/scripts/audit_submission_record.py path/to/record.md --json
python3 -m unittest discover -s submit-product-directories-open-source/tests
```

状态无效、缺少必要证据、提交 URL 重复、存在未解决占位符或时间格式错误时，审计器会返回非零退出码。

## 关于 Flaq.ai

[Flaq.ai](https://flaq.ai/zh/) 为 AI Agent 和生产应用提供图片、视频、音乐和语言模型的统一接入。本项目由 Flaq AI 团队维护，旨在开源分享谨慎、可执行、可复用的产品发现渠道提交工作流。

相关合集：[Awesome Codex Skills](https://github.com/flaqai/awesome_codex_skills) · [Awesome Claude Code Skills](https://github.com/flaqai/awesome_claude_code_skills)

## 许可证

参见 [LICENSE](LICENSE)。
