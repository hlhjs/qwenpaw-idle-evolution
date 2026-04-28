#!/bin/bash
# CoPaw Awesome Starter 一键安装脚本
# Usage: curl -fsSL https://your-domain.com/install.sh | bash
# 或: bash <(curl -fsSL https://your-domain.com/install.sh)

set -euo pipefail

# 配置
REPO_URL="https://github.com/YOUR_USERNAME/copaw-awesome-starter.git"
INSTALL_DIR="${HOME}/.copaw-awesome"
QWENPAW_DIR="${HOME}/.copaw/workspaces/default"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Python
check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        error "Python 未安装，请先安装 Python 3.10+"
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

# 检查 qwenpaw
check_qwenpaw() {
    if ! $PYTHON_CMD -c "import qwenpaw" &> /dev/null; then
        warn "QwenPaw 未安装，正在安装..."
        $PYTHON_CMD -m pip install qwenpaw
    fi
    info "QwenPaw 已就绪"
}

# 克隆模板
clone_template() {
    if [ -d "$INSTALL_DIR" ]; then
        warn "模板已存在于 $INSTALL_DIR，正在更新..."
        cd "$INSTALL_DIR" && git pull
    else
        info "正在克隆模板..."
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi
}

# 初始化 CoPaw
init_copaw() {
    info "正在初始化 CoPaw..."
    
    # 运行 copaw init (使用默认配置)
    if command -v copaw &> /dev/null; then
        copaw init --defaults --accept-security 2>/dev/null || true
    fi
}

# 复制模板文件
copy_templates() {
    info "正在复制模板文件..."
    
    # 复制配置模板
    if [ -f "$INSTALL_DIR/config/AGENTS.md.template" ]; then
        cp "$INSTALL_DIR/config/"*.template "$QWENPAW_DIR/" 2>/dev/null || true
        info "配置模板已复制"
    fi
    
    # 复制 Skills
    if [ -d "$INSTALL_DIR/skills" ]; then
        cp -r "$INSTALL_DIR/skills/"* "$QWENPAW_DIR/skills/" 2>/dev/null || true
        info "Skills 已复制"
    fi
    
    # 复制脚本
    if [ -d "$INSTALL_DIR/scripts" ]; then
        mkdir -p "$QWENPAW_DIR/scripts"
        cp -r "$INSTALL_DIR/scripts/"* "$QWENPAW_DIR/scripts/" 2>/dev/null || true
        info "脚本已复制"
    fi
}

# 主函数
main() {
    echo "========================================"
    echo "  CoPaw Awesome Starter 一键安装"
    echo "========================================"
    echo
    
    check_python
    check_pip
    check_qwenpaw
    clone_template
    init_copaw
    copy_templates
    
    echo
    echo "========================================"
    echo -e "${GREEN}  安装完成！${NC}"
    echo "========================================"
    echo
    echo "下一步："
    echo "  1. 编辑 $QWENPAW_DIR/agent.json 填入 API keys"
    echo "  2. 运行 'copaw' 启动"
    echo
}

main "$@"
