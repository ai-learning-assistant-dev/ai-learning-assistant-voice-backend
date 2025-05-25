import click
from models.model_manager import model_manager
from api.api_handler import app
import uvicorn

@click.group()
def cli():
    """AI TTS 命令行工具"""
    pass

@cli.command()
@click.option('--model-name', 
              type=click.Choice(['Kokoro']),  # 可选的模型列表
              required=True, 
              help='模型名称')
@click.option('--config', required=True, help='配置文件路径')
@click.option('--port', default=8000, help='服务端口')
def run(model_name, config, port):
    """运行TTS服务命令"""
    model_manager.load_model(model_name, config)
    uvicorn.run(app, host="0.0.0.0", port=port)
    
    

if __name__ == "__main__":
    cli()