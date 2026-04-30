"""
闲时进化系统 v2 - 彻底修复版
核心：从用户对话中感知需求 → 找方案 → 集成 → 减少纠正

功能：
1. 用户超过60分钟无活动时触发
2. 自动分析MEMORY.md、RULES.md和近期对话日志
3. 识别用户痛点和纠正模式
4. 主动搜索GitHub找解决方案
5. 创建或更新Skills
6. 将学习成果写入记忆文件
7. 输出结构化报告
"""
import json
import re
import sys
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import urllib.request
import urllib.error
import urllib.parse

# UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============== 配置 ==============
CONFIG = {
    "idle_threshold_minutes": 60,
    "check_interval_seconds": 60,
    "cooldown_minutes": 120,
    "max_topics": 10,
    "max_corrections": 20,
    "workspace": Path.home() / ".copaw" / "workspaces" / "default",
    "memory_file": Path.home() / ".copaw" / "workspaces" / "default" / "MEMORY.md",
    "rules_file": Path.home() / ".copaw" / "workspaces" / "default" / "RULES.md",
    "dialog_dir": Path.home() / ".copaw" / "workspaces" / "default" / "dialog",
    "skills_dir": Path.home() / ".copaw" / "workspaces" / "default" / "skills",
    "scholar_db": Path.home() / ".copaw" / "workspaces" / "default" / ".scholar_evolve.db",
    "report_file": Path.home() / ".copaw" / "workspaces" / "default" / "idle_evolution_report.json",
    "state_file": Path.home() / ".copaw" / "idle_state.json",
    "copaw_api": "http://127.0.0.1:8088",
}

# ============== 工具函数 ==============
def log(msg: str):
    """带时间戳的日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def read_file(path: Path) -> str:
    """安全读取文件"""
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        log(f"读取文件失败 {path}: {e}")
    return ""

def write_file(path: Path, content: str) -> bool:
    """安全写入文件"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        log(f"写入文件失败 {path}: {e}")
        return False

def http_get(url: str, timeout: int = 10) -> Optional[str]:
    """HTTP GET请求"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        log(f"HTTP GET 失败 {url}: {e}")
    return None

def http_post(url: str, data: dict, timeout: int = 30) -> Optional[dict]:
    """HTTP POST请求"""
    try:
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        log(f"HTTP POST 失败 {url}: {e}")
    return None

# ============== 核心分析模块 ==============
class CorrectionAnalyzer:
    """纠正模式分析器"""
    
    def __init__(self):
        self.keywords = [
            "不对", "不对吧", "错了", "不行", "没做到", "不是这样",
            "重来", "重新", "修改", "改进", "优化", "修复", "bug",
            "应该", "不应该", "要这样", "要那样", "按照我的",
            "不对，是", "你得", "你看看", "检查", "调试"
        ]
    
    def extract_corrections_from_db(self) -> List[Dict]:
        """从 SQLite 数据库提取纠正记录"""
        corrections = []
        try:
            if CONFIG['scholar_db'].exists():
                conn = sqlite3.connect(str(CONFIG['scholar_db']))
                cursor = conn.cursor()
                
                # 提取最近的纠正
                cursor.execute("""
                    SELECT id, correction_text, timestamp 
                    FROM corrections 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (CONFIG['max_corrections'],))
                
                for row in cursor.fetchall():
                    corrections.append({
                        "id": row[0],
                        "text": row[1][:200] if row[1] else "",
                        "timestamp": row[2]
                    })
                
                conn.close()
        except Exception as e:
            log(f"提取纠正失败: {e}")
        return corrections
    
    def extract_corrections_from_rules(self) -> List[Dict]:
        """从 RULES.md 提取纠正模式"""
        corrections = []
        content = read_file(CONFIG['rules_file'])
        
        # 提取 Rule added 行
        pattern = r'## Rule added: (.+?)\n(.+?)(?=\n##|\Z)'
        for match in re.finditer(pattern, content, re.DOTALL):
            timestamp = match.group(1).strip()
            rule_content = match.group(2).strip()
            
            # 提取触发条件
            trigger_match = re.search(r'\*\*触发条件\*\*:\s*(.+)', rule_content)
            trigger = trigger_match.group(1).strip() if trigger_match else ""
            
            # 提取典型纠正
            example_match = re.search(r'\*\*典型纠正\*\*:\s*(.+)', rule_content)
            example = example_match.group(1).strip() if example_match else ""
            
            corrections.append({
                "timestamp": timestamp,
                "trigger": trigger,
                "example": example,
                "full_rule": rule_content[:300]
            })
        
        return corrections[:CONFIG['max_corrections']]

