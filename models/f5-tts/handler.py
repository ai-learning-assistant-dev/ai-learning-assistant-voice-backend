from importlib.resources import files
import os
from f5_tts.api import F5TTS
import numpy as np
from models.model_interface import TTSModelInterface, ModelDetail, VoiceDetail
import toml
import models.voice_util as voice_util

class TTSModel(TTSModelInterface):
    def __init__(self, config_path: str):
        with open(config_path) as f:
            config = toml.load(f)
        
        self.default_voice = config['voice']['default_voice']
        self.model_name = config['model']['name']
        self.f5tts = F5TTS()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.voice_dir = os.path.join(self.current_dir, "voices")
        self.available_voices = voice_util.load_voice_config(os.path.join(self.voice_dir, "voice_config.json"))
    def synthesize(self, text: str, voice_type: str, speed: float) -> np.ndarray:
        voice = self.available_voices.get_voice_config(voice_type, self.default_voice)
        
        wav, sr, spec = self.f5tts.infer(
            ref_file=voice.get_file_path(self.voice_dir),
            ref_text=voice.get_text(),
            gen_text=text,
            seed=None,
        )
        if wav is None:
            raise ValueError("合成的音频数据为空")
        return wav 
    def get_model_info(self) -> ModelDetail:
        return ModelDetail(
            model_name=self.model_name,
            device=self.f5tts.device,
            voices=[VoiceDetail(name=voice.name, description=voice.description) for voice in self.available_voices.voices.values()],
            description="F5-TTS 模型效果好，支持音色克隆。建议在GPU环境使用。"
        )
    def max_input_length(self) -> int:
        return 300
    
    @staticmethod
    def create() -> 'TTSModel':
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "model_config.toml")
        return TTSModel(config)
