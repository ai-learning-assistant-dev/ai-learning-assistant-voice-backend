# Quickstart
pip install -r ./requirements.txt

pip install -r ./models/kokoro/requirements.txt

pip install -r ./models/f5-tts/requirements.txt

python ./cli.py run --model-names=kokoro,f5-tts

python ./test_client.py --model kokoro --voice zm_010 或者 zf_001

python ./test_client.py --model f5-tts --voice vmz 或者 glw
