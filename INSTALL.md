# 安装指南

## 前置要求

- Python 3.8+
- CoPaw/QwenPaw 已安装
- Windows 或 Linux 系统

## 安装步骤

### 1. 下载/克隆

```bash
git clone https://github.com/hlhjs/qwenpaw-idle-evolution.git
cd qwenpaw-idle-evolution
```

### 2. 配置环境变量（推荐）

```bash
# Linux/macOS
export COPAW_WORKSPACE=~/.copaw/workspaces/default
export IDLE_THRESHOLD_MINUTES=60
export IDLE_COOLDOWN=120

# Windows PowerShell
$env:COPAW_WORKSPACE="$env:USERPROFILE\.copaw\workspaces\default"
$env:IDLE_THRESHOLD_MINUTES="60"
$env:IDLE_COOLDOWN="120"
```

### 3. Windows 任务计划（推荐）

运行脚本创建定时任务：

```batch
cd task_scheduler
create_task.bat
```

或手动创建：

```batch
schtasks /create /tn "QwenPawIdleEvolution" ^
    /tr "pythonw idle_evolution.py --run" ^
    /sc minute /mo 10 /f
```

### 4. 验证安装

```bash
python idle_evolution.py --status
```

预期输出：
```
[2026-05-01 00:00:00] 当前状态:
[2026-05-01 00:00:00]   最后活动: 未知
[2026-05-01 00:00:00]   上次进化: 从未
[2026-05-01 00:00:00]   进化次数: 0
[2026-05-01 00:00:00]   空闲状态: 否 (0分钟)
[2026-05-01 00:00:00]   可进化: 是
```

### 5. 测试运行

```bash
python idle_evolution.py --run
```

## 卸载

```batch
schtasks /delete /tn "QwenPawIdleEvolution" /f
```

## 故障排除

### 问题：任务计划执行失败

检查：
1. Python 路径是否正确
2. 工作目录是否存在
3. 日志文件权限

### 问题：GitHub API 限流

解决方案：
1. 设置 `GITHUB_TOKEN` 环境变量
2. 或等待限流恢复（通常 1 小时）

### 问题：无法读取文件

检查：
1. CoPaw 工作空间路径是否正确
2. 文件权限是否足够
