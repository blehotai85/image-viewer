"""Generate synthetic fixtures; keep downloaded HEIC data out of version control."""
from pathlib import Path
import os
import shutil

TESTS = Path(__file__).resolve().parent
WORK = TESTS / '.work'
HEIC_URL = 'https://raw.githubusercontent.com/strukturag/libheif/master/examples/example.heic'

def heic_fixture(download=False):
    cache = WORK / 'input' / 'example.heic'
    external = os.environ.get('GALLERY_HEIC_FIXTURE')
    if external:
        source = Path(external).expanduser().resolve()
        if not source.is_file():
            raise RuntimeError('GALLERY_HEIC_FIXTURE must point to an existing HEIC file.')
        cache.parent.mkdir(parents=True, exist_ok=True)
        if source != cache.resolve():
            shutil.copyfile(source, cache)
    if not cache.exists() and download:
        import urllib.request
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(HEIC_URL, timeout=30) as response:
            data = response.read(16 * 1024 * 1024 + 1)
        if len(data) > 16 * 1024 * 1024:
            raise RuntimeError('HEIC fixture download exceeded the size limit.')
        cache.write_bytes(data)
    if not cache.is_file():
        raise RuntimeError('HEIC fixture missing. Run tests/run_tests.py --download-fixtures '
                           'or set GALLERY_HEIC_FIXTURE to a local HEIC image.')
    return cache

def prepare_fixtures():
    from PIL import Image, TiffImagePlugin
    source = heic_fixture()
    output = WORK / 'editor-check'
    output.mkdir(parents=True, exist_ok=True)
    image = Image.new('RGBA', (360, 240))
    image.putdata([(x * 255 // 359, y * 255 // 239, (x * 7 + y * 11) % 256,
                    128 if x < 20 else 255) for y in range(240) for x in range(360)])
    image.save(output / 'source.png')
    exif = Image.Exif()
    exif[271] = 'Codex'
    exif[272] = 'Editor Test'
    exif[34665] = {36867: '2026:10:27 11:12:13',
                   33437: TiffImagePlugin.IFDRational(56, 10), 34855: 640}
    image.convert('RGB').save(output / 'source.jpg', quality=95, exif=exif)
    shutil.copyfile(source, output / 'source.heic')
    return output
