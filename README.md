# Quickstart

## 安装依赖
```bash
# 安装主依赖
pip install -r ./requirements.txt

# 安装模型特定依赖
pip install -r ./models/kokoro/requirements.txt
pip install -r ./models/f5-tts/requirements.txt
```

# 下载模型
```bash
python ./cli.py download --model-names=kokoro,f5-tts
```

# 启动服务
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