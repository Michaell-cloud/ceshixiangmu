#!/usr/bin/env bash
# 下载 PanoWorld 模型权重
# 用法: bash download_models.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL_DIR="$SCRIPT_DIR/model_ckpt"

echo "========================================"
echo "⬇️  下载 PanoWorld 模型权重"
echo "========================================"

mkdir -p "$MODEL_DIR"
cd "$MODEL_DIR"

echo ""
echo "📦 下载 1024x512 模型 (~2.4GB)..."
if [ ! -f "ckpt_panoworld_lrm_1024_512.pt" ]; then
    wget -c --show-progress \
        "https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_1024_512.pt" \
        -O ckpt_panoworld_lrm_1024_512.pt
    echo "✅ 1024x512 模型下载完成"
else
    echo "✅ 1024x512 模型已存在，跳过下载"
fi

echo ""
echo "📦 下载 2048x1024 模型 (~2.4GB)..."
echo "   (取消下方注释以启用)"
# if [ ! -f "ckpt_panoworld_lrm_2048_1024.ckpt" ]; then
#     wget -c --show-progress \
#         "https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_2048_1024.ckpt" \
#         -O ckpt_panoworld_lrm_2048_1024.ckpt
#     echo "✅ 2048x1024 模型下载完成"
# else
#     echo "✅ 2048x1024 模型已存在，跳过下载"
# fi

echo ""
echo "========================================"
echo "✅ 模型下载完成"
echo "========================================"
echo ""
ls -lh "$MODEL_DIR"
