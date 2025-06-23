# AI语音助手后端 - 统一Dockerfile（离线版本-预打包模型）
# 包含ASR和TTS两个服务，共享相同的运行环境，模型预打包在镜像中
FROM docker.io/pytorch/pytorch:2.7.0-cuda11.8-cudnn9-runtime

# 设置工作目录
WORKDIR /app

# 更换为国内软件源（解决网络问题）
# 选项1: 阿里云源
# RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
#     sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN sed -i 's/archive.ubuntu.com/repo.huaweicloud.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/repo.huaweicloud.com/g' /etc/apt/sources.list

# RUN sed -i 's/archive.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list && \
#     sed -i 's/security.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list

# 安装系统依赖和Python环境
# RUN apt-get update && \
#     apt-get install -y --fix-missing --no-install-recommends \
#     wget \
#     curl \
#     build-essential \
#     ffmpeg \
#     libsndfile1-dev \
#     espeak-ng \
#     locales \
#     # python3.10 \
#     # python3-pip \
#     # python3.10-dev \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*



# RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN pip3 install --no-cache-dir --timeout 60 --retries 3 \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl || \
    pip3 install --no-cache-dir --timeout 60 --retries 3 en_core_web_sm==3.7.1 || \
    echo "Warning: spacy model download failed, will download at runtime"

# 复制项目代码
COPY asr/ /app/asr/
COPY tts/ /app/tts/
COPY requirements.txt /app/requirements.txt

# 安装统一依赖
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# 安装各个TTS模型的特定依赖
RUN cd /app/tts/models/index-tts && pip3 install --no-cache-dir -r requirements.txt

# 复制预下载的模型文件到镜像中
# 这样模型就直接打包在镜像里，不需要运行时下载或挂载
COPY models_cache/ /app/models_cache/

# 确保模型目录权限正确
RUN chmod -R 755 /app/models_cache/

# 设置环境变量 - 使用镜像内的模型路径
ENV ASR_ENGINE=sensevoice
ENV ASR_DEVICE=cuda
ENV DEFAULT_MODEL=kokoro
ENV AUDIO_SAMPLE_RATE=24000
ENV CUDA_VISIBLE_DEVICES=0
ENV HF_HUB_OFFLINE=1
ENV MODELSCOPE_CACHE=/app/models_cache/modelscope
ENV HF_HOME=/app/models_cache/huggingface
ENV SENSEVOICE_MODEL=/app/models_cache/modelscope/models/iic/SenseVoiceSmall
# # 强制使用本地模型缓存，禁用在线下载
# ENV FUNASR_USE_CACHE=1
# ENV FUNASR_CACHE_DIR=/app/models_cache/modelscope
# # 设置ModelScope缓存为离线模式
# ENV MODELSCOPE_HUB_OFFLINE=1
# # 设置默认ASR语言为中文，避免多语言混合识别
# ENV ASR_DEFAULT_LANGUAGE=zh
# # 设置Python编码为UTF-8
# ENV PYTHONIOENCODING=utf-8
# # 禁用funasr的更新检查，避免网络问题
# ENV FUNASR_DISABLE_UPDATE=1

# 复制启动脚本
COPY start.sh /app/start.sh
COPY start_asr.sh /app/start_asr.sh
COPY start_tts.sh /app/start_tts.sh

# 设置脚本权限
RUN chmod +x /app/start.sh /app/start_asr.sh /app/start_tts.sh

# 暴露端口
EXPOSE 8000 9000

# 注释掉构建时的模型下载，因为模型已经预打包
# RUN python3 /app/tts/cli.py download --model-names kokoro,f5-tts,index-tts

# 设置启动命令 - 保持容器运行，等待手动启动服务
CMD ["tail", "-f", "/dev/null"] 