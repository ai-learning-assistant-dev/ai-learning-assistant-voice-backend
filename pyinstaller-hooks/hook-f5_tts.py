from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('f5_tts', includes=['*'])