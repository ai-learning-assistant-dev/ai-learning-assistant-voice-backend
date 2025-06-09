import click
from models.model_manager import model_manager
from api.api_handler import app
import uvicorn
import logging
import traceback

def setup_logging(level):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

# 调用函数设置日志级别
setup_logging(logging.INFO)

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
              required=True,
              help='要加载的模型名称列表，用逗号分隔 (如 kokoro,f5-tts)')
@click.option('--port', default=8000, help='服务端口')
def run(model_names, port):
    """运行TTS服务命令，支持加载多个模型"""
    models = [name.strip() for name in model_names.split(',')]
    
    for model_name in models:
        try:
            model_manager.load_model(model_name)
            click.echo(f"成功加载模型: {model_name}")
        except Exception as e:
            click.echo(f"加载模型 {model_name} 失败: {str(e)}", err=True)
            logging.error(traceback.format_exc())  # 打印完整栈信息
            
    
    uvicorn.run(app, host="0.0.0.0", port=port)

@cli.command()
@click.option('--model-names', 
              required=True,
              help='要加载的模型名称列表，用逗号分隔 (如 kokoro,f5-tts)')
def warm_up(model_names):
    """预热TTS服务命令，支持加载多个模型，解决打出来的docker包第一次运行时还需要从网上下载文件的问题"""
    models = [name.strip() for name in model_names.split(',')]
    
    for model_name in models:
        try:
            model_manager.load_model(model_name)
            click.echo(f"成功加载模型: {model_name}")
        except Exception as e:
            click.echo(f"加载模型 {model_name} 失败: {str(e)}", err=True)
            logging.error(traceback.format_exc())  # 打印完整栈信息
    
    

if __name__ == "__main__":
    cli()