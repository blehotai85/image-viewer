"""Native instruction tests, run only while developing the emitted binary.

Map our own PE into this test process and call its pure pixel routines. This
does not build or link code, touch UI state, or add a dependency to Gallery.exe.
"""
import ctypes as c, json, struct, pathlib, math, random, sys
root=pathlib.Path(__file__).resolve().parent.parent
name=sys.argv[1] if len(sys.argv)>1 else 'Gallery.check.exe'
data=(root/name).read_bytes(); m=json.loads((root/(pathlib.Path(name).stem+'.map.json')).read_text())['symbols']
pe=struct.unpack_from('<I',data,60)[0];opt=pe+24;size=struct.unpack_from('<I',data,opt+56)[0]
k=c.WinDLL('kernel32',use_last_error=True);k.VirtualAlloc.restype=c.c_void_p;k.VirtualAlloc.argtypes=[c.c_void_p,c.c_size_t,c.c_uint32,c.c_uint32];k.VirtualFree.argtypes=[c.c_void_p,c.c_size_t,c.c_uint32]
base=k.VirtualAlloc(None,size,0x3000,0x40)
assert base,c.get_last_error()
for i in range(struct.unpack_from('<H',data,pe+6)[0]):
    section=opt+240+i*40;vsize,rva,rawsize,raw=struct.unpack_from('<IIII',data,section+8)
    c.memmove(base+rva,data[raw:raw+rawsize],rawsize)
lut=c.WINFUNCTYPE(None)(base+m['editorlut'])
process=c.WINFUNCTYPE(None,c.c_void_p,c.c_void_p,c.c_void_p,c.c_uint64)(base+m['processpixels'])
def trunc(a,b):return (abs(a)//abs(b))*(-1 if (a<0)!=(b<0) else 1)
def clamp(a):return max(0,min(255,a))
def reference(src,w,h,values):
    bright,contrast,sat,white,black,sharp,gamma,hue,temp=values
    co=math.cos(math.radians(hue));si=math.sin(math.radians(hue))
    matrix=[.213+.787*co-.213*si,.715-.715*co-.715*si,.072-.072*co+.928*si,
            .213-.213*co+.143*si,.715+.285*co+.140*si,.072-.072*co-.283*si,
            .213-.213*co-.787*si,.715-.715*co+.715*si,.072+.928*co+.072*si]
    luma=[3490,11714,1180]; sf=256+trunc(sat*(512 if sat>=0 else 256),100)
    matrix=[((round(v*16384)-luma[i%3])*sf>>8)+luma[i%3] for i,v in enumerate(matrix)]
    bp=trunc(black*127,100);den=255-trunc(white*127,100)-bp
    cf=256+trunc(contrast*(768 if contrast>=0 else 256),100);bf=trunc(bright*128,100);tf=trunc(temp*40,100)
    power=2.0**(-gamma/100.0)
    lookup=[]
    for ch in range(3):
        row=[]
        for x in range(256):
            lev=trunc((x-bp)*255,den);t=clamp(((lev-128)*cf>>8)+128+bf)
            row.append(clamp(round(255*(t/255)**power)+(tf if ch==0 else -tf if ch==2 else 0)))
        lookup.append(row)
    work=bytearray(len(src))
    for p in range(w*h):
        b,g,r,a=src[p*4:p*4+4];rgb=[r,g,b]
        changed=[lookup[ch][clamp(sum(matrix[ch*3+j]*rgb[j] for j in range(3))>>14)] for ch in range(3)]
        work[p*4:p*4+4]=bytes([changed[2],changed[1],changed[0],a])
    result=bytearray(work)
    if sharp:
        for y in range(1,h-1):
            for x in range(1,w-1):
                p=(y*w+x)*4
                for ch in range(3):
                    delta=4*work[p+ch]-sum(work[q+ch] for q in [p-4,p+4,p-w*4,p+w*4])
                    result[p+ch]=clamp(work[p+ch]+trunc(delta*sharp,400))
    return bytes(result)
try:
    random.seed(73);w,h=23,17;src=bytes(random.randrange(256) for _ in range(w*h*4))
    cases=[[0]*9]
    for i in range(9):
        for value in ([0,47,100] if i==5 else [-100,-23,38,100] if i!=7 else [-180,-71,93,180]):
            v=[0]*9;v[i]=value;cases.append(v)
    cases.extend([[19,-27,45,13,-9,64,31,72,-38],[-30,40,-50,66,22,100,-54,-133,100],[100,100,100,100,100,100,100,180,100]])
    source=c.create_string_buffer(src);output=c.create_string_buffer(len(src));work=c.create_string_buffer(len(src))
    for values in cases:
        c.memmove(base+m['edvalues'],struct.pack('<9q',*values),72);c.memmove(base+m['procheight'],struct.pack('<Q',h),8)
        lut();process(c.addressof(source),c.addressof(output),c.addressof(work),w)
        actual=output.raw;expected=reference(src,w,h,values)
        assert actual==expected,('pixel mismatch',values,next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None))
    assert reference(src,w,h,[0]*9)==src
    print('PASS:',len(cases),'native pixel cases; identity, all nine sliders, extremes, combined settings, alpha and sharpening edges.')
finally:k.VirtualFree(base,0,0x8000)
