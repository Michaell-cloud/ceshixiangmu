# 🏠 PanoWorld 本地-Colab 协同部署方案

> **本地管理代码 & 数据** → **Colab GPU 运行推理**

---

## 📁 项目结构

```
PanoWorld/
├── PanoWorld/                    # 项目代码
│   ├── inference.py              # 推理入口
│   ├── model.py                  # PanoWorldLRM 模型
│   ├── transformer.py            # Transformer 模块
│   ├── dpt_head.py               # DPT 特征头
│   ├── prope_custom.py           # PRoPE 位姿编码
│   ├── dataset.py                # 数据加载
│   ├── utils.py                  # 工具函数
│   ├── configs/                  # 配置文件
│   │   ├── local_inference_1024_512.yaml
│   │   └── colab_inference.yaml
│   ├── model_ckpt/               # 模型权重（需下载）
│   ├── data/                     # 数据目录
│   └── outputs/                  # 输出结果
├── venv/                         # Python 虚拟环境
├── sync_to_colab.py             # Colab 同步工具
├── setup_local.sh               # 本地环境一键设置
├── PanoWorld_Colab_GPU_Test.ipynb  # Colab Notebook
└── README.md                     # 本文件
```

---

## 🚀 快速开始

### 第一步：本地环境设置

```bash
# 1. 进入项目目录
cd /Users/huxiaobo/Documents/PanoWorld

# 2. 运行一键设置脚本
bash setup_local.sh
```

此脚本会自动：
- ✅ 检查 Python 3.10
- ✅ 创建虚拟环境 (`venv/`)
- ✅ 安装 CPU 版 PyTorch 和项目依赖
- ✅ 安装 `omegaconf`（配置管理）

### 第二步：激活虚拟环境

```bash
source venv/bin/activate
```

### 第三步：生成 Colab Notebook

```bash
python sync_to_colab.py
```

此命令会：
- 🔍 检查本地环境完整性
- 📝 生成 `PanoWorld_Colab_GPU_Test.ipynb`
- 📋 打印同步指引

---

## 📦 模型下载

### 方式 1：脚本下载（推荐）

```bash
cd PanoWorld
bash download_models.sh
```

### 方式 2：手动下载

| 模型 | 大小 | 链接 |
|------|------|------|
| 1024x512 | ~2.4GB | [下载](https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_1024_512.pt) |
| 2048x1024 | ~2.4GB | [下载](https://huggingface.co/JiaJinrang/PanoWorld/resolve/main/model_ckpt/ckpt_panoworld_lrm_2048_1024.ckpt) |

下载后放置到 `PanoWorld/model_ckpt/` 目录。

---

## 🔗 本地 ↔ Colab 同步方案

### 方案 A：Google Drive（推荐）

```
本地代码修改 → 上传到 Drive → Colab 挂载运行 → 结果下载
```

**步骤：**
1. 在 Google Drive 创建 `MyDrive/PanoWorld/` 文件夹
2. 将 `PanoWorld/` 代码目录上传到该文件夹
3. 在 Colab 中挂载 Drive：
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
4. 运行 `PanoWorld_Colab_GPU_Test.ipynb`

### 方案 B：GitHub 同步

```
本地代码修改 → git push → Colab git clone → 运行
```

### 方案 C：手动上传

适合单次快速测试，直接将文件拖拽到 Colab 文件面板。

---

## 💻 本地开发（CPU 调试）

本地无 GPU，但可以用于：
- ✅ 代码阅读和修改
- ✅ 配置文件调整
- ✅ 数据结构验证
- ✅ 模型结构检查

```bash
# 进入虚拟环境
source venv/bin/activate
cd PanoWorld

# 本地运行（CPU 模式，极慢，仅用于调试）
python inference.py --config configs/local_inference_1024_512.yaml
```

---

## 🚀 Colab GPU 运行

### 1. 打开 Colab

访问 [colab.research.google.com](https://colab.research.google.com)

### 2. 上传 Notebook

将 `PanoWorld_Colab_GPU_Test.ipynb` 上传到 Colab

### 3. 设置 GPU

运行时 → 更改运行时类型 → **GPU (T4 或更高)**

### 4. 按 Cell 顺序运行

| Cell | 功能 |
|------|------|
| 1 | 挂载 Google Drive |
| 2 | 克隆/同步代码 |
| 3 | 安装依赖 |
| 4 | 检查 GPU |
| 5 | 下载模型 |
| 6 | 配置参数 |
| 7 | **运行推理** |
| 8 | 同步结果回 Drive |

### 5. 显存需求

| 配置 | 推荐 GPU | 显存 | 预计时间 |
|------|---------|------|---------|
| 1024x512 | T4 | 8-12GB | ~5-10分钟/scene |
| 2048x1024 | V100/A100 | 16-24GB | ~15-30分钟/scene |

---

## 📊 结果查看

推理完成后，结果保存在 `PanoWorld/outputs/`：

```
outputs/
└── colab_inference/
    └── {scene_name}/
        └── {view_name}/
            ├── target_rendering/       # 渲染的新视角 RGB
            ├── target_rendering_depth/ # 深度图
            ├── input_image/            # 输入全景图
            ├── input_depth/            # 输入深度图
            └── output_ply/             # 3DGS PLY 文件
```

### PLY 文件查看

- 在线：[Supersplat](https://playcanvas.com/supersplat/editor/)
- 桌面：[SIBR Viewers](https://github.com/graphdeco-inria/gaussian-splatting?tab=readme-ov-file#sibr-viewers)

---

## 🛠️ 常见问题

### Q: 本地安装 gsplat 失败？
A: `gsplat` 需要 CUDA 编译。本地无需 GPU，跳过即可，Colab 会自动安装 GPU 版本。

### Q: Colab 挂载 Drive 失败？
A: 确保已授权 Colab 访问 Google Drive，且路径正确。

### Q: 模型下载太慢？
A: 使用 `wget -c` 支持断点续传，或在 Colab 中直接下载（Colab 网络通常更快）。

### Q: 显存不足？
A: 使用 1024x512 模型，或升级到 Colab Pro (V100/A100)。

---

## 📚 参考链接

- 论文：[arXiv:2605.17916](https://arxiv.org/abs/2605.17916)
- 项目主页：[PanoWorld](https://jjrcn.github.io/PanoWorld-project-home/)
- GitHub：[github.com/jjrCN/PanoWorld](https://github.com/jjrCN/PanoWorld)
- HuggingFace 模型：[JiaJinrang/PanoWorld](https://huggingface.co/JiaJinrang/PanoWorld)

---

## 📝 更新日志

| 日期 | 更新 |
|------|------|
| 2026-05-26 | 创建本地-Colab 协同部署方案 |
