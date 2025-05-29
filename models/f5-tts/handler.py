from importlib.resources import files
import os
from cached_path import cached_path
from f5_tts.api import F5TTS
from huggingface_hub import hf_hub_download
import numpy as np
import torch
from models.model_interface import TTSModelInterface, ModelDetail, VoiceDetail
import toml
import models.voice_util as voice_util

class TTSModel(TTSModelInterface):
    def __init__(self, config_path: str):
        with open(config_path) as f:
            config = toml.load(f)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_voice = config['voice']['default_voice']
        self.model_name = config['model']['name']
        self.use_gpu = config['performance']['use_gpu']
        
        self.model_path = config['paths']['model_path']
        self.model_path = os.path.join(self.current_dir, self.model_path)

        self.vocos_path = config['paths']['vocos_path']
        self.vocos_path = os.path.join(self.current_dir, self.vocos_path)
        
        
        self.voice_dir = os.path.join(self.current_dir, config['paths']['voice_path'])
        self.available_voices = voice_util.load_voice_config(os.path.join(self.voice_dir, "voice_config.json"))

        self.f5tts = F5TTS(ckpt_file=self.model_path, vocoder_local_path=self.vocos_path, device="cpu" if not self.use_gpu else None)
    def synthesize(self, text: str, voice_type: str, speed: float) -> np.ndarray:
        voice = self.available_voices.get_voice_config(voice_type, self.default_voice)
        
        wav, sr, spec = self.f5tts.infer(
            ref_file=voice.get_file_path(self.voice_dir),
            ref_text=voice.get_text(),
            gen_text=text,
            seed=None,
            speed=speed,
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
    def download_model() -> str:
        vocos_path = TTSModel.download_vocos_model()

        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "model_config.toml")
        with open(config) as f:
            config = toml.load(f)
        model_download_dir = os.path.join(current_dir, "model_download")
        os.makedirs(model_download_dir, exist_ok=True)

        model = "F5TTS_v1_Base"
        repo_name, ckpt_step, ckpt_type = "F5-TTS", 1250000, "safetensors"
        ckpt_file = str(
            cached_path(f"hf://SWivid/{repo_name}/{model}/model_{ckpt_step}.{ckpt_type}")
        )
        print(ckpt_file)
        import shutil
        dest_path = os.path.join(model_download_dir, os.path.basename(ckpt_file))
        if os.path.islink(ckpt_file):  # 如果是符号链接，读取实际文件
            ckpt_file = os.path.realpath(ckpt_file)
        shutil.move(ckpt_file, dest_path)
        return dest_path
    
    @staticmethod
    def download_vocos_model() -> str:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "model_config.toml")
        with open(config) as f:
            config = toml.load(f)
        
        vocos_path = config['paths']['vocos_path']
        vocos_path = os.path.join(current_dir, vocos_path)

        repo_id = "charactr/vocos-mel-24khz"
        config_path = hf_hub_download(repo_id=repo_id, local_dir=vocos_path, filename="config.yaml")
        model_path = hf_hub_download(repo_id=repo_id, local_dir=vocos_path, filename="pytorch_model.bin")
        return vocos_path

    @staticmethod
    def create() -> 'TTSModel':
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "model_config.toml")
        return TTSModel(config)
