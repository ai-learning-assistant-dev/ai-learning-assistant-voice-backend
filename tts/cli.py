import os
import click
from models.model_manager import model_manager
from api.api_handler import app
import uvicorn
import logging
import traceback
import torch
import subprocess

def setup_logging(level):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

# 调用函数设置日志级别
setup_logging(logging.INFO)

def detect_cuda_environment():
    """检测CUDA环境是否可用"""
    try:
        # 检查PyTorch是否支持CUDA
        if torch.cuda.is_available():
            logging.info(f"检测到CUDA环境，GPU数量: {torch.cuda.device_count()}")
            return True
        else:
            logging.info("PyTorch未检测到CUDA环境")
            return False
    except Exception as e:
        logging.warning(f"CUDA检测失败: {e}")
        
    # 备用检测方法：使用nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            logging.info("通过nvidia-smi检测到CUDA环境")
            return True
        else:
            logging.info("nvidia-smi执行失败，判断为CPU环境")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        logging.info(f"nvidia-smi不可用: {e}")
        return False

def auto_select_model():
    """根据CUDA环境自动选择合适的TTS模型"""
    cuda_available = detect_cuda_environment()
    
    if cuda_available:
        selected_model = "index-tts"
        logging.info(f"CUDA环境可用，自动选择模型: {selected_model}")
    else:
        selected_model = "kokoro"
        logging.info(f"CUDA环境不可用，自动选择CPU模型: {selected_model}")
    
    return selected_model

@click.group()
def cli():
    """AI TTS 命令行工具"""
    pass

@cli.command()
@click.option('--model-names', 
              required=True,
              help='要下载的模型名称列表，用逗号分隔 (如 kokoro,f5-tts)')
def download(model_names):
    """下载模型及相关音色资源"""
    models = [name.strip() for name in model_names.split(',')]
    
    for model_name in models:
        try:
            path = model_manager.download_model(model_name)
            click.echo(f"成功下载模型: {model_name}，路径: {path}")
        except Exception as e:
            click.echo(f"下载模型 {model_name} 失败: {str(e)}", err=True)
            logging.error(traceback.format_exc())  # 打印完整栈信息

@cli.command()
@click.option('--model-names', 
              required=False,
              help='要加载的模型名称列表，用逗号分隔 (如 kokoro,f5-tts)。如果不指定，将自动检测CUDA环境选择模型')
@click.option('--port', default=8000, type=int, help='服务端口')
@click.option('--auto-detect', is_flag=True, default=False, help='自动检测CUDA环境并选择合适的模型')
def run(model_names, port, auto_detect):
    """运行TTS服务命令，支持加载多个模型或自动选择模型"""
    
    # 如果启用了自动检测模式或未指定模型名称，则自动选择
    if auto_detect or not model_names:
        if model_names:
            click.echo("同时指定了模型名称和自动检测，将优先使用自动检测")
        selected_model = auto_select_model()
        models = [selected_model]
        click.echo(f"自动选择的模型: {selected_model}")
    else:
        models = [name.strip() for name in model_names.split(',')]
        click.echo(f"手动指定的模型: {', '.join(models)}")
    
    for model_name in models:
        try:
            model_manager.load_model(model_name)
            click.echo(f"成功加载模型: {model_name}")
        except Exception as e:
            click.echo(f"加载模型 {model_name} 失败: {str(e)}", err=True)
            logging.error(traceback.format_exc())  # 打印完整栈信息
            
    
    uvicorn.run(app, host="0.0.0.0", port=port)
    
    

if __name__ == "__main__":
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    cli()