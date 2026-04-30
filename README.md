# 🎉 CoPaw Awesome Starter

> 一键启动你的 AI 个人助手，基于 QwenPaw/CoPaw 框架

**让任何人都能像使用模板一样，快速搭建自己的 AI 工作环境。**

---

## ✨ 特性

- 🧠 **智能记忆系统** - 自动整理会话记忆，学习你的习惯
- 🔌 **即插即用 Skills** - 整合多个顶级开源 Skills 项目
- 🔄 **空闲进化 (v2)** - 你空闲时自动分析纠正模式、识别痛点、搜索 GitHub 方案
- 📚 **科研工作流** - 文献调研→仿真验证→论文写作完整支持
- 🌐 **多渠道支持** - 微信、钉钉、QQ、Discord 等

---

## 🚀 快速开始

### 方式一：Windows 任务计划（推荐）

```batch
# 以管理员身份运行
scripts\task_scheduler\create_task.bat
```

### 方式二：手动运行

```bash
# 查看状态
python scripts/idle_evolution.py --status

# 手动触发进化
python scripts/idle_evolution.py --run

# 持续监控模式
python scripts/idle_evolution.py --monitor
```

### 方式三：克隆安装

```bash
# 1. 克隆模板
git clone https://github.com/hlhjs/qwenpaw-idle-evolution.git
cd qwenpaw-idle-evolution

# 2. 运行安装脚本
install.cmd  # Windows
./install.sh  # Linux/macOS

# 3. 启动 CoPaw
copaw
```

---

## 📁 项目结构

```
qwenpaw-idle-evolution/
├── README.md                    # 本文件
├── LICENSE                     # MIT 许可证
├── install.sh / install.cmd    # 一键安装脚本
├── scripts/
│   ├── idle_evolution.py      # 空闲进化服务 v2
│   ├── idle_evolution.py.bak  # 旧版本备份
│   └── task_scheduler/
│       └── create_task.bat     # Windows 任务计划创建
├── skills/                     # 核心 Skills
│   ├── autonomous-learner/     # 空闲进化
│   ├── spec-driven/           # 规格驱动开发
│   └── ...
├── config/                     # 配置模板
└── docs/                      # 详细文档
```

---

## 🧠 空闲进化 v2 工作原理

```
用户空闲 > 60分钟
    ↓
┌─────────────────────────────────────────────┐
│ 1. CorrectionAnalyzer - 分析纠正模式          │
│ 2. PainPointAnalyzer - 识别用户痛点          │
│ 3. SkillDiscoverer - GitHub 搜索方案        │
│ 4. SkillManager - 创建/更新 Skills          │
│ 5. MemoryUpdater - 更新记忆                  │
│ 6. CopawNotifier - 通知用户                 │
└─────────────────────────────────────────────┘
    ↓
生成进化报告 → 写入记忆 → 进入冷却期（120分钟）
```

### 配置参数

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `IDLE_THRESHOLD_MINUTES` | 60 | 触发阈值（分钟） |
| `IDLE_COOLDOWN` | 120 | 冷却期（分钟） |
| `COPAW_WORKSPACE` | `~/.copaw/...` | CoPaw 工作空间 |
| `GITHUB_TOKEN` | 空 | GitHub Token（可选） |

---

## 🛠️ 核心 Skills

| Skill | 来源 | 功能 |
|-------|------|------|
| **autonomous-learner** | 自创 | 空闲时自动学习并汇报 |
| **spec-driven-development** | agent-skills | 规格驱动开发 |
| **test-driven-development** | agent-skills | 测试驱动开发 |
| **brainstorming** | superpowers | 头脑风暴 |
| **grill-me** | mattpocock | 需求追问 |
| **diagnose** | mattpocock | 系统调试 |
| **chinaclaw** | 自创 | 科研流水线 |

---

## 📖 详细文档

- [空闲进化 RFC 提案](RFC_IDLE_EVOLUTION.md) - 功能设计和实现细节
- [安装指南](docs/INSTALL.md) - 详细安装步骤
- [配置说明](docs/CONFIG.md) - 环境变量配置

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

本项目整合了以下开源项目：

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [obra/superpowers](https://github.com/obra/superpowers)
- [xzf-thu/Pask](https://github.com/xzf-thu/Pask) - 灵感来源
