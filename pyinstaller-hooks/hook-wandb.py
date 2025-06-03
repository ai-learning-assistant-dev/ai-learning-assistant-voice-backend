# extra-hooks/hook-wandb.py
from PyInstaller.utils.hooks import collect_data_files, copy_metadata
datas = collect_data_files('wandb', include_py_files=True, includes=['**/vendor/**/*.py'])

datas = datas + copy_metadata('wandb')
