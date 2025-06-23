import requests
import json
import time
import argparse

def call_tts_api(text, voice="glw", output_file="output.mp3", model="kokoro"):
    url = "http://localhost:8000/v1/audio/speech"
    headers = {"Content-Type": "application/json"}
    data = {
        "input": text,
        "voice": voice,
        "response_format": "mp3",
        "speed": 1.0,
        "model": model,
    }

    try:
        start_time = time.time()
        response = requests.post(url, json=data, headers=headers)
        duration = time.time() - start_time
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"音频已保存到 {output_file}，耗时 {duration:.2f}秒, 每token耗时 {duration/len(text):.2f}秒")
        else:
            print(f"请求失败: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"调用API出错: {str(e)}")

def call_get_models_info():
    url = "http://localhost:8000/v1/models/info"
    headers = {"Content-Type": "application/json"}
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers)
        duration = time.time() - start_time
        if response.status_code == 200:
            print(f"获取模型信息成功, 耗时 {duration:.2f}秒")
            print(response.json())
        else:
            print(f"请求失败: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"调用API出错: {str(e)}")

test_text = """
驻店模式比较清晰就是把类似于星巴克，麦当劳等一些商圈的店铺订单统一分发给驻店骑手配送。小队模式就是区域承包商建设的专职的达达团队，平台会把大部分订单给团队配送，大部分订单给小队的时候，骑手可提前看订单15秒，派单时也会优先派给小队骑手。订单被小队筛选后，难送的单子放到了众包平台，兼职骑手也会经过有些难送的订单诸如高层需要爬楼和医院挤电梯，偏远地区且只接一单的就被众包骑手放弃。这样的情况下，天气好的时候订单还能被小队慢慢消化，天气不好就会出现大量的订单积压。
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TTS API 测试客户端')
    parser.add_argument('--text', type=str, default=test_text, help='要合成的文本')
    parser.add_argument('--voice', type=str, default='glw', help='语音类型')
    parser.add_argument('--output', type=str, default='output.mp3', help='输出文件名')
    parser.add_argument('--model', type=str, default='kokoro', help='模型名称')
    
    # 示例调用
    call_tts_api(
        text=parser.parse_args().text,
        voice=parser.parse_args().voice,
        output_file=parser.parse_args().output,
        model=parser.parse_args().model
    )
    call_get_models_info()