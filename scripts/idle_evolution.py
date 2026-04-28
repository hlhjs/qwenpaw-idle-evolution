"""
CoPaw 空闲进化服务
当用户空闲超过指定时间后，自动学习新技能并汇报
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
IDLE_THRESHOLD_MINUTES = 60  # 空闲阈值（分钟）
CHECK_INTERVAL_SECONDS = 300  # 检查间隔（5分钟）
STATE_FILE = Path(__file__).parent / "idle_state.json"
LOG_FILE = Path(__file__).parent / "idle_evolution.log"

def get_idle_time_windows():
    """Windows获取idle时间"""
    try:
        # 使用 PowerShell 获取系统空闲时间（毫秒）
        cmd = '''powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SystemInformation]::UserIdleTime.TotalMinutes"'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        idle_minutes = int(result.stdout.strip())
        return idle_minutes
    except Exception as e:
        print(f"获取idle时间失败: {e}")
        return 0

def load_state():
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_activity": datetime.now().isoformat(),
        "last_evolution": None,
        "evolution_count": 0
    }

def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def log(msg):
    """日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def should_evolve(state):
    """判断是否应该进化"""
    if state.get("last_evolution") is None:
        return True
    
    last_evolution = datetime.fromisoformat(state["last_evolution"])
    hours_since = (datetime.now() - last_evolution).total_seconds() / 3600
    
    # 每天最多进化一次
    return hours_since >= 24

def trigger_evolution():
    """触发进化（通过调用CoPaw API）"""
    log("触发空闲进化...")
    
    try:
        # 调用 CoPaw API 触发进化
        import requests
        response = requests.post(
            "http://127.0.0.1:8088/api/agents/default/chat",
            json={
                "message": "执行 autonomous-learner skill 进行空闲进化分析",
                "skill": "autonomous-learner"
            },
            timeout=60
        )
        log(f"进化请求已发送，状态码: {response.status_code}")
    except Exception as e:
        log(f"触发进化失败: {e}")
        log("提示: 确保 CoPaw 正在运行")

def main():
    """主循环"""
    print("=" * 50)
    print("  CoPaw 空闲进化服务")
    print(f"  空闲阈值: {IDLE_THRESHOLD_MINUTES} 分钟")
    print(f"  检查间隔: {CHECK_INTERVAL_SECONDS} 秒")
    print("=" * 50)
    print()
    
    state = load_state()
    log("服务启动")
    
    while True:
        try:
            idle_minutes = get_idle_time_windows()
            log(f"当前空闲时间: {idle_minutes} 分钟")
            
            if idle_minutes >= IDLE_THRESHOLD_MINUTES:
                if should_evolve(state):
                    log(f"超过 {IDLE_THRESHOLD_MINUTES} 分钟空闲，开始进化")
                    trigger_evolution()
                    
                    state["last_evolution"] = datetime.now().isoformat()
                    state["evolution_count"] = state.get("evolution_count", 0) + 1
                    save_state(state)
                else:
                    log("今日已进化，跳过")
            else:
                remaining = IDLE_THRESHOLD_MINUTES - idle_minutes
                log(f"还需 {remaining:.0f} 分钟达到阈值")
            
            time.sleep(CHECK_INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            log("服务已停止")
            break
        except Exception as e:
            log(f"错误: {e}")
            time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
