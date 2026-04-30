# 🚀 快速开始

## 方式一：一键安装（推荐）

### Windows
```batch
# 方法1: PowerShell 一行命令
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hlhjs/qwenpaw-idle-evolution/main/install.cmd' -OutFile '$env:TEMP\qwenpaw_install.cmd'; Start-Process '$env:TEMP\qwenpaw_install.cmd' -Wait"

# 方法2: 克隆后运行
git clone https://github.com/hlhjs/qwenpaw-idle-evolution.git
cd qwenpaw-idle-evolution
install.cmd
```

### Linux / macOS
```bash
# 一行命令
curl -fsSL https://raw.githubusercontent.com/hlhjs/qwenpaw-idle-evolution/main/install.sh | bash

# 或克隆后运行
git clone https://github.com/hlhjs/qwenpaw-idle-evolution.git
cd qwenpaw-idle-evolution
chmod +x install.sh
./install.sh
```

---

## 方式二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/hlhjs/qwenpaw-idle-evolution.git ~/.copaw-awesome

# 2. 复制到 CoPaw 工作目录
cp -r ~/.copaw-awesome/skills ~/.copaw/workspaces/default/
cp -r ~/.copaw-awesome/scripts ~/.copaw/workspaces/default/

# 3. 配置 API keys
# 编辑 ~/.copaw/workspaces/default/agent.json
```

---

## 方式三：仅安装空闲进化脚本

```bash
# 直接下载脚本
wget https://raw.githubusercontent.com/hlhjs/qwenpaw-idle-evolution/main/scripts/idle_evolution.py
python idle_evolution.py --status
```

---

## 配置 API Keys

安装后需要配置你的 AI API keys：

```json
// ~/.copaw/workspaces/default/agent.json
{
  "active_model": {
    "provider_id": "openai",  // 或 minimax, deepseek 等
    "model": "gpt-4"          // 或 gpt-3.5-turbo, deepseek-chat 等
  }
}
```

对于 MiniMax:
```json
{
  "provider_api_keys": {
    "MINIMAX_API_KEY": "your-minimax-key"
  }
}
```

---

## 使用

```bash
# 查看状态
python ~/.copaw/workspaces/default/scripts/idle_evolution.py --status

# 手动触发一次
python ~/.copaw/workspaces/default/scripts/idle_evolution.py --run

# 设置定时任务
# Windows: scripts/task_scheduler/create_task.bat
# Linux: crontab -e 添加 */10 * * * * python /path/to/idle_evolution.py --run
```

---

## 环境变量（可选）

```bash
# CoPaw 工作目录
export COPAW_WORKSPACE=~/.copaw/workspaces/default

# 空闲阈值（分钟）
export IDLE_THRESHOLD_MINUTES=60

# 冷却期（分钟）
export IDLE_COOLDOWN=120

# GitHub Token（增加 API 限制）
export GITHUB_TOKEN=your_github_token
```

---

## 常见问题

### Q: 安装后无法运行？
A: 确保 Python 版本 >= 3.8，CoPaw 已安装

### Q: GitHub API 限流？
A: 设置 GITHUB_TOKEN 环境变量，或等待限流恢复

### Q: 如何卸载？
```bash
# Windows
schtasks /delete /tn "QwenPawIdleEvolution" /f

# Linux
crontab -e  # 删除相关行
```

---

更多信息请查看 [README.md](README.md)
