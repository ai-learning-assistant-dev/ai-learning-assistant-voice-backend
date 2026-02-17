# Quickstart

## 环境

- python 3.11

## 安装依赖

```bash
# 安装主依赖
pip install -r ./requirements.txt

# 安装模型特定依赖
# kokoro
pip install -r ./models/kokoro/requirements.txt

# f5-tts
pip install -r ./models/f5-tts/requirements.txt

# index-tts
git submodule update --init --recursive
cd models/index-tts && pip install -r ./requirements.txt
```

## 使用 uv 管理依赖（推荐，Python 3.11.9）

```bash
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装并选择 Python 3.11.9（遵循 pyproject.toml 配置）
uv python install 3.11.9

# 同步基础依赖（pyproject.toml）
uv sync

# 如需额外模型依赖：
uv sync --extra kokoro --extra f5-tts

# index-tts 仍需初始化子模块并按其 README 安装
git submodule update --init --recursive
uv pip install -r models/index-tts/requirements.txt
```

## 使用 DeepSpeed 加速

`index-tts` 模型支持借助 DeepSpeed 进行性能加速。若要使用此功能，需按以下步骤操作：

### 1. 安装 DeepSpeed

执行以下命令安装 DeepSpeed：

```bash
pip install deepspeed
```

### 2. 安装 CUDA 工具包

使用 DeepSpeed 加速时，必须安装 nvcc（NVIDIA CUDA 编译器驱动），否则服务启动会失败。可通过以下命令安装 CUDA 工具包：

```bash
sudo apt install nvidia-cuda-toolkit
```

## 下载模型

```bash
python ./cli.py download --model-names=kokoro,f5-tts,index-tts
```

## 启动服务

```bash
python ./cli.py run --model-names=kokoro,f5-tts,index-tts --port 8001
```

## 测试

```bash
# 测试kokoro模型
python ./test_client.py --model kokoro --voice zm_010

# 测试f5-tts模型
python ./test_client.py --model f5-tts --voice 男性声音1

# 测试index-tts模型
python ./test_client.py --model index-tts --voice 男性声音1
```

## Windows 快速启动

### uv 安装(若没有uv脚本)

使用`download_uv_standalone.ps1`文件，可以将独立的uv包安装至上级目录中的util\uv-bin文件夹中

> ps:该方法是一个暂时性的替代，可能会有更优雅的解决方法


### 服务自动运行 


- 脚本位置: 提供两个便捷脚本： [scripts/start_windows.ps1](scripts/start_windows.ps1#L1) 和 [scripts/start_windows.bat](scripts/start_windows.bat#L1)。
- 作用: 在无环境的 Windows 机器上自动创建虚拟环境、使用阿里云 PyPI 镜像安装依赖，并启动服务（默认端口 `8000`）。
- PowerShell 示例: 在项目根目录打开 PowerShell（以管理员身份可选），运行：

  ```powershell
  .\scripts\start_windows.ps1
  ```

- CMD 示例: 在项目根目录打开命令提示符，运行：

  ```cmd
  .\scripts\start_windows.bat
  ```

- 说明: 脚本会检查 `python` 是否可用，若找不到会提示安装。脚本会在仓库根目录下创建 `.venv` 虚拟环境，并通过阿里云镜像安装 `requirements.txt`。

> ps:目前的uv路径是写死的，若需要可以自行修改
