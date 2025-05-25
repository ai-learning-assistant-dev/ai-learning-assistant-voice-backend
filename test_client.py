import requests
import json
import time

def call_tts_api(text, voice="zf_001", output_file="output.mp3"):
    url = "http://localhost:8000/v1/audio/speech"
    headers = {"Content-Type": "application/json"}
    data = {
        "input": text,
        "voice": voice,
        "response_format": "mp3",
        "speed": 1.0
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

if __name__ == "__main__":
    # 示例调用
    call_tts_api(
        text="这是一个测试文本，用于验证TTS服务的功能是否正常。",
        voice="zf_001",
        output_file="test_output.mp3"
    )