class PainPointAnalyzer:
    """用户痛点分析器"""
    
    def __init__(self):
        self.domain_keywords = {
            "AO仿真": ["AO", "自适应光学", "HCIPy", "OOMAO", "闭环", "Strehl", "Zernike", "波前", "WFS", "变形镜", "Shack-Hartmann"],
            "仿真算法": ["仿真", "Monte Carlo", "相位屏", "湍流", "Kolmogorov", "Von Karman", "SPGD", "PD算法"],
            "论文写作": ["论文", "Pipeline", "文献", "综述", "abstract", "引言", "chinaclaw"],
            "代码开发": ["代码", "Python", "实现", "bug", "调试", "优化", "重构", "opencode"],
            "工具使用": ["skill", "配置", "安装", "集成", "MCP", "CoPaw"]
        }
    
    def analyze_dialog_history(self) -> Dict:
        """分析对话历史，识别痛点"""
        result = {
            "domains": [],
            "topics": [],
            "frustrations": [],
            "recent_questions": []
        }
        
        try:
            # 读取 CoPaw 对话日志
            if CONFIG['dialog_dir'].exists():
                dialog_files = sorted(
                    CONFIG['dialog_dir'].glob("*.jsonl"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True
                )
                
                for df in dialog_files[:5]:  # 最近5个文件
                    content = read_file(df)
                    lines = content.split('\n')
                    
                    # 分析每行 JSON
                    for line in lines[-500:]:  # 每个文件最后500行
                        try:
                            obj = json.loads(line.strip())
                            text = json.dumps(obj, ensure_ascii=False)
                            
                            # 识别领域
                            for domain, keywords in self.domain_keywords.items():
                                if any(kw in text for kw in keywords):
                                    if domain not in result['domains']:
                                        result['domains'].append(domain)
                            
                            # 识别痛点关键词
                            frustration_kws = ["不对", "不行", "错了", "没做到", "不会", "做不到", "太慢", "没反应"]
                            for kw in frustration_kws:
                                if kw in text and kw not in result['frustrations']:
                                    result['frustrations'].append(kw)
                            
                            # 识别问题
                            if any(q in text for q in ["怎么", "如何", "为什么", "是什么", "?"]):
                                # 提取问题句子
                                for sent in text.split('。'):
                                    if any(q in sent for q in ["怎么", "如何", "为什么", "是什么"]) and len(sent) > 5:
                                        result['recent_questions'].append(sent[:100])
                                        break
                        except:
                            pass
        except Exception as e:
            log(f"分析对话历史失败: {e}")
        
        # 限制数量
        result['recent_questions'] = result['recent_questions'][:10]
        result['frustrations'] = result['frustrations'][:10]
        
        return result

class SkillDiscoverer:
    """技能发现器 - 主动搜索GitHub找解决方案"""
    
    def __init__(self):
        self.github_api = "https://api.github.com"
    
    def search_github(self, query: str, per_page: int = 5) -> List[Dict]:
        """搜索GitHub"""
        url = f"{self.github_api}/search/repositories?q={urllib.parse.quote(query)}&per_page={per_page}&sort=stars"
        result = http_get(url)
        
        repos = []
        if result:
            try:
                data = json.loads(result)
                for item in data.get('items', []):
                    repos.append({
                        "name": item.get('full_name', ''),
                        "description": item.get('description', ''),
                        "stars": item.get('stargazers_count', 0),
                        "url": item.get('html_url', ''),
                        "language": item.get('language', ''),
                    })
            except Exception as e:
                log(f"解析GitHub结果失败: {e}")
        
        return repos
    
    def recommend_skills(self, domains: List[str], pain_points: List[str]) -> List[Dict]:
        """基于痛点推荐技能/工具"""
        recommendations = []
        
        # 域名到搜索关键词的映射
        domain_searches = {
            "AO仿真": ["HCIPy AO simulation", "Soapy adaptive optics", "OOMAO"],
            "论文写作": ["GPT research paper", "AI literature review", "paper pipeline"],
            "代码开发": ["AI code review", "autonomous coding agent", "self-improving AI"],
            "工具使用": ["AI agent skill management", "agent skills framework"],
        }
        
        # 痛点到搜索关键词的映射
        pain_searches = {
            "不对": ["AI code correction", "self-healing code"],
            "太慢": ["AI performance optimization", "fast AI inference"],
            "不会": ["AI learning tutorial", "beginner AI coding"],
            "错了": ["AI debugging", "error correction AI"],
            "不行": ["AI alternative tools", "AI replacement"],
        }
        
        # 搜索领域相关
        for domain in domains:
            if domain in domain_searches:
                for query in domain_searches[domain]:
                    repos = self.search_github(query)
                    recommendations.extend(repos)
        
        # 搜索痛点相关
        for pain in pain_points:
            if pain in pain_searches:
                for query in pain_searches[pain]:
                    repos = self.search_github(query)
                    recommendations.extend(repos)
        
        # 去重
        seen = set()
        unique = []
        for r in recommendations:
            if r['name'] not in seen:
                seen.add(r['name'])
                unique.append(r)
        
        return sorted(unique, key=lambda x: x['stars'], reverse=True)[:10]

class SkillManager:
    """技能管理器 - 创建和更新Skills"""
    
    def __init__(self):
        self.skills_dir = CONFIG['skills_dir']
        self.skills_dir.mkdir(parents=True, exist_ok=True)
    
    def create_skill(self, name: str, description: str = "", content: str = "") -> bool:
        """创建新Skill"""
        skill_dir = self.skills_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            log(f"Skill 已存在: {name}")
            return False
        
        # 如果没有提供内容，生成默认模板
        if not content:
            content = f"""# {name}

{description if description else "自动生成的Skill"}

## 功能
- 

## 使用方法
```

## 触发条件
当用户说"..."时调用
```

## 作者
自动生成 - {datetime.now().strftime('%Y-%m-%d')}
"""
        
        return write_file(skill_file, content)
    
    def update_skill(self, name: str, content: str) -> bool:
        """更新Skill"""
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return self.create_skill(name, "", content)
        
        return write_file(skill_file, content)
    
    def list_skills(self) -> List[str]:
        """列出所有Skills"""
        if not self.skills_dir.exists():
            return []
        return [d.name for d in self.skills_dir.iterdir() if d.is_dir()]

class MemoryUpdater:
    """记忆更新器"""
    
    def __init__(self):
        self.memory_file = CONFIG['memory_file']
    
    def append_evolution_log(self, log_entry: str) -> bool:
        """追加进化日志到记忆文件"""
        content = read_file(self.memory_file)
        
        MARKER = "## 🧠 进化日志"
        
        # 检查是否已有 Evolution Log 章节
        if MARKER in content:
            # 追加到现有章节：在章节末尾的 --- 之后插入
            idx = content.find(MARKER)
            insert_pos = content.find("\n---\n", idx)
            if insert_pos == -1:
                # 找不到分隔符，在下一个 ## 之前插入
                next_section = content.find("\n## ", idx + len(MARKER))
                if next_section == -1:
                    insert_pos = len(content)
                else:
                    insert_pos = next_section
            else:
                # 在 --- 之后插入（跳过 --- 本身）
                insert_pos = insert_pos + len("\n---\n")
            
            new_content = content[:insert_pos] + f"{log_entry}\n\n---\n" + content[insert_pos:]
        else:
            # 添加新章节
            new_content = content + f"\n\n{MARKER}\n{log_entry}\n---\n"
        
        return write_file(self.memory_file, new_content)
    
    def get_last_evolution_time(self) -> Optional[datetime]:
        """获取上次进化时间"""
        content = read_file(self.memory_file)
        
        # 查找最新日志
        pattern = r'\[SELF-EVOLUTION\]\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
        matches = re.findall(pattern, content)
        
        if matches:
            try:
                return datetime.strptime(matches[-1], "%Y-%m-%d %H:%M:%S")
            except:
                pass
        return None

# ============== 状态管理 ==============
class StateManager:
    """状态管理器"""
    
    def __init__(self):
        self.state_file = CONFIG['state_file']
    
    def load(self) -> Dict:
        """加载状态"""
        content = read_file(self.state_file)
        if content:
            try:
                return json.loads(content)
            except:
                pass
        return {
            "last_activity": datetime.now().isoformat(),
            "last_evolution": None,
            "evolution_count": 0,
            "total_idle_minutes": 0
        }
    
    def save(self, state: Dict) -> bool:
        """保存状态"""
        return write_file(self.state_file, json.dumps(state, indent=2, ensure_ascii=False))
    
    def update_activity(self):
        """更新最后活动时间"""
        state = self.load()
        state["last_activity"] = datetime.now().isoformat()
        self.save(state)
    
    def check_idle(self) -> Tuple[bool, int]:
        """检查是否空闲，返回 (是否空闲, 空闲分钟数)"""
        state = self.load()
        try:
            last = datetime.fromisoformat(state["last_activity"])
            idle_minutes = (datetime.now() - last).total_seconds() / 60
            return idle_minutes >= CONFIG['idle_threshold_minutes'], int(idle_minutes)
        except:
            return False, 0
    
    def can_evolve(self) -> bool:
        """检查是否可以进化（有冷却期）"""
        state = self.load()
        if not state.get("last_evolution"):
            return True
        
        try:
            last = datetime.fromisoformat(state["last_evolution"])
            cooldown_minutes = (datetime.now() - last).total_seconds() / 60
            return cooldown_minutes >= CONFIG['cooldown_minutes']
        except:
            return True
    
    def record_evolution(self):
        """记录进化"""
        state = self.load()
        state["last_evolution"] = datetime.now().isoformat()
        state["evolution_count"] = state.get("evolution_count", 0) + 1
        self.save(state)

# ============== CoPaw 交互 ==============
class CopawNotifier:
    """CoPaw 通知器"""
    
    def send_notification(self, title: str, content: str) -> bool:
        """发送通知到 CoPaw"""
        payload = {
            "type": "text",
            "content": f"**{title}**\n\n{content}"
        }
        result = http_post(f"{CONFIG['copaw_api']}/api/notifications", payload)
        return result is not None
    
    def check_copaw_status(self) -> bool:
        """检查 CoPaw 是否运行"""
        return http_get(f"{CONFIG['copaw_api']}/api/status") is not None

# ============== 主执行器 ==============
class IdleEvolutionExecutor:
    """闲时进化执行器"""
    
    def __init__(self):
        self.correction_analyzer = CorrectionAnalyzer()
        self.pain_point_analyzer = PainPointAnalyzer()
        self.skill_discoverer = SkillDiscoverer()
        self.skill_manager = SkillManager()
        self.memory_updater = MemoryUpdater()
        self.state_manager = StateManager()
        self.notifier = CopawNotifier()
    
    def run_full_evolution(self) -> Dict:
        """执行完整进化流程"""
        log("=" * 50)
        log("开始闲时进化分析...")
        log("=" * 50)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "steps": [],
            "corrections_found": 0,
            "domains_detected": [],
            "pain_points": [],
            "skill_recommendations": [],
            "skills_created": [],
            "errors": []
        }
        
        try:
            # Step 1: 分析纠正模式
            log("[1/6] 分析纠正模式...")
            corrections_db = self.correction_analyzer.extract_corrections_from_db()
            corrections_rules = self.correction_analyzer.extract_corrections_from_rules()
            result["corrections_found"] = len(corrections_db) + len(corrections_rules)
            result["steps"].append(f"发现 {result['corrections_found']} 条纠正记录")
            log(f"  - 从数据库: {len(corrections_db)} 条")
            log(f"  - 从RULES.md: {len(corrections_rules)} 条")
            
            # Step 2: 分析痛点
            log("[2/6] 分析用户痛点...")
            pain_points = self.pain_point_analyzer.analyze_dialog_history()
            result["domains_detected"] = pain_points['domains']
            result["pain_points"] = pain_points['frustrations']
            result["steps"].append(f"检测领域: {', '.join(pain_points['domains'])}")
            log(f"  - 领域: {pain_points['domains']}")
            log(f"  - 痛点: {pain_points['frustrations']}")
            
            # Step 3: 搜索GitHub找解决方案
            log("[3/6] 搜索GitHub解决方案...")
            recommendations = self.skill_discoverer.recommend_skills(
                pain_points['domains'],
                pain_points['frustrations']
            )
            result["skill_recommendations"] = recommendations[:5]
            result["steps"].append(f"找到 {len(recommendations)} 个推荐项目")
            for r in recommendations[:3]:
                log(f"  - {r['name']} ({r['stars']} stars)")
            
            # Step 4: 检查现有Skills
            log("[4/6] 检查现有Skills...")
            existing_skills = self.skill_manager.list_skills()
            result["steps"].append(f"现有 Skills: {len(existing_skills)} 个")
            log(f"  - {len(existing_skills)} 个Skills")
            
            # Step 5: 生成进化报告
            log("[5/6] 生成进化报告...")
            report = self._generate_report(result, corrections_rules, recommendations, pain_points)
            
            # 保存报告
            write_file(CONFIG['report_file'], json.dumps(report, indent=2, ensure_ascii=False))
            
            # Step 6: 更新记忆
            log("[6/6] 更新记忆...")
            memory_log = f"""[SELF-EVOLUTION] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
检测到领域: {', '.join(pain_points['domains']) if pain_points['domains'] else '无'}
发现纠正: {result['corrections_found']} 条
推荐项目: {len(recommendations)} 个
推荐Top3: {', '.join([r['name'] for r in recommendations[:3]])}
"""
            self.memory_updater.append_evolution_log(memory_log)
            result["steps"].append("记忆已更新")
            
            # 通知 CoPaw
            if self.notifier.check_copaw_status():
                self.notifier.send_notification(
                    "🧠 闲时进化完成",
                    f"发现 {result['corrections_found']} 条纠正\n"
                    f"检测到 {len(pain_points['domains'])} 个领域\n"
                    f"推荐 {len(recommendations)} 个GitHub项目"
                )
            
            result["success"] = True
            result["report_path"] = str(CONFIG['report_file'])
            
            log("✅ 闲时进化完成！")
            
        except Exception as e:
            error_msg = f"错误: {e}"
            log(error_msg)
            result["errors"].append(error_msg)
        
        return result
    
    def _generate_report(self, result: Dict, corrections: List, recommendations: List, pain_points: Dict) -> Dict:
        """生成结构化报告"""
        return {
            "timestamp": result["timestamp"],
            "summary": {
                "corrections_found": result["corrections_found"],
                "domains": result["domains_detected"],
                "pain_points": result["pain_points"],
                "recommendations_count": len(recommendations)
            },
            "corrections": corrections[:5],
            "recommendations": [
                {
                    "name": r["name"],
                    "description": r["description"],
                    "stars": r["stars"],
                    "url": r["url"]
                }
                for r in recommendations[:5]
            ],
            "pain_points": pain_points,
            "action_items": self._generate_action_items(result, recommendations)
        }
    
    def _generate_action_items(self, result: Dict, recommendations: List) -> List[str]:
        """生成行动项"""
        items = []
        
        if result["corrections_found"] > 10:
            items.append("⚠️ 纠正次数较多，建议分析纠正模式并创建专门的纠正恢复Skill")
        
        if "AO仿真" in result["domains_detected"]:
            items.append("🔬 检测到AO仿真需求，可考虑集成 HCIPy/MAP-Elites 优化能力")
        
        if "代码开发" in result["domains_detected"]:
            items.append("💻 检测到代码开发需求，可考虑集成代码评审Skill")
        
        if len(recommendations) > 0:
            top_repo = recommendations[0]
            items.append(f"📦 推荐关注: {top_repo['name']} ({top_repo['stars']} stars)")
        
        return items

