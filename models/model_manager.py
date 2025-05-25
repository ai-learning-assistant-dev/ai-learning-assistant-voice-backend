# models/model_loader.py
import importlib
import logging
from models.model_interface import TTSModelInterface


class ModelManager:
    def __init__(self):
        self._models = {}  # 模型名称到实例的映射
    
    def get_model(self, model_name: str) -> TTSModelInterface:
        """获取模型实例"""
        if model_name not in self._models:
            raise ValueError(f"模型{model_name}未加载")
        return self._models[model_name]
    
    def load_model(self, model_name: str, config):
        """动态加载并初始化模型"""
        if model_name in self._models:
            logging.warning(f"模型{model_name}已加载，无需重复加载")
        try:
            module = importlib.import_module(f"models.{model_name.lower()}.handler")
            model_class = getattr(module, f"{model_name}TTSModel")
            if not issubclass(model_class, TTSModelInterface):
                raise TypeError(f"{model_name}TTSModel必须实现TTSModelInterface")
            self._models[model_name] = model_class.create(config)  # 调用静态方法创建实例 
        except (ImportError, AttributeError) as e:
            raise ValueError(f"加载模型{model_name}失败: {e}")

model_manager = ModelManager()  # 全局实例