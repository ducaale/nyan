# https://github.com/kitao/pyxel/blob/master/pyxel/packager.py

import argparse
import os
import platform
import shutil
import warnings

import PyInstaller.__main__
warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    parser = argparse.ArgumentParser(description='nyan Packager')
    parser.add_argument(
        'python_file', type=argparse.FileType(), help='nyan program file entry point'
    )
    parser.add_argument(
        '-i', '--icon', type=argparse.FileType(), help='nyan program icon file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', help='enable console output'
    )
    parser.add_argument(
        '-f', '--onefile', action='store_true'
    )
    args = parser.parse_args()

    dirname = os.path.dirname(args.python_file.name) or "."
    filename = os.path.basename(args.python_file.name)
    name = os.path.splitext(filename)[0]

    original_cwd = os.getcwd()
    os.chdir(dirname)

    options = [
        '--clean',
        f'--name={name}',
        '--log-level=ERROR',
        '--distpath=dist',
        os.path.join(filename),
    ]

    if args.onefile:
        options.append('--onefile')
        if os.path.exists('assets'):
            shutil.copytree('assets', os.path.join('dist', 'assets'))
    else:
        options.append('--onedir')
        if os.path.exists('assets'):
            assets_src = os.path.join(dirname, 'assets')
            assets_dest = 'assets'
            separator = ';' if platform.system() == 'Windows' else ':'

            options.append(f'--add-data={assets_src}{separator}{assets_dest}')

    if not args.debug:
        options.append('--windowed')

    if args.icon:
        options.append(f'--icon={args.icon.name}')

    PyInstaller.__main__.run(options)

    build_path = os.path.join(original_cwd, 'build')
    shutil.rmtree(build_path, ignore_errors=True)

    spec_file = os.path.join(original_cwd, f'{name}.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)

if __name__ == "__main__":
    run()