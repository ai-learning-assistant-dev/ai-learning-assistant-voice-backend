from importlib.resources import files
import os
from indextts.infer_v2 import IndexTTS2
import huggingface_hub
from huggingface_hub import hf_hub_download
import numpy as np
import torch

from models.model_interface import TTSModelInterface, ModelDetail, VoiceDetail
import toml
import models.voice_util as voice_util
import env
class TTSModel(TTSModelInterface):
    def __init__(self, config_path: str):
        with open(config_path, encoding="utf-8") as f:
            config = toml.load(f)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_voice = config['voice']['default_voice']
        self.model_name = config['model']['name']
        self.model_path = config['paths']['model_path']
        self.model_path = os.path.join(self.current_dir, self.model_path)
        self.voice_dir = os.path.join(self.current_dir, config['paths']['voice_path'])
        self.available_voices = voice_util.load_voice_config(os.path.join(self.voice_dir, "voice_config.json"))
        
        self.use_fp16 = config['performance'].get('use_fp16', False)
        self.use_deepspeed = config['performance'].get('use_deepspeed', False)
        self.use_cuda_kernel = config['performance'].get('use_cuda_kernel', False)

        use_gpu = (env.USE_GPU == "true" and torch.cuda.is_available())
        device = None
        if not use_gpu:
            device = "cpu"

        cfg_path = os.path.join(self.model_path, "config.yaml")
        self.tts = IndexTTS2(model_dir=self.model_path, cfg_path=cfg_path, device=device, use_fp16=self.use_fp16, use_deepspeed=self.use_deepspeed, use_cuda_kernel=self.use_cuda_kernel)
        
    def synthesize(self, text: str, voice_type: str, speed: float) -> np.ndarray:
        voice = self.available_voices.get_voice_config(voice_type, self.default_voice)
        _, wav = self.tts.infer(spk_audio_prompt=voice.get_file_path(self.voice_dir), text=text, verbose=True, output_path=None)
        return wav 
    def get_model_info(self) -> ModelDetail:
        return ModelDetail(
            model_name=self.model_name,
            device=self.tts.device,
            voices=[VoiceDetail(name=voice.name, description=voice.description) for voice in self.available_voices.voices.values()],
            description="IndexTTS2 模型效果最优。支持音色克隆。建议在GPU环境使用。",
            max_input_length=self.max_input_length()
        )
    def max_input_length(self) -> int:
        return 150
    
    @staticmethod
    def download_model() -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "model_config.toml"), encoding="utf-8") as f:
            config = toml.load(f)
        
        model_path = config['paths']['model_path']
        model_path = os.path.join(current_dir, model_path)
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        
        repo_id = "IndexTeam/IndexTTS-2"
        model_path = huggingface_hub.snapshot_download(
            repo_id=repo_id,
            local_dir=model_path,  # 会将文件下载到这个目录
            local_dir_use_symlinks=False  # 可选：设为 False 可避免创建符号链接，直接复制文件
        )
        return model_path
   
    @staticmethod
    def create() -> 'TTSModel':
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(current_dir, "model_config.toml")
        return TTSModel(config)
