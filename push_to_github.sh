#!/usr/bin/env bash
# ============================================================
# PanoWorld GitHub 推送脚本
# 用法:
#   1. 修改下方 GITHUB_USER 和 GITHUB_REPO
#   2. bash push_to_github.sh
# ============================================================

set -euo pipefail

# ========== 请修改以下配置 ==========
GITHUB_USER="YOUR_USERNAME"      # 替换为你的 GitHub 用户名
GITHUB_REPO="PanoWorld"          # 替换为你的仓库名
# ====================================

REMOTE_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

echo "========================================"
echo "🚀 推送到 GitHub"
echo "========================================"
echo ""
echo "仓库: ${REMOTE_URL}"
echo ""

# 检查配置
if [ "${GITHUB_USER}" = "YOUR_USERNAME" ]; then
    echo "❌ 错误: 请先编辑此脚本，将 GITHUB_USER 改为你的 GitHub 用户名"
    exit 1
fi

# 设置 Git 用户信息（如未设置）
if [ -z "$(git config user.name 2>/dev/null)" ]; then
    echo "📧 设置 Git 用户名..."
    git config user.name "PanoWorld Developer"
fi
if [ -z "$(git config user.email 2>/dev/null)" ]; then
    echo "📧 设置 Git 邮箱..."
    git config user.email "dev@example.com"
fi

# 检查远程仓库
cd "$(dirname "$0")"

if git remote | grep -q "origin"; then
    echo "📝 更新远程仓库地址..."
    git remote set-url origin "${REMOTE_URL}"
else
    echo "📝 添加远程仓库..."
    git remote add origin "${REMOTE_URL}"
fi

echo ""
echo "📤 开始推送..."
git branch -M main 2>/dev/null || true
git push -u origin main

echo ""
echo "========================================"
echo "✅ 推送完成！"
echo "========================================"
echo ""
echo "仓库地址: ${REMOTE_URL}"
echo ""
echo "下一步:"
echo "  1. 打开 ${REMOTE_URL}"
echo "  2. 复制仓库地址到 Colab Notebook 的 GITHUB_REPO 变量"
echo "  3. 在 Colab 中运行推理"
