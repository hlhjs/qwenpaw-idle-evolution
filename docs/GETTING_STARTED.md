# 🚀 快速入门

## 环境要求

- Python 3.10+
- Windows / Linux / macOS
- API Key（MiniMax / OpenAI 等）

---

## 第一步：安装 QwenPaw

```bash
pip install qwenpaw
```

---

## 第二步：克隆本项目

```bash
git clone https://github.com/YOUR_USERNAME/copaw-awesome-starter.git
cd copaw-awesome-starter
```

---

## 第三步：安装

**Windows:**
```batch
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

---

## 第四步：配置

### 1. 复制配置文件

```bash
cp config/agent.json.template ~/.copaw/workspaces/default/agent.json
```

### 2. 编辑配置

```bash
# 编辑 agent.json，填入你的 API keys
notepad ~/.copaw/workspaces/default/agent.json
```

关键配置项：

```json
{
  "active_model": {
    "provider_id": "minimax-cn",
    "model": "MiniMax-M2"
  }
}
```

### 3. 复制 Skills 和配置模板

```bash
# 复制 Skills
cp -r skills/* ~/.copaw/workspaces/default/skills/

# 复制配置模板
cp config/*.md.template ~/.copaw/workspaces/default/
```

---

## 第五步：启动

```bash
copaw
```

看到以下输出说明成功：

```
[CoPaw] 正在启动...
[CoPaw] 加载 Skills...
[CoPaw] 已就绪 ✓
```

---

## 第六步：测试

输入 `help` 查看可用命令：

```
> help
```

输入一个简单任务测试：

```
> 你好，介绍一下你自己
```

---

## 🔧 常见问题

### Q: 提示 "command not found: copaw"

```bash
# 确保 Python Scripts 在 PATH 中
pip install qwenpaw --force-reinstall
```

### Q: API Key 无效

检查 `agent.json` 中的 `provider_id` 和 `model` 是否正确。

### Q: Skills 不工作

```bash
# 重新扫描 Skills
cd ~/.copaw
python enable_skills.py
```

---

## 下一步

- 查看 [Skills 使用指南](SKILLS_GUIDE.md)
- 查看 [科研工作流](RESEARCH_WORKFLOW.md)
- 查看 [空闲进化](IDLE_EVOLUTION.md)
