"""Write a native AMD64 PE directly. No compiler, assembler, linker or runtime.

Only Python's standard library is used to emit bytes. The resulting executable
imports Windows USER32/GDI32/KERNEL32/OLE32 and uses WIC COM interfaces.
"""
import struct, pathlib, uuid, json, sys

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
def u32(v): return struct.pack('<I', v & 0xffffffff)
def u64(v): return struct.pack('<Q', v & 0xffffffffffffffff)
def align(v, a): return (v+a-1)&-a

# Register operands and symbolic RIP-relative operands.
rax,rcx,rdx,rbx,rsp,rbp,rsi,rdi,r8,r9,r10,r11,r12,r13,r14,r15=range(16)
def R(r): return ('r',r)
def G(n,off=0): return ('g',n,off)
def A(n,off=0): return ('a',n,off)
class Emitter:
    def __init__(self): self.code=bytearray(); self.labels={}; self.fix=[]; self.imports={}; self.seq=0
    def b(self,*a): self.code.extend(a)
    def raw(self,a): self.code.extend(a)
    def label(self,n):
        assert n not in self.labels,n
        self.labels[n]=len(self.code)
    def unique(self,p='L'): self.seq+=1; return p+str(self.seq)
    def rex(self,w=1,r=0,b=0): self.b(0x40|(w<<3)|((r>>3)<<2)|(b>>3))
    def mod(self,reg,base,disp=0):
        self.b(0x80|((reg&7)<<3)|(base&7))
        if base&7==4: self.b(0x24)
        self.raw(u32(disp))
    def rip(self,reg,n,off=0):
        self.b(((reg&7)<<3)|5); self.fix.append((len(self.code),n,off)); self.raw(b'\0'*4)
    def imm(self,r,v,w=1):
        if w: self.rex(1,b=r); self.b(0xb8+(r&7)); self.raw(u64(v))
        else:
            if r>=8:self.rex(0,b=r)
            self.b(0xb8+(r&7)); self.raw(u32(v))
    def mov(self,d,s,w=1): self.rex(w,r=s,b=d); self.b(0x89,0xc0|((s&7)<<3)|(d&7))
    def load(self,d,base,off=0,w=1): self.rex(w,r=d,b=base); self.b(0x8b); self.mod(d,base,off)
    def store(self,base,off,s,w=1): self.rex(w,r=s,b=base); self.b(0x89); self.mod(s,base,off)
    def get(self,r,n,off=0,w=1): self.rex(w,r=r); self.b(0x8b); self.rip(r,n,off)
    def put(self,n,r,off=0,w=1): self.rex(w,r=r); self.b(0x89); self.rip(r,n,off)
    def lea(self,r,n,off=0): self.rex(1,r=r); self.b(0x8d); self.rip(r,n,off)
    def memlea(self,r,base,off=0): self.rex(1,r=r,b=base);self.b(0x8d);self.mod(r,base,off)
    def val(self,r,v):
        if isinstance(v,tuple):
            if v[0]=='r': self.mov(r,v[1])
            elif v[0]=='g': self.get(r,v[1],v[2])
            elif v[0]=='a': self.lea(r,v[1],v[2])
        else:self.imm(r,v)
    def set(self,n,v,off=0,w=1): self.val(rax,v); self.put(n,rax,off,w)
    def op(self,code,d,s,w=1): self.rex(w,r=s,b=d);self.b(code,0xc0|((s&7)<<3)|(d&7))
    def add(self,d,s): self.op(0x01,d,s)
    def sub(self,d,s): self.op(0x29,d,s)
    def cmp(self,d,s,w=1): self.op(0x39,d,s,w)
    def test(self,d,w=1): self.op(0x85,d,d,w)
    def ai(self,r,v,kind=0): self.rex(1,b=r);self.b(0x81,0xc0|(kind<<3)|(r&7));self.raw(u32(v))
    def addi(self,r,v): self.ai(r,v)
    def subi(self,r,v): self.ai(r,v,5)
    def cmpi(self,r,v): self.ai(r,v,7)
    def andi(self,r,v): self.ai(r,v,4)
    def shift(self,r,v,kind=7): self.rex(1,b=r);self.b(0xc1,0xc0|(kind<<3)|(r&7),v)
    def mul(self,d,s,v=None):
        self.rex(1,r=d,b=s)
        if v is None:self.b(0x0f,0xaf,0xc0|((d&7)<<3)|(s&7))
        else:self.b(0x69,0xc0|((d&7)<<3)|(s&7));self.raw(u32(v))
    def div(self,r): self.b(0x48,0x99); self.rex(1,b=r);self.b(0xf7,0xf8|(r&7))
    def jump(self,n,cond=None):
        if cond is None:self.b(0xe9)
        else:self.b(0x0f,{'e':0x84,'ne':0x85,'l':0x8c,'ge':0x8d,'le':0x8e,'g':0x8f,'s':0x88,'ns':0x89,'b':0x82,'ae':0x83}[cond])
        self.fix.append((len(self.code),n,0));self.raw(b'\0'*4)
    def begin(self,n):
        self.label(n)
        for r in [rbx,rsi,rdi,r12,r13,r14,r15]:
            if r>=8:self.b(0x41)
            self.b(0x50+(r&7))
        self.subi(rsp,0x200)
    def ret(self):
        self.addi(rsp,0x200)
        for r in [r15,r14,r13,r12,rdi,rsi,rbx]:
            if r>=8:self.b(0x41)
            self.b(0x58+(r&7))
        self.b(0xc3)
    def args(self,args):
        # Stage values before setting argument registers (no register alias hazards).
        for i,a in enumerate(args):
            if isinstance(a,tuple) and a[0]=='r':self.store(rsp,0x80+i*8,a[1])
        for i,a in enumerate(args):
            if not (isinstance(a,tuple) and a[0]=='r'):self.val(rax,a);self.store(rsp,0x80+i*8,rax)
        for i in range(len(args)):
            if i<4:self.load([rcx,rdx,r8,r9][i],rsp,0x80+i*8)
            else:self.load(rax,rsp,0x80+i*8);self.store(rsp,0x20+(i-4)*8,rax)
    def call(self,name,*args):
        self.args(args)
        if '!' in name:
            dll,fn=name.split('!');self.imports.setdefault(dll,[])
            if fn not in self.imports[dll]:self.imports[dll].append(fn)
            self.b(0xff,0x15);self.fix.append((len(self.code),'IAT:'+name,0));self.raw(b'\0'*4)
        else:self.b(0xe8);self.fix.append((len(self.code),name,0));self.raw(b'\0'*4)
    def com(self,obj,index,*args):
        self.args((obj,)+args);self.load(r11,rcx);self.rex(1,b=r11);self.b(0xff);self.mod(2,r11,index*8)
    def check(self,target):self.test(rax,0);self.jump(target,'s')
