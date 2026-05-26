#!/usr/bin/env python3
"""
PanoWorld 本地 ↔ Colab 同步脚本

功能：
1. 检查本地项目环境
2. 生成 Colab 专用 Notebook（自动填充本地配置）
3. 提供 Google Drive 同步指引

用法：
    python sync_to_colab.py
"""

import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PANOWORLD_DIR = os.path.join(PROJECT_ROOT, "PanoWorld")

def check_environment():
    """检查本地环境配置"""
    print("=" * 60)
    print("🔍 PanoWorld 本地环境检查")
    print("=" * 60)

    # Python 版本
    import platform
    py_version = platform.python_version()
    print(f"\n📌 Python 版本: {py_version}")
    if py_version.startswith("3.10"):
        print("   ✅ Python 3.10 已就绪")
    else:
        print("   ⚠️  建议升级到 Python 3.10 以获得最佳兼容性")

    # 虚拟环境
    venv_path = os.path.join(PROJECT_ROOT, "venv")
    if os.path.exists(venv_path):
        print(f"\n📌 虚拟环境: {venv_path}")
        print("   ✅ venv 已创建")
    else:
        print(f"\n📌 虚拟环境: 未找到")
        print("   ⚠️  建议运行: python3.10 -m venv venv")

    # 关键文件检查
    key_files = [
        "PanoWorld/inference.py",
        "PanoWorld/model.py",
        "PanoWorld/requirements.txt",
        "PanoWorld/configs/local_inference_1024_512.yaml",
    ]
    print("\n📌 关键文件检查:")
    all_ok = True
    for f in key_files:
        path = os.path.join(PROJECT_ROOT, f)
        if os.path.exists(path):
            print(f"   ✅ {f}")
        else:
            print(f"   ❌ {f} (缺失)")
            all_ok = False

    # 模型目录
    model_dir = os.path.join(PANOWORLD_DIR, "model_ckpt")
    if os.path.exists(model_dir):
        models = [f for f in os.listdir(model_dir) if f.endswith('.pt') or f.endswith('.ckpt')]
        print(f"\n📌 模型检查点: {model_dir}")
        if models:
            for m in models:
                print(f"   ✅ {m}")
        else:
            print("   ⚠️  暂无模型文件（需从 HuggingFace 下载）")
    else:
        print(f"\n📌 模型检查点目录不存在，已创建: {model_dir}")
        os.makedirs(model_dir, exist_ok=True)

    # 数据目录
    data_dir = os.path.join(PANOWORLD_DIR, "data")
    print(f"\n📌 数据目录: {data_dir}")
    if os.path.exists(data_dir):
        print("   ✅ 数据目录已创建")
    else:
        os.makedirs(data_dir, exist_ok=True)
        print("   ✅ 数据目录已自动创建")

    return all_ok

