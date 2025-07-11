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

