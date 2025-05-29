import logging
import os
import torch
from models.model_interface import TTSModelInterface, ModelDetail, VoiceDetail
from kokoro import KModel, KPipeline
import numpy as np
import toml
import models.voice_util as voice_util

class TTSModel(TTSModelInterface):
    def __init__(self, config_path: str):
        with open(config_path) as f:
            config = toml.load(f)
        
        self.device = "cuda" if torch.cuda.is_available() and config['performance']['use_gpu'] == True else "cpu"
        logging.info(f"使用设备: {self.device}")
        self.repo_id = config['model']['repo_id']
        
        en_pipeline = KPipeline(lang_code='a', repo_id=self.repo_id, model=False)
        def en_callable(text):
            return next(en_pipeline(text)).phonemes

        self.model = KModel(repo_id=self.repo_id).to(self.device).eval()
        self.pipeline = KPipeline(lang_code='z', repo_id=self.repo_id, model=self.model, en_callable=en_callable)

        self.default_voice = config['voice']['default_voice']
        self.model_name = config['model']['name']
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.voice_dir = os.path.join(self.current_dir, "voices")
        self.available_voices = voice_util.load_voice_config(os.path.join(self.voice_dir, "voice_config.json"))
    def synthesize(self, text: str, voice_type: str, speed: float) -> np.ndarray:
        voice = self.available_voices.get_voice_config(voice_type, self.default_voice)
        generator = self.pipeline(text, voice.get_voice_name(), speed)
        result_wav = None
        for result in generator:
            if result.audio is not None:
                wav = result.audio.cpu().numpy()
                result_wav = np.concatenate([result_wav, wav]) if result_wav is not None else wav
        if result_wav is None:
            raise ValueError("合成的音频数据为空")
        return result_wav 
    def get_model_info(self) -> ModelDetail:
        return ModelDetail(
            model_name=self.model_name,
            device=self.device,
            voices=[VoiceDetail(name=voice.name, description=voice.description) for voice in self.available_voices.voices.values()],
            description="Kokoro 模型推理速度快"
        )
    def max_input_length(self) -> int:
        return 100
    
    @staticmethod
    def create() -> 'TTSModel':
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "model_config.toml")
        return TTSModel(config)
        
        