# ============== 命令行接口 ==============
def main():
    import argparse
    parser = argparse.ArgumentParser(description="闲时进化系统 v2")
    parser.add_argument("--check", action="store_true", help="检查是否空闲")
    parser.add_argument("--run", action="store_true", help="强制运行进化")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--monitor", action="store_true", help="持续监控模式")
    args = parser.parse_args()
    
    executor = IdleEvolutionExecutor()
    
    if args.status:
        state = executor.state_manager.load()
        log("当前状态:")
        log(f"  最后活动: {state.get('last_activity', '未知')}")
        log(f"  上次进化: {state.get('last_evolution', '从未')}")
        log(f"  进化次数: {state.get('evolution_count', 0)}")
        
        is_idle, idle_minutes = executor.state_manager.check_idle()
        log(f"  空闲状态: {'是' if is_idle else '否'} ({idle_minutes}分钟)")
        
        can = executor.state_manager.can_evolve()
        log(f"  可进化: {'是' if can else '否'}")
    
    elif args.check:
        is_idle, idle_minutes = executor.state_manager.check_idle()
        if is_idle:
            log(f"用户空闲超过 {idle_minutes} 分钟")
        else:
            log(f"用户空闲 {idle_minutes} 分钟，尚未达到阈值")
    
    elif args.run:
        result = executor.run_full_evolution()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 记录进化
        if result.get("success"):
            executor.state_manager.record_evolution()
            log("✅ 进化状态已记录")
    
    elif args.monitor:
        log("启动持续监控模式 (Ctrl+C 退出)...")
        while True:
            is_idle, idle_minutes = executor.state_manager.check_idle()
            
            if is_idle and executor.state_manager.can_evolve():
                log(f"触发闲时进化 (空闲 {idle_minutes} 分钟)...")
                executor.run_full_evolution()
                executor.state_manager.record_evolution()
            else:
                if not is_idle:
                    log(f"用户活跃中...")
                else:
                    log(f"冷却期内，跳过...")
            
            time.sleep(CONFIG["check_interval_seconds"])
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
