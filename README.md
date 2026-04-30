# QwenPaw Idle Evolution - 闲时进化系统

> CoPaw/QwenPaw 的智能闲时进化插件，当用户空闲时自动分析、学习和改进

## 🌟 特性

- **智能感知**：自动分析对话历史、纠正模式和用户痛点
- **主动学习**：在空闲时搜索 GitHub 寻找解决方案
- **技能进化**：自动创建和更新 Skills，减少重复错误
- **记忆同步**：将学习成果写入记忆文件
- **跨平台**：支持 Windows (Task Scheduler)、Linux (cron)

## 📁 文件结构

```
qwenpaw-idle-evolution/
├── idle_evolution.py    # 主程序
├── README.md            # 本文件
├── INSTALL.md           # 安装指南
├── CONFIG.md            # 配置说明
└── task_scheduler/      # Windows 任务计划脚本
    ├── create_task.bat
    └── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
# 无需额外依赖，仅使用 Python 标准库
```

### 2. 配置

复制并编辑配置文件：

```bash
# 设置环境变量
export COPAW_WORKSPACE=~/.copaw/workspaces/default
export IDLE_THRESHOLD_MINUTES=60
export IDLE_COOLDOWN=120

# 可选：GitHub Token（增加 API 速率限制）
export GITHUB_TOKEN=your_github_token
```

### 3. 运行

```bash
# 查看状态
python idle_evolution.py --status

# 手动运行
python idle_evolution.py --run

# 持续监控模式
python idle_evolution.py --monitor

# Windows 任务计划（推荐）
task_scheduler\create_task.bat
```

## 🎯 工作原理

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
生成进化报告 → 写入记忆 → 进入冷却期
```

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `IDLE_THRESHOLD_MINUTES` | 60 | 触发空闲阈值（分钟） |
| `IDLE_CHECK_INTERVAL` | 60 | 检查间隔（秒） |
| `IDLE_COOLDOWN` | 120 | 冷却期（分钟） |
| `COPAW_WORKSPACE` | `~/.copaw/...` | CoPaw 工作空间 |
| `GITHUB_TOKEN` | 空 | GitHub Token（可选） |

## 📊 输出

- **进化报告**: `idle_evolution_report.json`
- **状态文件**: `idle_state.json`
- **记忆更新**: 自动追加到 `MEMORY.md`

## 🔧 Windows 任务计划

创建每 10 分钟执行的任务：

```batch
schtasks /create /tn "QwenPawIdleEvolution" ^
    /tr "pythonw idle_evolution.py --run" ^
    /sc minute /mo 10 /f
```

## 📝 示例输出

```json
{
  "timestamp": "2026-05-01T00:00:00",
  "success": true,
  "summary": {
    "corrections_found": 15,
    "domains": ["代码开发", "工具使用"],
    "pain_points": ["不对", "太慢"],
    "recommendations_count": 5
  },
  "recommendations": [
    {
      "name": "cline/cline",
      "stars": 61220,
      "url": "https://github.com/cline/cline"
    }
  ]
}
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关项目

- [QwenPaw/CoPaw](https://github.com/agentscope-ai/QwenPaw) - 主项目
- [Pask DD-MM-PAS](https://github.com/xzf-thu/Pask) - 灵感来源
