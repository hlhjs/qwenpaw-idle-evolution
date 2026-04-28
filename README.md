# 🎉 CoPaw Awesome Starter

> 一键启动你的 AI 个人助手，基于 QwenPaw 框架

**让任何人都能像使用模板一样，快速搭建自己的 AI 工作环境。**

---

## ✨ 特性

- 🧠 **智能记忆系统** - 自动整理会话记忆，学习你的习惯
- 🔌 **即插即用 Skills** - 整合多个顶级开源 Skills 项目
- 🔄 **空闲进化** - 你空闲时自动学习新技能并汇报
- 📚 **科研工作流** - 文献调研→仿真验证→论文写作完整支持
- 🌐 **多渠道支持** - 微信、钉钉、QQ、Discord 等

---

## 🚀 快速开始

### 一键安装

**Linux / macOS:**
```bash
curl -fsSL https://your-domain.com/install.sh | bash
```

**Windows:**
```batch
curl -fsSL https://your-domain.com/install.cmd | cmd
```

或者手动：

```bash
# 1. 安装 QwenPaw
pip install qwenpaw

# 2. 克隆本模板
git clone https://github.com/YOUR_USERNAME/copaw-awesome-starter.git
cd copaw-awesome-starter

# 3. 运行安装脚本
install.cmd  # Windows
./install.sh  # Linux/macOS

# 4. 配置 API keys
notepad ~/.copaw/workspaces/default/agent.json

# 5. 启动
copaw
```

---

## 📁 项目结构

```
copaw-awesome-starter/
├── README.md                    # 本文件
├── install.sh / install.cmd     # 一键安装脚本
├── LICENSE                     # 许可证
├── config/                     # 配置模板
│   ├── agent.json.template
│   ├── AGENTS.md.template
│   └── ...
├── skills/                     # 核心 Skills
│   ├── autonomous-learner/     # 空闲进化
│   ├── spec-driven/            # 规格驱动开发
│   └── ...
└── scripts/
    └── idle_evolution.py       # 空闲进化服务
```

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

## ⚙️ 配置说明

编辑 `~/.copaw/workspaces/default/agent.json`，填入你的 API keys：

```json
{
  "active_model": {
    "provider_id": "your-provider",
    "model": "your-model"
  }
}
```

### 启用 CoPaw 内置记忆系统

```json
{
  "memory_manager_backend": "remelight",
  "reme_light_memory_config": {
    "dream_cron": "0 23 * * *"
  }
}
```

---

## 📖 详细文档

- [Getting Started](docs/GETTING_STARTED.md) - 详细入门指南
- [Skills 使用指南](docs/SKILLS_GUIDE.md) - 各 Skill 的使用说明
- [科研工作流](docs/RESEARCH_WORKFLOW.md) - 如何做研究
- [空闲进化](docs/IDLE_EVOLUTION.md) - 自动学习机制

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

本项目整合了以下开源项目：

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [obra/superpowers](https://github.com/obra/superpowers)
- [xzf-thu/Pask](https://github.com/xzf-thu/Pask)
