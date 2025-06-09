# Quickstart

## 安装依赖
```bash
# 安装pytorch，如果环境已经有了，就不用重复安装了
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# 安装主依赖
pip install -r ./requirements.txt
```

## 下载模型
```bash
python ./cli.py download --model-names=kokoro,f5-tts
```

## 预热模型，下载运行时才会下载的依赖
```bash
python ./cli.py warm-up --model-names=kokoro,f5-tts
```

## 启动服务
```bash
python ./cli.py run --model-names=kokoro,f5-tts
```

## 测试
```bash
# 测试kokoro模型
python ./test_client.py --model kokoro --voice zm_010

# 测试f5-tts模型
python ./test_client.py --model f5-tts --voice vmz
```