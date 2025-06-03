from PyInstaller.utils.hooks import collect_all
datas, binaries, hiddenimports = collect_all('misaki', include_py_files=True, include_datas=['*'])