import logging
import torch
from models.model_interface import TTSModelInterface, ModelInfo
from kokoro import KModel, KPipeline
import numpy as np
import toml

class TTSModel(TTSModelInterface):
    def __init__(self, config_path: str):
        with open(config_path) as f:
            config = toml.load(f)
        
        self.device = "cuda" if torch.cuda.is_available() and config['performance']['use_gpu'] is True else "cpu"
        self.repo_id = config['model']['repo_id']
        
        en_pipeline = KPipeline(lang_code='a', repo_id=self.repo_id, model=False)
        def en_callable(text):
            return next(en_pipeline(text)).phonemes

        self.model = KModel(repo_id=self.repo_id).to(self.device).eval()
        self.pipeline = KPipeline(lang_code='z', repo_id=self.repo_id, model=self.model, en_callable=en_callable)
        self.voice_list = config['voices']['available']
        self.default_voice = config['voices']['default']
    def synthesize(self, text: str, voice_type: str, speed: float) -> np.ndarray:
        if voice_type not in self.voice_list:
            logging.warning(f"使用默认声音: {self.default_voice}")
            voice_type = self.default_voice
        generator = self.pipeline(text, voice_type, speed)
        result_wav = None
        for result in generator:
            if result.audio is not None:
                wav = result.audio.cpu().numpy()
                result_wav = np.concatenate([result_wav, wav]) if result_wav is not None else wav
        if result_wav is None:
            raise ValueError("合成的音频数据为空")
        return result_wav 
    def get_model_info(self) -> ModelInfo:
        return ModelInfo(
            model_name="Kokoro",
            device=self.device,
            voices=self.voice_list,
            default_voice=self.default_voice,
            description="Kokoro 模型推理速度快"
        )
    def max_input_length(self) -> int:
        return 100
    
    @staticmethod
    def create() -> 'TTSModel':
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "config.toml")
        return TTSModel(config)
        
        

