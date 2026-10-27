"""Exercise the actual generated batch worker on isolated image fixtures."""
import ctypes as c, pathlib, json, struct, uuid, hashlib, shutil
from PIL import Image
from native_test_host import NativeHost
from test_support import prepare_fixtures
root=pathlib.Path(__file__).resolve().parent.parent;fixtures=prepare_fixtures();d=root/'tests'/'.work'/'batch-check';d.mkdir(parents=True,exist_ok=True)
sources={'a.png':fixtures/'source.png','b.jpg':fixtures/'source.jpg','c.heic':fixtures/'source.heic'}
for name,source in sources.items():shutil.copyfile(source,d/name)
(d/'z.jpg').write_bytes(b'not an image')
sentinel=d/'a_szerkesztett.png';sentinel.write_bytes(b'previous copy must survive')
before={n:(d/n).read_bytes() for n in [*sources,'z.jpg']}
host=NativeHost();ole=c.OleDLL('ole32');ole.CoInitializeEx(None,2)
class GUID(c.Structure):_fields_=[('bytes',c.c_ubyte*16)]
def guid(v):return GUID.from_buffer_copy(uuid.UUID(v).bytes_le)
def method(obj,index,restype,*args):return c.WINFUNCTYPE(restype,c.c_void_p,*args)(c.cast(obj,c.POINTER(c.POINTER(c.c_void_p))).contents[index])
factory=c.c_void_p();cls=guid('cacaf262-9370-4615-a13b-9f5539da4c0a');iid=guid('ec5ec8a9-c395-4314-9c77-54d7a935ff70');ole.CoCreateInstance(c.byref(cls),None,1,c.byref(iid),c.byref(factory));host.put('factory',factory.value)
def names():return [c.wstring_at(host.addr('images',i*1056)) for i in range(host.get('imagecount'))]
def select_originals():
    host.call('memzero',host.addr('batchselection'),16384*8);ns=names()
    for i,n in enumerate(ns):host.put('batchselection',int(n in before),i*8)
    host.put('batchcount',len(before));host.put('batchhaspreset',1);c.memmove(host.addr('batchvalues'),struct.pack('<9q',-2,28,22,8,4,18,-4,0,4),72)
def run(copy):
    host.call('batchstartjob',int(copy))
    for _ in range(host.get('imagecount')+3):
        host.call('batchstep')
        if host.get('batchdone'):break
    assert host.get('batchdone')==1
    assert (host.get('batchprocessed'),host.get('batchfailed'))==(3,1),(host.get('batchprocessed'),host.get('batchfailed'),host.readwide('batcherrorpath'))
try:
    host.wide('path',d);host.call('loadfolder');host.put('clientw',1240);host.put('clienth',800);host.call('layout')
    # Checkbox hit testing consumes the click instead of opening the picture.
    assert host.call('batchclick',304+186-24,148+24)==1
    assert host.get('batchcount')==1 and host.get('mode')==0
    host.call('batchselectall',0);assert host.get('batchcount')==0
    # Built-in installation keeps an existing user preset intact.
    host.wide('edpresetpath',d/'test-presets.json');host.wide('edpresettemppath',d/'test-presets.json.tmp');host.put('edpresetcount',0);host.call('batchensurepresets')
    assert host.get('edpresetcount')==3
    presets=json.loads((d/'test-presets.json').read_text(encoding='utf8'));assert [p['name'] for p in presets['presets']]==['kodacolor 400','kodacolor 800','kodachome 64']
    select_originals();ns=names();host.put('batchselection',0,ns.index('z.jpg')*8);host.put('batchselection',0,ns.index('c.heic')*8);host.put('batchcount',2);host.put('batchgeneration',1);host.put('batchscan',0)
    for _ in range(len(ns)+2):host.call('batchpreview')
    assert host.get('batchversions',ns.index('a.png')*8)==1
    assert host.get('batchversions',ns.index('b.jpg')*8)==1
    host.put('batchselection',0,ns.index('a.png')*8);host.put('batchgeneration',2);host.put('batchscan',0)
    for _ in range(len(ns)+2):host.call('batchpreview')
    assert host.get('batchversions',ns.index('a.png')*8)==0
    assert host.get('batchversions',ns.index('b.jpg')*8)==2
    print('PASS: checkbox hit testing, built-ins, selected previews and deselection restoration.')
    select_originals();run(True)
    assert all((d/n).read_bytes()==b for n,b in before.items())
    assert sentinel.read_bytes()==b'previous copy must survive'
    pngs=sorted(d.glob('a_szerkesztett_*.png'));assert pngs
    saved=Image.open(pngs[-1]).convert('RGBA');original=Image.open(d/'a.png').convert('RGBA');assert saved.size==original.size and saved.tobytes()!=original.tobytes();assert saved.getchannel('A').tobytes()==original.getchannel('A').tobytes()
    for name in ['b_szerkesztett.jpg','c_szerkesztett.heic']:assert (d/name).exists()
    print('PASS: three batch copies, automatic collision suffix, originals untouched, corrupt input counted and PNG alpha preserved.')
    host.put('batchdone',0);select_originals();run(False)
    assert all((d/n).read_bytes()!=before[n] for n in sources)
    assert (d/'z.jpg').read_bytes()==before['z.jpg']
    print('PASS: automatic PNG/JPEG/HEIC batch overwrite and failure isolation.')
    for n,b in before.items():(d/n).write_bytes(b)
    host.put('batchdone',0);select_originals();host.call('batchstartjob',1);host.call('batchstep');host.put('batchcancelled',1);host.call('batchstep')
    assert host.get('batchdone')==1 and host.get('batchprocessed')==1 and host.get('batchfailed')==0
    assert all((d/n).read_bytes()==b for n,b in before.items())
    print('PASS: cancellation finishes the current image and leaves remaining originals unchanged.')
    # Simulate an unavailable HEIF encoder only inside this private test mapping.
    # Other formats still call the same real generated encoding routine.
    address=host.addr('editorencode');original_entry=c.string_at(address,12)
    def encode_proxy():
        if host.readwide('edtarget').lower().endswith(('.heic','.heif')):
            host.put('edencoded',0);host.put('error',host.addr('edcodecfailed'));return 0
        c.memmove(address,original_entry,12)
        try:return host.call('editorencode')
        finally:c.memmove(address,jump,12)
    proxy=c.WINFUNCTYPE(c.c_uint64)(encode_proxy);jump=b'\x48\xb8'+struct.pack('<Q',c.cast(proxy,c.c_void_p).value)+b'\xff\xe0'
    c.memmove(address,jump,12)
    host.put('batchdone',0);select_originals();ns=names()
    for i,n in enumerate(ns):host.put('batchselection',int(n=='c.heic'),i*8)
    host.put('batchcount',1);host.call('batchstartjob',1)
    for _ in range(len(ns)+3):
        host.call('batchstep')
        if host.get('batchdone'):break
    c.memmove(address,original_entry,12)
    assert host.get('batchprocessed')==1 and host.get('batchfailed')==0
    assert list(d.glob('c_szerkesztett*.png')) and (d/'c.heic').read_bytes()==before['c.heic']
    print('PASS: automatic HEIC-to-PNG copy fallback when the HEIF encoder is unavailable.')
finally:
    for n,b in before.items():(d/n).write_bytes(b)
    method(factory,2,c.c_ulong)(factory);ole.CoUninitialize();host.close()