e=Emitter()
exec(compile((ROOT/'native_ui.py').read_text(encoding='utf8'), 'native_ui.py', 'exec'), globals())

# Build import directory and IAT, then fix all relative operands.
def build_imports(rva):
    out=bytearray(20*(len(e.imports)+1));syms={};iat_start=None;iat_end=None
    for i,(dll,functions) in enumerate(e.imports.items()):
        name=rva+len(out);out.extend(dll.encode()+b'\0')
        while len(out)%8:out.append(0)
        hints=[]
        for fn in functions:
            hints.append(rva+len(out));out.extend(b'\0\0'+fn.encode()+b'\0')
            if len(out)%2:out.append(0)
        while len(out)%8:out.append(0)
        ilt=rva+len(out)
        for h in hints:out.extend(u64(h))
        out.extend(u64(0));iat=rva+len(out)
        if iat_start is None:iat_start=iat
        for fn,h in zip(functions,hints):syms['IAT:'+dll+'!'+fn]=rva+len(out);out.extend(u64(h))
        out.extend(u64(0));iat_end=rva+len(out)
        struct.pack_into('<IIIII',out,i*20,ilt,0,0,name,iat)
    return out,syms,iat_start,iat_end-iat_start
text_rva=0x1000;imp_rva=align(text_rva+len(e.code),0x1000)
imports,syms,iat,iat_size=build_imports(imp_rva);data_rva=align(imp_rva+len(imports),0x1000)
bss_start=align(len(data),16)
for name,off in ds.items():syms[name]=data_rva+(bss_start+off[1] if isinstance(off,tuple) else off)
for name,off in e.labels.items():syms[name]=text_rva+off
for off,name,extra in e.fix:
    assert name in syms,name
    struct.pack_into('<i',e.code,off,syms[name]+extra-(text_rva+off+4))
headers=bytearray(0x400);headers[:2]=b'MZ';struct.pack_into('<I',headers,0x3c,0x80)
stub=b'Native x64. Direct machine code.\r\n\0';headers[0x40:0x40+len(stub)]=stub
pe=0x80;headers[pe:pe+4]=b'PE\0\0'
struct.pack_into('<HHIIIHH',headers,pe+4,0x8664,4,0,0,0,240,0x0022)
opt=pe+24;text_raw=align(len(e.code),0x200);imp_raw=align(len(imports),0x200);data_raw=align(len(data),0x200)
struct.pack_into('<HBBIIIIIQII',headers,opt,0x20b,1,0,text_raw,imp_raw+data_raw,bss,syms['entry'],text_rva,0x140000000,0x1000,0x200)
struct.pack_into('<HHHHHH',headers,opt+40,6,0,0,0,6,0)
reloc_rva=align(data_rva+bss_start+bss,0x1000);reloc=struct.pack('<IIHH',0,12,0,0)
struct.pack_into('<IIIIHHQQQQII',headers,opt+52,0,reloc_rva+0x1000,0x400,0,2,0x8160,0x100000,0x10000,0x100000,0x10000,0,16)
struct.pack_into('<II',headers,opt+112+8,imp_rva,20*(len(e.imports)+1))
struct.pack_into('<II',headers,opt+112+12*8,iat,iat_size)
struct.pack_into('<II',headers,opt+112+5*8,reloc_rva,len(reloc))
rawpos=0x400
for i,(name,rva,raw,virtual,flags) in enumerate([(b'.text',text_rva,e.code,len(e.code),0x60000020),(b'.idata',imp_rva,imports,len(imports),0xc0000040),(b'.data',data_rva,data,bss_start+bss,0xc0000040),(b'.reloc',reloc_rva,reloc,len(reloc),0x42000040)]):
    rawsize=align(len(raw),0x200)
    struct.pack_into('<8sIIIIIIHHI',headers,opt+240+i*40,name,virtual,rva,rawsize,rawpos,0,0,0,0,flags);rawpos+=rawsize
out=headers+e.code+bytes(text_raw-len(e.code))+imports+bytes(imp_raw-len(imports))+data+bytes(data_raw-len(data))+reloc+bytes(0x200-len(reloc))
output=PROJECT_ROOT/(sys.argv[1] if len(sys.argv)>1 else 'Gallery.exe')
output.write_bytes(out)
mapfile=PROJECT_ROOT/('binary-map.json' if output.name=='Gallery.exe' else output.stem+'.map.json')
mapfile.write_text(json.dumps({'format':'PE32+ AMD64 native','bytes':len(out),'code_bytes':len(e.code),'symbols':syms,'imports':e.imports},indent=2),encoding='utf8')
print(output.name+':',len(out),'bytes; code:',len(e.code),'bytes. No compiler or linker used.')
