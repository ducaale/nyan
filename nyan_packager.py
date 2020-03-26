# https://github.com/kitao/pyxel/blob/master/pyxel/packager.py

import argparse
import os
import platform
import shutil
import tempfile

import PyInstaller.__main__

parser = argparse.ArgumentParser(description="nyan Packager")
parser.add_argument(
    "python_file", type=argparse.FileType(), help="nyan program file entry point"
)
args = parser.parse_args()

dirname = os.path.dirname(args.python_file.name) or "."
filename = os.path.basename(args.python_file.name)
name = os.path.splitext(filename)[0]

original_cwd = os.getcwd()
os.chdir(dirname)

assets_src = os.path.join(dirname, 'assets', '*.png')
assets_dest = 'assets'
separator = ";" if platform.system() == "Windows" else ":"

options = [
    '--clean',
    f'--name={name}',
    '--windowed',
    '--log-level=ERROR',
    '--distpath=dist',
    f'--workpath={tempfile.gettempdir()}',
    f'--add-data={assets_src}{separator}{assets_dest}',
    os.path.join(filename),
]

PyInstaller.__main__.run(options)

spec_file = os.path.join(original_cwd, f'{name}.spec')
if os.path.exists(spec_file):
    os.remove(spec_file)
