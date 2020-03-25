# https://github.com/kitao/pyxel/blob/master/pyxel/packager.py

import argparse
import os
import platform
import tempfile

import PyInstaller.__main__

parser = argparse.ArgumentParser(description="Nyan Packager")
parser.add_argument(
    "python_file", type=argparse.FileType(), help="Nyan program file entry point"
)
args = parser.parse_args()

dirname = os.path.dirname(args.python_file.name) or "."
filename = os.path.basename(args.python_file.name)
name = os.path.splitext(filename)[0]

os.chdir(dirname)

assets_src = os.path.join(dirname, 'assets', '*.png')
assets_dest = 'assets'
separator = ";" if platform.system() == "Windows" else ":"

options = [
    '--clean',
    f'--name={name}',
    '--windowed',
    '--log-level=ERROR',
    f'--distpath={os.path.join(os.path.abspath("."), "dist")}',
    f'--workpath={tempfile.gettempdir()}',
    f'--add-data={assets_src}{separator}{assets_dest}',
    os.path.join(filename),
]

PyInstaller.__main__.run(options)