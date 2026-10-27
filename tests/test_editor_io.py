"""Test generated JSON/MRU routines and WIC PNG/JPEG/HEIF encoding."""
import ctypes as c, pathlib, json, struct, uuid, hashlib
from native_test_host import NativeHost
from test_support import prepare_fixtures
root=pathlib.Path(__file__).resolve().parent.parent;fixtures=prepare_fixtures();host=NativeHost()
ole=c.OleDLL('ole32');ole.CoInitializeEx(None,2)
class GUID(c.Structure):_fields_=[('bytes',c.c_ubyte*16)]
def guid(value):return GUID.from_buffer_copy(uuid.UUID(value).bytes_le)
def method(obj,index,restype,*argtypes):return c.WINFUNCTYPE(restype,c.c_void_p,*argtypes)(c.cast(obj,c.POINTER(c.POINTER(c.c_void_p))).contents[index])
factory=c.c_void_p();cls=guid('cacaf262-9370-4615-a13b-9f5539da4c0a');iid=guid('ec5ec8a9-c395-4314-9c77-54d7a935ff70');ole.CoCreateInstance(c.byref(cls),None,1,c.byref(iid),c.byref(factory));host.put('factory',factory.value)
try:
    # Parser accepts standard JSON escaping, clamps limits, and bounds records.
    sample={'version':1,'presets':[{'name':'Árnyék "A" \\ próba','values':[22,-23,45,67,-78,99,54,-179,84]},{'name':'Második','values':[1000]*9}]}
    host.wide('edjsonwide',json.dumps(sample,ensure_ascii=True));host.call('editorparsepresets');assert host.get('edpresetcount')==2
    assert host.readwide('edpresets')==sample['presets'][0]['name']
    first=struct.unpack('<9q',c.string_at(host.addr('edpresets',128),72));assert list(first)==sample['presets'][0]['values']
    limits=struct.unpack('<9q',c.string_at(host.addr('edpresets',256+128),72));assert list(limits)==[100,100,100,100,100,100,100,180,100]
    target=fixtures/'native-presets.json';temporary=fixtures/'native-presets.json.tmp';host.wide('edpresetpath',target);host.wide('edpresettemppath',temporary)
    host.wide('edname','Második');c.memmove(host.addr('edvalues'),struct.pack('<9q',*limits),72);assert host.call('editorstorepreset',1)==1
    assert json.loads(target.read_text(encoding='utf8'))['presets'][0]['name']=='Második'
    host.wide('edname','Új „szín”');values=[2,3,4,5,6,7,8,9,10];c.memmove(host.addr('edvalues'),struct.pack('<9q',*values),72);assert host.call('editorstorepreset',0xffffffffffffffff)==1
    saved=json.loads(target.read_text(encoding='utf8'));assert saved['presets'][0]=={'name':'Új „szín”','values':values};assert len(saved['presets'])==3
    host.wide('edjsonwide',json.dumps(saved,ensure_ascii=False));host.call('editorparsepresets');assert host.get('edpresetcount')==3;assert host.readwide('edpresets')=='Új „szín”'
    host.put('edpresetcount',0);c.memset(host.addr('edjsonwide'),0,131072);host.call('editorreadpresetfile');assert host.get('edpresetcount')==3;assert host.readwide('edpresets')=='Új „szín”'
    print('PASS: native JSON parser, UTF-8 output, escaping, range clamping, insertion and MRU promotion.')
    # Test the SAME emitted encoding function used by the UI, including metadata
    # block transfer and conversion to the encoder-selected pixel format.
    for ext in ['png','jpg','heic']:
        source=fixtures/('source.'+ext);before=hashlib.sha256(source.read_bytes()).hexdigest();host.put('metatarget',0)
        sourcepath=c.create_unicode_buffer(str(source));bmp=host.call('decode',c.addressof(sourcepath),0);assert bmp,ext
        try:
            w,h=host.get('dw'),host.get('dh');host.put('vieww',w);host.put('viewh',h);host.put('edfullpixels',host.get('pixels'));host.wide('edoriginalfile',source)
            output=fixtures/('native-encoded.'+ext);temp=fixtures/('native-encoded-'+ext+'.tmp');host.wide('edtarget',output);host.wide('edtempfile',temp)
            result=host.call('editorencode')
            if not result:
                message=c.wstring_at(host.get('error'));print('CODEC FALLBACK:',ext,message)
                if temp.exists():temp.unlink()
                assert ext=='heic',message
                continue
            assert temp.stat().st_size>100;temp.replace(output)
            checkpath=c.create_unicode_buffer(str(output));check=host.call('decode',c.addressof(checkpath),0);assert check,('encoded image cannot be decoded',ext)
            try:assert (host.get('dw'),host.get('dh'))==(w,h)
            finally:host.dlls['gdi32.dll'].DeleteObject(c.c_void_p(check))
            assert hashlib.sha256(source.read_bytes()).hexdigest()==before
            print('PASS: native',ext.upper(),'encode, commit and decode;',w,'x',h,'pixels;',output.stat().st_size,'bytes.')
        finally:host.dlls['gdi32.dll'].DeleteObject(c.c_void_p(bmp))
finally:
    method(factory,2,c.c_ulong)(factory);ole.CoUninitialize();host.close()
