<div align="center">

<!-- <img src="assets/banner.png" alt="亚马逊竞品狙击手" width="100%"> -->

# 🎯 Amazon Competitor Radar

**亚马逊竞品狙击手：五步找出真实对手，筛选值得学的对象，输出可执行的打法总表。**

**想了解更多最新AI行业动态,AI+电商/广告的行业实践方法,人与AI如何协作共生的思考,请关注公众号:【新西楼.AI】**

![qrcode_for_gh_e3b954bd3859_258](https://github.com/user-attachments/assets/d8f068d9-c4f8-46c7-914c-fbcab5d52f2a)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-SKILL-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![Version](https://img.shields.io/badge/version-0.1.0-black.svg)]()

**流量词反查 · 关键词重叠聚合 · 主图三分类 · 五维度打分 · 人工确认 · 打法总表**

**Created By Buluu@新西楼.AI**

</div>

## 项目简介

亚马逊竞品狙击手 是由 **buluslan（公众号：新西楼.AI）** 研发的亚马逊竞品识别工具。

你输入一个 ASIN 和站点，Skill 会反查流量词并按关键词重叠聚合候选竞品（需接入可用的亚马逊数据源），先看主图区分同方案、跨方案和无关产品，再从价格带、人群场景、卖点结构、标题布局和发展阶段五个维度筛选对标对象——每一步都留给你确认和纠偏，最后输出一套带核心词清单、竞品名单和打法总表的分析结果，讲清谁值得学、学什么、什么不能照搬。

这是 Agent 通用的指令集，可作为 Claude Code、Codex、Cursor 等 Agent 的工作指令使用；实际取数和读图能力由运行环境提供。Claude Code 是安装方式之一，不是唯一适用平台。

## ✨ 它做什么

竞品不仅是同类目产品，更是打同一批关键词、争夺类似流量的产品。不同形态的产品，也可能在解决同一个场景问题。

| 步骤 | 核心动作 | 交付物 |
|---|---|---|
| ① 反查圈词 | 将流量词分为品类词与场景词，各取流量贡献最高的至多 10 个词。 | 核心词清单和流量结构诊断。 |
| ② 搜词聚合 | 逐词取商品列表，按重叠词数聚合，并排除自身及已确认的同父变体。 | 15–20 个候选竞品及其重叠词明细；数据不足时如实标注。 |
| ③ 看图分类 | 对比真实主图，区分同方案、跨方案和场景无关产品。 | 附图片依据的分类名单；不能判断的留给人工确认。 |
| ④ Listing 打分 | 仅对同方案竞品做五维度打分，识别适合参考的对象。 | 核心对标、待定、只防不学三档名单。 |
| ⑤ 汇总打法 | 核心对标分析打法，跨方案只借鉴场景切入思路。 | 值得学的内容、不能照搬的原因和具体动作建议。 |

评分规则以 [五维度打分规则](references/scoring-rules.md) 为准；分数是判断依据，最终名单由你确认。

## 🚀 快速开始

### 安装到 Claude Code

此仓库为私有仓库，克隆前需使用有访问权限的 GitHub 账号登录。以下方式需要已安装 GitHub CLI：

```bash
gh auth status
mkdir -p ~/.claude/skills
gh repo clone buluslan/amazon-competitor-radar ~/.claude/skills/amazon-competitor-radar
```

Codex、Cursor 等 Agent 用户可将 [SKILL.md](SKILL.md) 作为指令输入，同时提供同目录的 `references/` 文件；按各运行环境的技能加载方式安装即可。

### 最小输入

将下方 ASIN 占位符替换为你要分析的真实 ASIN：

```text
使用 amazon-competitor-radar，帮我看看这个产品的对手都是谁。
ASIN：填写真实 ASIN
站点：US
```

先提供 ASIN 和站点；走到第四步时，再补充一句产品定位，例如“面向新手的高性价比自动卷发器”。每一步交付后，确认或纠正结果，再继续下一步。

## 🔌 数据接入

不绑定某一家数据服务，按所需字段选择可用的数据工具。

| 数据能力 | 用途 |
|---|---|
| ASIN 流量词反查及流量贡献 | 圈出品类词和场景词。 |
| 每个关键词下的商品列表 | 统计关键词重叠，形成候选池。 |
| 商品详情、价格、上架时间和评分数 | 补全候选信息并完成五维度打分。 |
| 商品主图和 Agent 读图能力 | 区分同方案与跨方案竞品；无法读图时由人工确认。 |
| 评论、促销与销量或排名趋势 | 支持第五步分析；缺失项明确标注，不编造。 |

第一步的核心词表可以手动提供，第二步起需要可用的数据工具。环境里工具调用失败时会如实报告；没有数据时不生成猜测的词表或候选名单。字段说明见 [数据提取与兜底](references/data-fallback.md)。

交付围绕一次竞品识别与打法参考展开；周期性追踪需另行配置存档和重跑流程。单个已知竞品的完整深拆、批量评论深分析与选品可行性拍板交由相应工具或人工完成。

## 🏠 交流社区

<div align="center">

🎯 **更多 AI 实战教程和专属福利尽在我们「MBG 跨境AI实战圈」,已有 50+ 跨境大卖、AI 专家热聊中**

—— 欢迎跨境电商从业者加入我们,一起探索 AI+商业的最佳实践和真实边界,跑通【跨境AI】的从 0 到 1,打败你的同事,干掉你的老板。

**社区介绍:[my.feishu.cn/wiki/WNi0wh3mIiOLhzkCLFPcwUr9nrg](https://my.feishu.cn/wiki/WNi0wh3mIiOLhzkCLFPcwUr9nrg)**

<img width="1125" height="618" alt="image" src="https://github.com/user-attachments/assets/20f47cd6-e33c-4f3e-9362-3846c11135fd" />

</div>

## 📁 结构

```text
amazon-competitor-radar/
├── SKILL.md
├── references/
│   ├── data-fallback.md
│   ├── scoring-rules.md
│   └── step5-playbook.md
├── evals/
│   └── evals.json
├── ci/
│   └── validate.py
├── .github/workflows/validate.yml
├── requirements-dev.txt
├── release.yml
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## ✅ 本地校验

运行校验需要 Python 3.9+；使用独立环境安装开发依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python ci/validate.py
```

自动校验覆盖元数据、版本一致性、JSON/YAML 解析、文件引用和发布文件范围。`evals/evals.json` 保留 4 个行为评测用例，需在具备取数及读图能力的 Agent 环境中另行执行；结构校验不等同于真实业务端到端测试。

## 📜 License

采用 [MIT License](LICENSE)，署名 **Buluu@新西楼.AI**。仓库可见性保持私有；MIT 是代码与文档的使用许可，不表示仓库已公开。

## 📖 写在最后

<div align="center">

**如果这个工具帮到了你,欢迎 ⭐ Star 支持。更多 AI × 跨境电商实操内容,关注公众号「新西楼.AI」。**

</div>
