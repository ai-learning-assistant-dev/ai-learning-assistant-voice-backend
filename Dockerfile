FROM docker.io/pytorch/pytorch:2.7.0-cuda11.8-cudnn9-runtime

WORKDIR /app

# 充分利用缓存加快打镜像速度
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

RUN ["python", "cli.py", "warm-up", "--model-names=kokoro,f5-tts"]

EXPOSE 8000
CMD ["python", "cli.py", "run", "--model-names=kokoro,f5-tts"]
