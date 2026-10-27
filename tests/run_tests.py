"""Build a separate test executable and run the native Windows test suite."""
import argparse
from pathlib import Path
import subprocess
import sys
import struct
from test_support import heic_fixture, prepare_fixtures

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download-fixtures', action='store_true',
                        help='Download the public libheif sample if no local HEIC fixture exists.')
    args = parser.parse_args()
    if sys.platform != 'win32' or struct.calcsize('P') != 8:
        parser.error('The native test suite requires Windows x64 and 64-bit Python.')
    root = Path(__file__).resolve().parent.parent
    heic_fixture(download=args.download_fixtures)
    prepare_fixtures()
    commands = [
        [root / 'src' / 'make_binary.py', 'Gallery.check.exe'],
        [root / 'tests' / 'test_editor_pixels.py'],
        [root / 'tests' / 'test_editor_io.py'],
        [root / 'tests' / 'test_settings.py'],
        [root / 'tests' / 'test_batch.py'],
    ]
    for command in commands:
        subprocess.run([sys.executable, *map(str, command)], cwd=root, check=True)
    print('All native tests passed.')

if __name__ == '__main__':
    main()
