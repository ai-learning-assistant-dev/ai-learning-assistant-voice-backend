# This script builds the Python application using PyInstaller.
pyinstaller cli.py --clean --noconfirm \
    --hidden-import models.kokoro.handler \
    --hidden-import models.f5-tts.handler \
    --hidden-import en_core_web_sm \
    --add-data "models/kokoro:models/kokoro" \
    --add-data "models/f5-tts:models/f5-tts" \
    --additional-hooks-dir pyinstaller-hooks
cp start_exe.sh.sample dist/start_exe.sh
#REM test distribution
./dist/cli/cli.app run --model-names=kokoro,f5-tts