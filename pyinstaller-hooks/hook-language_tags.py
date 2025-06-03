
from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('language_tags', include_py_files=True, includes=['**/*.json'])