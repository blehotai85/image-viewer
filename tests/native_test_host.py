"""Development-only host for calling our own generated native routines."""
import ctypes as c, json, struct, pathlib
class NativeHost:
    def __init__(self,name='Gallery.check.exe'):
        root=pathlib.Path(__file__).resolve().parent.parent;data=(root/name).read_bytes();self.symbols=json.loads((root/(pathlib.Path(name).stem+'.map.json')).read_text())['symbols']
        pe=struct.unpack_from('<I',data,60)[0];opt=pe+24;size=struct.unpack_from('<I',data,opt+56)[0]
        self.kernel=c.WinDLL('kernel32',use_last_error=True);self.kernel.VirtualAlloc.restype=c.c_void_p;self.kernel.VirtualAlloc.argtypes=[c.c_void_p,c.c_size_t,c.c_uint32,c.c_uint32];self.kernel.VirtualFree.argtypes=[c.c_void_p,c.c_size_t,c.c_uint32]
        self.base=self.kernel.VirtualAlloc(None,size,0x3000,0x40);assert self.base,c.get_last_error();self.dlls={}
        for i in range(struct.unpack_from('<H',data,pe+6)[0]):
            vsize,rva,rawsize,raw=struct.unpack_from('<IIII',data,opt+240+i*40+8);c.memmove(self.base+rva,data[raw:raw+rawsize],rawsize)
        for name,rva in self.symbols.items():
            if not name.startswith('IAT:'):continue
            dll,fn=name[4:].split('!');module=self.dlls.setdefault(dll,c.WinDLL(dll));c.c_void_p.from_address(self.base+rva).value=c.cast(getattr(module,fn),c.c_void_p).value
    def addr(self,n,off=0):return self.base+self.symbols[n]+off
    def put(self,n,value,off=0):c.c_int64.from_address(self.addr(n,off)).value=value
    def get(self,n,off=0):return c.c_uint64.from_address(self.addr(n,off)).value
    def wide(self,n,value):
        b=(str(value)+'\0').encode('utf-16le');c.memmove(self.addr(n),b,len(b))
    def readwide(self,n):return c.wstring_at(self.addr(n))
    def call(self,n,*args):return c.WINFUNCTYPE(c.c_uint64,*([c.c_uint64]*len(args)))(self.addr(n))(*args)
    def close(self):self.kernel.VirtualFree(self.base,0,0x8000)
