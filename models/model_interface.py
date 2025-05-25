# models/model_interface.py
from abc import ABC, abstractmethod
import numpy as np

class ModelInfo:
    def __init__(self, model_name: str, device: str, voices: list, default_voice: str, description: str):
        self.model_name = model_name
        self.device = device
        self.voices = voices
        self.default_voice = default_voice
        self.description = description


class TTSModelInterface(ABC):
    @abstractmethod
    def synthesize(self, text: str, voice_type: str, speed: float) -> np.ndarray:
        """
        合成语音并返回音频数据
        Returns:
            audio_data: numpy数组格式的音频波形数据
        """
        pass
    
    @staticmethod
    @abstractmethod
    def create(config) -> 'TTSModelInterface':
        """Initialize the model with configuration.
        
        Returns:
            TTSModelInterface: 初始化完成的TTS模型实例
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        """Get model information."""
        pass