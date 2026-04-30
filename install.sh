#!/bin/bash
# QwenPaw Idle Evolution 一键安装脚本
# Usage: 
#   curl -fsSL https://raw.githubusercontent.com/hlhjs/qwenpaw-idle-evolution/main/install.sh | bash
#   或: bash <(curl -fsSL https://raw.githubusercontent.com/hlhjs/qwenpaw-idle-evolution/main/install.sh)
#   或: git clone 后直接运行 ./install.sh

set -euo pipefail

# 配置
REPO_URL="https://github.com/hlhjs/qwenpaw-idle-evolution.git"
INSTALL_DIR="${HOME}/.copaw-awesome"
QWENPAW_DIR="${HOME}/.copaw/workspaces/default"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }
step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 检查 Python
check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        error "Python 未安装，请先安装 Python 3.8+"
        exit 1
    fi
    
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    info "Python 版本: $PYTHON_VERSION"
}

# 检查 pip
check_pip() {
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        warn "pip 未安装，尝试安装..."
        $PYTHON_CMD -m ensurepip --upgrade || $PYTHON_CMD -m pip install --upgrade pip
    fi
    info "pip 已就绪"
}

# 检查 CoPaw/QwenPaw
check_copaw() {
    if ! $PYTHON_CMD -c "import qwenpaw" &> /dev/null && ! $PYTHON_CMD -c "import copaw" &> /dev/null; then
        warn "CoPaw/QwenPaw 未安装，正在安装..."
        $PYTHON_CMD -m pip install qwenpaw
    fi
    info "CoPaw/QwenPaw 已就绪"
}

# 检查 git
check_git() {
    if ! command -v git &> /dev/null; then
        error "git 未安装，请先安装 git"
        exit 1
    fi
    info "git 已就绪"
}

# 克隆模板
clone_template() {
    if [ -d "$INSTALL_DIR" ]; then
        warn "模板已存在于 $INSTALL_DIR"
        read -p "是否更新？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$INSTALL_DIR" && git pull
            info "模板已更新"
        fi
    else
        info "正在克隆模板..."
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi
}

# 创建工作目录
init_workspace() {
    if [ ! -d "$QWENPAW_DIR" ]; then
        mkdir -p "$QWENPAW_DIR"
        info "工作目录已创建: $QWENPAW_DIR"
    else
        info "工作目录已存在: $QWENPAW_DIR"
    fi
}

# 复制模板文件
copy_templates() {
    step "复制模板文件..."
    
    # 复制配置模板
    if [ -f "$INSTALL_DIR/config/AGENTS.md.template" ]; then
        cp "$INSTALL_DIR/config/"*.template "$QWENPAW_DIR/" 2>/dev/null || true
        info "配置模板已复制"
    fi
    
    # 复制 Skills
    if [ -d "$INSTALL_DIR/skills" ]; then
        mkdir -p "$QWENPAW_DIR/skills"
        cp -r "$INSTALL_DIR/skills/"* "$QWENPAW_DIR/skills/" 2>/dev/null || true
        info "Skills 已复制"
    fi
    
    # 复制脚本
    if [ -d "$INSTALL_DIR/scripts" ]; then
        mkdir -p "$QWENPAW_DIR/scripts"
        cp -r "$INSTALL_DIR/scripts/"* "$QWENPAW_DIR/scripts/" 2>/dev/null || true
        info "脚本已复制"
    fi
    
    # 复制 docs
    if [ -d "$INSTALL_DIR/docs" ]; then
        mkdir -p "$QWENPAW_DIR/docs"
        cp -r "$INSTALL_DIR/docs/"* "$QWENPAW_DIR/docs/" 2>/dev/null || true
        info "文档已复制"
    fi
}

# 创建定时任务 (Linux/macOS)
create_cron() {
    echo
    read -p "是否创建定时任务？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        step "创建定时任务 (crontab)..."
        
        # 获取脚本路径
        SCRIPT_PATH="$QWENPAW_DIR/scripts/idle_evolution.py"
        
        # 添加 crontab 条目 (每10分钟)
        CRON_JOB="*/10 * * * * $PYTHON_CMD $SCRIPT_PATH --run >> ~/.idle_evolution.log 2>&1"
        
        # 检查是否已有条目
        if crontab -l 2>/dev/null | grep -q "idle_evolution.py"; then
            warn "定时任务已存在，跳过"
        else
            (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
            info "定时任务创建成功！"
            info "日志文件: ~/.idle_evolution.log"
        fi
    fi
}

# 主函数
main() {
    echo "========================================"
    echo "  QwenPaw Idle Evolution 一键安装"
    echo "========================================"
    echo
    
    check_python
    check_pip
    check_copaw
    check_git
    clone_template
    init_workspace
    copy_templates
    create_cron
    
    echo
    echo "========================================"
    echo -e "  ${GREEN}安装完成！${NC}"
    echo "========================================"
    echo
    echo "下一步："
    echo "  1. 编辑 $QWENPAW_DIR/agent.json 填入 API keys"
    echo "  2. 运行 'copaw' 启动"
    echo "  3. 运行 '$PYTHON_CMD $QWENPAW_DIR/scripts/idle_evolution.py --status' 查看状态"
    echo
}

main
