# 🔗 PanoWorld GitHub + Colab 同步指南

> 本地代码管理 → GitHub 仓库同步 → Colab GPU 推理

---

## 📋 方案概览

```
┌─────────────┐     git push      ┌─────────────┐     git clone     ┌─────────────┐
│   本地电脑   │ ────────────────→ │   GitHub    │ ────────────────→ │   Colab     │
│  (无 GPU)   │                   │   仓库      │                   │  (GPU T4)   │
└─────────────┘                   └─────────────┘                   └─────────────┘
       ↑                                                                  │
       │                    本地管理代码                                      │
       │                    • 修改配置                                        ↓
       │                    • 调整参数                                  运行推理
       │                    • 添加数据                                  下载结果
       └──────────────────────────────────────────────────────────────────┘
                            结果保存到 Google Drive（可选）
```

---

## 🚀 快速上手（3 步走）

### 第 1 步：创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 填写仓库信息：
   - **Repository name**: `PanoWorld`（或你喜欢的名字）
   - **Visibility**: Private（推荐，模型和数据较大）
   - **Initialize**: 不勾选（已有本地代码）
4. 点击 **Create repository**

### 第 2 步：推送本地代码

在本地终端执行：

```bash
cd /Users/huxiaobo/Documents/PanoWorld

# 设置 Git 用户信息（首次使用）
git config user.name "你的名字"
git config user.email "你的邮箱"

# 添加 GitHub 远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库.git

# 推送代码
git branch -M main
git push -u origin main
```

**注意**：`.gitignore` 已配置，模型权重 (`*.pt`) 和数据不会上传到 GitHub。

### 第 3 步：Colab 运行

1. 打开 [Google Colab](https://colab.research.google.com)
2. 上传 `GITHUB_COLAB_NOTEBOOK.ipynb`
3. **运行时 → 更改运行时类型 → GPU (T4)**
4. 修改 **Cell 2** 中的 `GITHUB_REPO` 为你的仓库地址：
   ```python
   GITHUB_REPO = "https://github.com/YOUR_USERNAME/YOUR_REPO.git"
   ```
5. 按顺序运行所有 Cell

---

## 🔄 日常开发工作流

### 本地修改代码

```bash
cd /Users/huxiaobo/Documents/PanoWorld

# 激活虚拟环境
source venv/bin/activate

# 修改代码（如调整配置、修改参数等）
# ...

# 提交更改
git add .
git commit -m "描述你的修改"
git push origin main
```

### Colab 更新代码

在 Colab 中运行更新 Cell：
```python
%cd /content/PanoWorld
!git pull origin main
```

---

## 📦 仓库内容说明

### 提交到 GitHub 的文件（代码）

```
PanoWorld/
├── configs/          # 配置文件
├── inference.py      # 推理入口
├── model.py          # 模型定义
├── transformer.py    # Transformer 模块
├── dpt_head.py       # DPT 头
├── prope_custom.py   # PRoPE 编码
├── dataset.py        # 数据加载
├── utils.py          # 工具函数
├── metric_utils.py   # 评估工具
├── requirements.txt  # 依赖列表
└── setup.py          # 配置解析
```

### 不提交的文件（被 .gitignore 排除）

```
PanoWorld/
├── model_ckpt/*.pt   # 模型权重（2.4GB）
├── data/             # 数据集
└── outputs/          # 推理结果
```

这些大文件在 Colab 中直接从 HuggingFace 下载。

---

## 🎯 三种使用场景

### 场景 1：修改配置后重新推理

```
1. 本地: 修改 configs/local_inference_1024_512.yaml
2. 本地: git add . && git commit -m "更新配置" && git push
3. Colab: 运行 git pull Cell
4. Colab: 重新运行推理
```

### 场景 2：修改代码逻辑

```
1. 本地: 修改 model.py 或 dataset.py
2. 本地: 运行代码检查（CPU 模式，确保无语法错误）
3. 本地: git add . && git commit -m "修改模型逻辑" && git push
4. Colab: 运行 git pull Cell
5. Colab: 重新运行推理
```

### 场景 3：保存推理结果

```
1. Colab: 运行推理 Cell
2. Colab: 运行 "保存结果到 Drive" Cell
3. 本地: 从 Google Drive 下载结果查看
```

---

## 🔧 常见问题

### Q1: GitHub 推送失败（权限错误）

**A**: 使用 Personal Access Token 代替密码：

```bash
# 1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
# 2. 生成 Token，勾选 repo 权限
# 3. 使用 Token 推送
git remote set-url origin https://TOKEN@github.com/用户名/仓库.git
git push origin main
```

### Q2: Colab 上 git clone 失败

**A**: 检查仓库地址是否正确：
```python
GITHUB_REPO = "https://github.com/YOUR_USERNAME/YOUR_REPO.git"
```
如果是 Private 仓库，需要先配置 Token：
```python
!git clone https://TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Q3: 如何保存结果到 Google Drive？

**A**: 在 Notebook 中设置：
```python
SAVE_TO_DRIVE = True
DRIVE_PATH = "/content/drive/MyDrive/PanoWorld"
```

### Q4: 模型权重需要上传到 GitHub 吗？

**A**: **不需要**。`.gitignore` 已排除 `*.pt` 文件。Colab 直接从 HuggingFace 下载模型，更高效。

---

## 📊 方案对比

| 特性 | Google Drive 方案 | **GitHub 方案** ✅ |
|------|------------------|-------------------|
| 代码版本控制 | ❌ 无 | ✅ Git 完整支持 |
| 多人协作 | ❌ 困难 | ✅ Pull Request |
| 代码审查 | ❌ 无 | ✅ Code Review |
| 历史追溯 | ❌ 无 | ✅ Commit 历史 |
| 分支管理 | ❌ 无 | ✅ 多分支支持 |
| 设置复杂度 | 低 | 中等 |
| 适合场景 | 个人快速测试 | **长期开发/协作** |

---

## 📝 文件清单

| 文件 | 用途 |
|------|------|
| `GITHUB_COLAB_NOTEBOOK.ipynb` | **Colab 专用 Notebook** |
| `GITHUB_SYNC_GUIDE.md` | 本指南 |
| `setup_local.sh` | 本地环境设置 |
| `sync_to_colab.py` | 生成 Drive 版 Notebook |
| `PanoWorld/download_models.sh` | 模型下载脚本 |
| `PanoWorld/configs/local_inference_1024_512.yaml` | 本地配置 |

---

## 🎉 下一步

1. ✅ 创建 GitHub 仓库
2. ✅ 推送本地代码
3. ✅ 打开 Colab，上传 `GITHUB_COLAB_NOTEBOOK.ipynb`
4. ✅ 修改 `GITHUB_REPO` 为你的地址
5. ✅ 选择 GPU，开始运行！
