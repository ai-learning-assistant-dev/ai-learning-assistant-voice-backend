# TTS自动模型选择功能说明

## 功能概述

该功能允许TTS服务根据运行环境自动选择最合适的模型：
- **CUDA环境**：自动选择 `index-tts` 模型（GPU加速）
- **CPU环境**：自动选择 `kokoro` 模型（CPU优化）

## /voice挂载到 /app/tts/models/index-tts

## 使用方法

### 1. Docker Run 启动（推荐）

#### 自动检测模式（默认）
```bash
# 启动所有服务
docker run -e SERVICE_TYPE=both your-image ./start.sh

# 只启动ASR服务
docker run -e SERVICE_TYPE=asr your-image ./start.sh

# 只启动TTS服务
docker run -e SERVICE_TYPE=tts your-image ./start.sh
```

#### 手动指定模型
如果需要强制使用特定模型，可以设置环境变量：

```bash
# 强制使用kokoro模型
TTS_MODELS=kokoro docker-compose up ai-voice-backend

# 强制使用index-tts模型
TTS_MODELS=index-tts docker-compose up ai-voice-backend
```