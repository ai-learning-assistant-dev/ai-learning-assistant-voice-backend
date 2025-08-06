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

# test_text = """
# 我们今天讲主义主义的4-1-2-3，那代表人物呢。P代表人物是P。啊，当然呢代表任物呢也可以是L。如果我们想要具体知道这个话，我们应该是去看P的传记和P的。P写的东西呃，然后这个那是P交汇L的哎，。好，但是说呃这个russia的这个呃所谓的，我们更确切的应该把它叫做。啊C呃，公传的C主义，而不是啊。Legal的 legal的哎呀。哎呀，很多东西不能说，你知道吗？这个主一主意，反正我只能浮光掠影的给你讲一讲。那么这个就是。我把这个叫做正派青年的交友啊和团结啊。我们正派的青年，大家要互相做朋友，要团结起来。.嗯，呃但我说那个时代他们的中心人物啊很多都是被被开除的。但是我要强调一点，他们被开除的原因不是在学校里面小打小闹啊，不是在学校里小打小闹。呃，就以L作作为他哥，这我觉得这种人物都要献祭个哥啊，感觉。就刘秀献祭他哥刘敏是吧，那个字是念敏吧，哎呦有献祭个哥，不是献祭的意思，你能让他坚强一点。,u.你要是念念这个刘衍是吧，刘影还是演刘影应该是刘衍啊，字刘博生那同样的。但是说但是他哥的那那些同伴啊，他都是这个啊。呃，就是不是相信workermen，是相信这个farmer啊，不是相信worker，相信farmeralexander。他现在是farmer，那么这个logg呢，他就是混圈子啊，怎么怎么地的，然后是什么，反正就是哎我要讲的就是怎么来。中心人物啊往往是被开除，包括LL自己被开除，但是他成绩好，最后百般奔走，包括他老妈也是什么，他老爸是什么教育，一个省的，相当于。教育厅长啊，不就就是下下面具体执行任务的啊，所以呢还是给他面子啊，还是给他面子啊。就藏的很深啊，就是藏要藏的深，一定要藏的深，藏的深。永远不要公平呃，永远不要公平，永远不要公平啊。公平嘲讽啊啊那这互相交朋友，怎么能可以公平嘲讽别人呢？永远不要公平嘲讽。这个log格呢，他后来去这个呃这个peter book啊，peter的一个城市啊，由peter命名的一个城市，到那个城市里面，那个城市有点类似于我们的魔都啊。到里面去，有天晚上去呃去参加一个party。然后这这个party里面，他听上面有个老哥演讲，讲的东西太太拙劣了，太令人发指了。那他就由他上去。啊，当然这是学习能力很强，他读了好多书，由他上去来一讲，讲的他轰动的。然后当时很多对于这个这个啊。啊，这个SD啊对于这个SD感兴趣的人也欢欣鼓舞，小拳都捏起来了。他讲的那些讲的激动的不得了，全都都捏起来了。但是他讲完之后就后悔了。因为他抛头露面了，因为他抛头露面，因为他哥都是因为这个原因被枪毙呃，被枪毙，我不知道还是绞刑，应该是绞刑的。所以呢他始终是被就是被看着的，被看着的啊，所以。要藏的深越深越好越深越好越深越好啊，藏的越深越好。然后我要说的，为什么代表人物是P呢？所以我要就是说就是说这个工作的这一实践，这一工作的口诀就就这么简单，口诀就这么简单。由于它是灌输论啊，那就是。给一个人很多观念，给一个人很多观念，然后给两个人。啊，很多很多观念，然后给三个人很多很的观念。那么你们这些人呢就形成一个观念上的呃都比较富足的啊共同体。这个观念上非常富足的共同体，下面要做的就是给许多人，给许多许多人一个观念。啊，你们要有一定要中心化，所以说必须是中心化的，因为你们必须得磋商，而且你必须是拧成一股神，有主心骨的，有一个最强的人过来拍板的，要有他决策权的。你们前期起效的就是要给许多许多人一个观点，往往这个观念是经济观念，经济上的。啊，就是一些小利啊一些小利。比如说星期六早点下班，让他去洗澡啊，新经济上的一些小利这些观点。还有一个观点就是尊严上的观念，最重要的是尊严。啊，最重要比如说你和老你老板是平等的嗯，平等的，你只要给一个观点就行了。
# """

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