def generate_colab_notebook():
    """生成 Colab 专用 Notebook"""
    print("\n" + "=" * 60)
    print("🚀 生成 Colab 专用 Notebook")
    print("=" * 60)

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 🏠 PanoWorld GPU 推理 - Colab 专用版\n",
                    "\n",
                    "本地管理代码 → Colab 运行 GPU 推理\n",
                    "\n",
                    "**配置来源**: 本地配置文件自动生成\n",
                    "**更新方式**: 在本地修改配置后重新运行 `sync_to_colab.py`"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1️⃣ 挂载 Google Drive"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from google.colab import drive\n",
                    "drive.mount('/content/drive')\n",
                    "\n",
                    "# 配置路径（根据你的 Google Drive 实际路径修改）\n",
                    "DRIVE_MOUNT = '/content/drive/MyDrive'  # 或你的自定义路径\n",
                    "PROJECT_NAME = 'PanoWorld'\n",
                    "PROJECT_PATH = f\"{DRIVE_MOUNT}/{PROJECT_NAME}\"\n",
                    "\n",
                    "import os\n",
                    "os.makedirs(PROJECT_PATH, exist_ok=True)\n",
                    "print(f\"项目路径: {PROJECT_PATH}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2️⃣ 克隆仓库（首次运行）或更新代码"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 方式1: 从 GitHub 克隆（推荐首次使用）\n",
                    "# !cd {PROJECT_PATH} && git clone https://github.com/jjrCN/PanoWorld.git\n",
                    "\n",
                    "# 方式2: 从 Google Drive 同步（推荐日常开发）\n",
                    "# 确保你已通过 sync_to_colab.py 将代码上传到 Drive\n",
                    "\n",
                    "# 方式3: 直接上传代码到 Colab 运行时（小修改时）\n",
                    "print(\"请根据你的同步方式选择上方注释中的命令\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3️⃣ 安装依赖"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "%cd {PROJECT_PATH}/PanoWorld\n",
                    "\n",
                    "# 安装依赖\n",
                    "!pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121\n",
                    "!pip install -q -r requirements.txt\n",
                    "!pip install -q omegaconf easydict\n",
                    "\n",
                    "print(\"✅ 依赖安装完成\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 4️⃣ 检查 GPU"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "!nvidia-smi\n",
                    "import torch\n",
                    "print(f\"CUDA: {torch.cuda.is_available()}\")\n",
                    "print(f\"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 5️⃣ 下载模型权重（如未同步到 Drive）"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "\n",
                    "os.makedirs(\"model_ckpt\", exist_ok=True)\n",
                    "\n",
                    "# 下载 1024x512 模型\n",
                    "!wget -q --show-progress \\\n",
                    "    \"https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_1024_512.pt\" \\\n",
                    "    -O model_ckpt/ckpt_panoworld_lrm_1024_512.pt\n",
                    "\n",
                    "# 如需 2048x1024，取消下方注释\n",
                    "# !wget -q --show-progress \\\n",
                    "#     \"https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_2048_1024.ckpt\" \\\n",
                    "#     -O model_ckpt/ckpt_panoworld_lrm_2048_1024.ckpt\n",
                    "\n",
                    "print(\"✅ 模型下载完成\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 6️⃣ 配置推理参数"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 根据你的实际数据路径修改\n",
                    "config_content = '''\n",
                    "model:\n",
                    "  class_name: model.PanoWorldLRM\n",
                    "  patch_factor: 2\n",
                    "  dim1: 256\n",
                    "  dim2: 512\n",
                    "  dim3: 1024\n",
                    "  num_register_tokens: 4\n",
                    "  head_dim: 64\n",
                    "  inter_multi: 4\n",
                    "  qk_norm: true\n",
                    "  stage1_nlayer: 2\n",
                    "  stage2_nlayer: 4\n",
                    "  stage3_nlayer: 8\n",
                    "  patch_size: 2\n",
                    "  in_channels: 12\n",
                    "  output_gs: true\n",
                    "  gaussians:\n",
                    "    sh_degree: 1\n",
                    "    opacity_degree: 2\n",
                    "    near_plane: 0.01\n",
                    "    far_plane: 1000000.0\n",
                    "    scale_bias: -6.9\n",
                    "    scale_max: -1.2\n",
                    "    opacity_bias: 1.0\n",
                    "    align_to_pixel: true\n",
                    "    max_dist: 15.0\n",
                    "    min_dist: 0.1\n",
                    "data:\n",
                    "  root_data_dir: \"/content/drive/MyDrive/PanoWorld/data/RealSee3D_eval\"\n",
                    "  data_path: \"data_realsee3D/realsee3D_1024_1024_20260507_whole_room_map_json_eval_8views.txt\"\n",
                    "  square_crop: true\n",
                    "  resize_h: 512\n",
                    "  resize_h_pano: 512\n",
                    "  sample_target_images: 6\n",
                    "  viewpoint_max_view: 8\n",
                    "  filter_top_down: false\n",
                    "training:\n",
                    "  train_stage: 1\n",
                    "inference:\n",
                    "  dataset_name: dataset.Dataset\n",
                    "  amp_dtype: bf16\n",
                    "  use_amp: true\n",
                    "  batch_size_per_gpu: 1\n",
                    "  num_threads: 8\n",
                    "  num_workers: 2\n",
                    "  prefetch_factor: 4\n",
                    "  use_tf32: true\n",
                    "  ckpt_path: model_ckpt/ckpt_panoworld_lrm_1024_512.pt\n",
                    "  out_dir: ./outputs/colab_inference\n",
                    "'''\n",
                    "\n",
                    "with open(\"configs/colab_inference.yaml\", \"w\") as f:\n",
                    "    f.write(config_content)\n",
                    "\n",
                    "print(\"✅ 配置已生成: configs/colab_inference.yaml\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 7️⃣ 运行推理"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "!CUDA_VISIBLE_DEVICES=0 python inference.py --config configs/colab_inference.yaml"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 8️⃣ 结果同步回 Google Drive（可选）"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import shutil\n",
                    "\n",
                    "# 将结果复制到 Drive\n",
                    "shutil.copytree(\"./outputs/colab_inference\", f\"{DRIVE_MOUNT}/PanoWorld/outputs\", dirs_exist_ok=True)\n",
                    "print(\"✅ 结果已同步到 Google Drive\")"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    output_path = os.path.join(PROJECT_ROOT, "PanoWorld_Colab_GPU_Test.ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"\n✅ Notebook 已生成: {output_path}")
    print("   将此文件上传到 Google Colab 即可运行")
    return output_path

def print_sync_guide():
    """打印同步指引"""
    print("\n" + "=" * 60)
    print("📋 本地 ↔ Colab 同步方案")
    print("=" * 60)

    print("""
方案 A: Google Drive 同步（推荐日常开发）
───────────────────────────────────────────
1. 在你的 Google Drive 创建文件夹: MyDrive/PanoWorld/
2. 将本地 PanoWorld/ 目录下的代码上传到该文件夹
3. 在 Colab 中挂载 Drive:
   from google.colab import drive
   drive.mount('/content/drive')
4. 直接运行 Drive 中的代码

方案 B: GitHub 同步
───────────────────────────────────────────
1. 将代码推送到你自己的 GitHub 仓库
2. 在 Colab 中直接 git clone
3. 适合多人协作

方案 C: 手动上传（适合快速测试）
───────────────────────────────────────────
1. 在 Colab 左侧文件面板直接上传
2. 适合单次快速测试
""")

def main():
    print("🚀 PanoWorld 本地-Colab 协同部署工具")
    print("=" * 60)

    # 检查环境
    ok = check_environment()

    if not ok:
        print("\n⚠️  部分文件缺失，请确保代码已完整下载")

    # 生成 Colab Notebook
    notebook_path = generate_colab_notebook()

    # 打印同步指引
    print_sync_guide()

    print("\n" + "=" * 60)
    print("✅ 准备就绪！下一步：")
    print("=" * 60)
    print(f"""
1. 在 Google Drive 创建目录: MyDrive/PanoWorld/
2. 将 {PANOWORLD_DIR}/ 上传到该目录
3. 打开 {notebook_path} 上传到 Colab
4. 按 Cell 顺序运行即可
""")

if __name__ == "__main__":
    main()
