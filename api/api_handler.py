# api/main.py
import io
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import numpy as np
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models.model_manager import model_manager
from .utils import is_text_too_complex, split_text_safely
import soundfile as sf
app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=3600
)

class TTSRequest(BaseModel):
    input: str
    voice: str
    response_format: str = "mp3"
    speed: float = 1.0
    model: str = "Kokoro"
    
model_name = "Kokoro"

sample_rate = 24000


@app.post("/v1/audio/speech")
async def tts_handler(request: TTSRequest):
    logging.info(f"收到TTS请求: {request}")
    
    try:
        model = model_manager.get_model(model_name)
         # 处理音频生成
        if is_text_too_complex(request.input):
            text_segments = split_text_safely(request.input)
            segment_audios = []
            for segment in text_segments:
                audio_data, sr = model.synthesize(segment, request.voice, request.speed)
                segment_audios.append(audio_data)
            combined_audio = np.concatenate(segment_audios)
        else:
            combined_audio = model.synthesize(request.input, request.voice, request.speed)

        # 创建内存中的音频文件
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, combined_audio, sample_rate, format=request.response_format)
        audio_buffer.seek(0)

        return StreamingResponse(
            audio_buffer,
            media_type=f"audio/{request.response_format}",
            headers={
                "Content-Disposition": f"attachment; filename=audio.{request.response_format}"
            }
        )
    except Exception as e:
        logging.error(f"TTS处理出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"TTS处理出错: {str(e)}")