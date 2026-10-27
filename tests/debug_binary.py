"""Native debugger smoke check for the emitted executable (test tooling only)."""
import ctypes as c, struct, pathlib, time, sys
k=c.WinDLL('kernel32',use_last_error=True)
class STARTUP(c.Structure):
    _fields_=[('cb',c.c_uint32),('reserved',c.c_void_p),('desktop',c.c_void_p),('title',c.c_void_p),('x',c.c_uint32),('y',c.c_uint32),('w',c.c_uint32),('h',c.c_uint32),('cx',c.c_uint32),('cy',c.c_uint32),('fill',c.c_uint32),('flags',c.c_uint32),('show',c.c_uint16),('cb2',c.c_uint16),('res2',c.c_void_p),('stdin',c.c_void_p),('stdout',c.c_void_p),('stderr',c.c_void_p)]
class PI(c.Structure):_fields_=[('process',c.c_void_p),('thread',c.c_void_p),('pid',c.c_uint32),('tid',c.c_uint32)]
k.CreateProcessW.argtypes=[c.c_wchar_p,c.c_wchar_p,c.c_void_p,c.c_void_p,c.c_int,c.c_uint32,c.c_void_p,c.c_wchar_p,c.POINTER(STARTUP),c.POINTER(PI)]
k.WaitForDebugEvent.argtypes=[c.c_void_p,c.c_uint32]
k.ContinueDebugEvent.argtypes=[c.c_uint32,c.c_uint32,c.c_uint32]
k.TerminateProcess.argtypes=[c.c_void_p,c.c_uint32]
si=STARTUP();si.cb=c.sizeof(si);pi=PI();root=pathlib.Path(__file__).resolve().parent.parent
assert k.CreateProcessW(str(root/(sys.argv[1] if len(sys.argv)>1 else 'Gallery.exe')),None,None,None,0,2,None,str(root),c.byref(si),c.byref(pi)),c.get_last_error()
end=time.time()+12
while time.time()<end:
    event=c.create_string_buffer(176)
    if not k.WaitForDebugEvent(event,500):continue
    b=event.raw;code,pid,tid=struct.unpack_from('<III',b)
    status=0x10002
    if code==1:
        exc=struct.unpack_from('<I',b,16)[0];addr=struct.unpack_from('<Q',b,32)[0];first=struct.unpack_from('<I',b,168)[0]
        print('exception',hex(exc),'address',hex(addr),'first',first,flush=True)
        if exc!=0x80000003:status=0x80010001
    elif code==3:print('image base',hex(struct.unpack_from('<Q',b,40)[0]),flush=True)
    elif code==5:
        print('exit',hex(struct.unpack_from('<I',b,16)[0]),flush=True);k.ContinueDebugEvent(pid,tid,status);break
    k.ContinueDebugEvent(pid,tid,status)
else:
    print('alive after 12 seconds',flush=True);k.TerminateProcess(pi.process,0)
