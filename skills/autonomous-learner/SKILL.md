---
name: autonomous-learner
description: 空闲进化模式 — 当用户空闲1小时以上时，主动分析近期任务模式，预测用户可能需要的技能，主动学习并汇报。参考Pask DD-MM-PAS框架 + CoPaw内置能力。
---

# Autonomous Learner（自主进化）

> **参考**: Pask DD-MM-PAS框架 + CoPaw内置reme_light记忆系统
> **论文**: https://arxiv.org/abs/2604.08000

**触发条件：用户空闲**

## 🏠 CoPaw 内置能力（必须使用！）

```
┌─────────────────────────────────────────────────────┐
│  CoPaw 内置生态系统（我的工具箱）                    │
│                                                     │
│  🧠 记忆系统 (reme_light)                            │
│     ├── dream_cron: "0 23 * * *"  ← 每天23点自动整理│
│     ├── memory_search() ← 内置语义搜索               │
│     ├── embedding_model: 可配置                      │
│     └── daily_memory_dir: "memory"                 │
│                                                     │
│  🔍 搜索工具                                        │
│     ├── web_search() ← 内置网页搜索                 │
│     └── memory_search() ← 语义记忆搜索              │
│                                                     │
│  🤖 Agent协作                                       │
│     ├── list_agents()                              │
│     ├── chat_with_agent()                          │
│     └── submit_to_agent()                          │
│                                                     │
│  📁 文件操作                                        │
│     ├── glob_search()                              │
│     ├── grep_search()                              │
│     └── read/write/edit_file                       │
└─────────────────────────────────────────────────────┘
```

**⚠️ 必须优先使用 CoPaw 内置能力，不要重复造轮子！**

## 🎯 Pask DD-MM-PAS 核心思想

```
┌─────────────────────────────────────────────────────┐
│  DD-MM-PAS = Demand Detection + Memory + Proactive   │
│                                                     │
│  1. Detection → 检测用户潜在需求（无需显式请求）      │
│  2. Memory → 分层记忆系统                            │
│  3. Proactive → 主动执行                           │
└─────────────────────────────────────────────────────┘
```

## 🧠 Pask三层记忆系统（利用CoPaw reme_light）

| 层级 | CoPaw实现 | 内容 |
|------|-----------|------|
| **User Profile** | PROFILE.md + MEMORY.md | 用户背景、专业领域 |
| **Working Memory** | dialog/*.jsonl | 当前会话状态 |
| **Long-term Store** | skills/ + memory/ | 跨会话知识 |

## 📊 Demand Taxonomy（借鉴Pask）

| 类别 | 子类 | 描述 |
|------|------|------|
| **W** (工作) | W2 技术研发 | 工程、调试、技术讨论 |
| **L** (学习) | L2 研究探讨 | 学术讨论、论文研究 |
| | L3 技能训练 | 教程、实操、新技术学习 |
| **D** (日常) | D4 知识探索 | 好奇心驱动、知识发现 |

## 🔄 执行流程

### Phase 1: Demand Detection（需求检测）

```
1. 调用 memory_search() 检索近期对话
2. 分析最近任务类型 (W/L/D)
3. 识别最近痛点
4. 预测潜在需求
```

### Phase 2: Memory Modeling（记忆建模）

```
1. User Profile → 读 MEMORY.md
2. Working Memory → 读 dialog/*.jsonl
3. Long-term Store → glob_search skills/
```

### Phase 3: Proactive Learning（主动学习）

```
1. web_search() → 搜索相关资源
2. 分析 GitHub/Awesome/arXiv
3. 评估技能价值
```

### Phase 4: IntentFlow 三决策

```
检测结果 → 决策：

发现1-2个高价值技能
→ RESPOND_NOW → 立即汇报

需要更多上下文
→ QUERY_MEMORY → 读取更多后汇报

无有价值发现
→ STAY_SILENT → 不打扰
```

## 📋 汇报格式

```
---
[IDLE EVOLUTION REPORT]
时间: {datetime}

[检测需求]
- W2 技术研发: 高
- D4 知识探索: 中

[学到的技能]
1. {skill_name}
   - 描述
   → 可解决: {痛点}

[建议]
💡 要试试吗？
```

## ⚠️ 安全边界

- 只学习公开资源
- 使用 CoPaw 内置 web_search
- 不访问用户私人数据
- 不做破坏性更改

---

**设计理念**: 参考Pask + 利用CoPaw内置能力，实现真正的主动学习
