import click
from models.model_manager import model_manager
from api.api_handler import app
import uvicorn

@click.group()
def cli():
    """AI TTS 命令行工具"""
    pass

@cli.command()
@click.option('--model-names', 
              required=True,
              help='要加载的模型名称列表，用逗号分隔 (如 Kokoro,Model2,Model3)')
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
    
    uvicorn.run(app, host="0.0.0.0", port=port)
    
    

if __name__ == "__main__":
    cli()