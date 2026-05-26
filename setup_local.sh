#!/usr/bin/env bash
# PanoWorld 本地环境一键设置脚本
# 用法: bash setup_local.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
CODE_DIR="$PROJECT_ROOT/PanoWorld"

echo "========================================"
echo "🚀 PanoWorld 本地环境设置"
echo "========================================"

# 1. 检查 Python 3.10
if command -v python3.10 &> /dev/null; then
    PYTHON="python3.10"
elif command -v python3 &> /dev/null && python3 --version 2>&1 | grep -q "3.10"; then
    PYTHON="python3"
else
    echo "❌ 未找到 Python 3.10"
    echo "   macOS 用户运行: brew install python@3.10"
    echo "   其他用户请访问: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python: $PYTHON ($($PYTHON --version))"

# 2. 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 创建虚拟环境..."
    $PYTHON -m venv "$VENV_DIR"
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
fi

# 3. 激活虚拟环境并安装依赖
echo "📦 安装依赖..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip

# 安装 CPU 版 PyTorch（本地无需 GPU）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 安装项目依赖
cd "$CODE_DIR"
pip install -r requirements.txt
pip install omegaconf

echo ""
echo "========================================"
echo "✅ 本地环境设置完成！"
echo "========================================"
echo ""
echo "📌 激活虚拟环境:"
echo "   source venv/bin/activate"
echo ""
echo "📌 进入项目目录:"
echo "   cd PanoWorld"
echo ""
echo "📌 本地运行（仅 CPU 调试，GPU 请用 Colab）:"
echo "   python inference.py --config configs/local_inference_1024_512.yaml"
echo ""
echo "📌 生成 Colab Notebook:"
echo "   python ../sync_to_colab.py"
