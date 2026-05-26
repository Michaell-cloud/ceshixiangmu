#!/usr/bin/env python3
"""
PanoWorld Colab 一键完整运行脚本
用法：在 Colab 中直接运行此文件
"""

import os
import sys
import urllib.request
import tarfile

print("=" * 60)
print("🚀 PanoWorld 一键部署")
print("=" * 60)

# ========== 配置 ==========
GITHUB_REPO = "https://github.com/Michaell-cloud/ceshixiangmu.git"
GITHUB_BRANCH = "main"

# ========== 1. 克隆代码 ==========
print("\n📦 1. 从 GitHub 克隆代码...")
if not os.path.exists("/content/PanoWorld"):
    os.system(f"git clone -b {GITHUB_BRANCH} {GITHUB_REPO} /content/PanoWorld")
    print("✅ 代码克隆完成")
else:
    print("✅ 代码已存在")

os.chdir("/content/PanoWorld/PanoWorld")
print(f"📍 工作目录: {os.getcwd()}")

# ========== 2. 安装依赖 ==========
print("\n📦 2. 安装依赖...")
os.system("pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121")
os.system("pip install -q -r requirements.txt")
os.system("pip install -q omegaconf easydict")
print("✅ 依赖安装完成")

# ========== 3. 下载模型 ==========
print("\n📦 3. 下载模型...")
os.makedirs("model_ckpt", exist_ok=True)
model_path = "model_ckpt/ckpt_panoworld_lrm_1024_512.pt"
if not os.path.exists(model_path):
    urllib.request.urlretrieve(
        "https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_1024_512.pt",
        model_path
    )
    print(f"✅ 模型下载完成 ({os.path.getsize(model_path)/1024/1024:.0f} MB)")
else:
    print("✅ 模型已存在")

# ========== 4. 下载数据 ==========
print("\n📦 4. 下载数据...")
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/RealSee3D_eval"):
    tar_path = "RealSee3D_eval_data.tar.gz"
    if not os.path.exists(tar_path):
        urllib.request.urlretrieve(
            "https://huggingface.co/datasets/JiaJinrang/PanoWorld/resolve/main/RealSee3D_eval_data.tar.gz",
            tar_path
        )
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path="data")
    print("✅ 数据解压完成")
else:
    print("✅ 数据已存在")

# ========== 5. 生成配置 ==========
print("\n⚙️ 5. 生成配置...")
os.makedirs("configs", exist_ok=True)
config_content = '''model:
  class_name: model.PanoWorldLRM
  patch_factor: 2
  dim1: 256
  dim2: 512
  dim3: 1024
  num_register_tokens: 4
  head_dim: 64
  inter_multi: 4
  qk_norm: true
  stage1_nlayer: 2
  stage2_nlayer: 4
  stage3_nlayer: 8
  patch_size: 2
  in_channels: 12
  output_gs: true
  gaussians:
    sh_degree: 1
    opacity_degree: 2
    near_plane: 0.01
    far_plane: 1000000.0
    scale_bias: -6.9
    scale_max: -1.2
    opacity_bias: 1.0
    align_to_pixel: true
    max_dist: 15.0
    min_dist: 0.1
data:
  root_data_dir: "./data/RealSee3D_eval"
  data_path: "data_realsee3D/realsee3D_1024_1024_20260507_whole_room_map_json_eval_8views.txt"
  square_crop: true
  resize_h: 512
  resize_h_pano: 512
  sample_target_images: 6
  viewpoint_max_view: 8
  filter_top_down: false
training:
  train_stage: 1
inference:
  dataset_name: dataset.Dataset
  amp_dtype: bf16
  use_amp: true
  batch_size_per_gpu: 1
  num_threads: 8
  num_workers: 2
  prefetch_factor: 4
  use_tf32: true
  ckpt_path: model_ckpt/ckpt_panoworld_lrm_1024_512.pt
  out_dir: ./outputs/colab_inference
'''
with open("configs/colab_inference.yaml", "w") as f:
    f.write(config_content)
print("✅ 配置已生成")

# ========== 6. 运行推理 ==========
print("\n🚀 6. 运行推理...")
print("   这可能需要几分钟，请耐心等待...")
os.system("CUDA_VISIBLE_DEVICES=0 python inference.py --config configs/colab_inference.yaml")
print("✅ 推理完成")

# ========== 7. 验证结果 ==========
print("\n📊 7. 验证结果...")
result_dir = "./outputs/colab_inference"
if os.path.exists(result_dir):
    scenes = [d for d in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, d))]
    print(f"✅ 生成场景数: {len(scenes)}")
else:
    print("❌ 输出目录不存在")

print("\n" + "=" * 60)
print("🎉 全部完成！")
print("=" * 60)
