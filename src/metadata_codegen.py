"""Emit bounded metadata formatting and WIC EXIF queries; no extra DLLs."""
e.begin('memzero');e.mov(rbx,rcx);e.mov(rsi,rdx);e.imm(rax,0)
e.label('zeroloop');e.test(rsi);zd=e.unique();e.jump(zd,'e');e.store(rbx,0,rax);e.addi(rbx,8);e.subi(rsi,8);e.jump('zeroloop');e.label(zd);e.ret()

# Decimal integer conversion, no CRT or printf. RCX=unsigned value, RDX=buffer.
e.begin('uinttext');e.mov(rbx,rcx);e.mov(rdi,rdx);e.imm(rsi,0);e.imm(r12,10)
e.label('digitloop');e.mov(rax,rbx);e.div(r12);e.mov(rbx,rax);e.addi(rdx,48);e.memlea(r13,rsp,0x160);e.add(r13,rsi);putword(r13,0,rdx);e.addi(rsi,2);e.test(rbx);e.jump('digitloop','ne')
e.label('digitcopy');e.subi(rsi,2);e.memlea(r13,rsp,0x160);e.add(r13,rsi);word(rax,r13);putword(rdi,0,rax);e.addi(rdi,2);e.test(rsi);e.jump('digitcopy','ne');e.imm(rax,0);putword(rdi,0,rax);e.ret()
e.begin('decimaltext');e.mov(rbx,rcx);e.mov(rsi,rdx);e.mov(rax,rbx);e.imm(rdi,10);e.div(rdi);e.mov(r12,rdx);e.call('uinttext',R(rax),R(rsi));e.call(K+'lstrcatW',R(rsi),A('decimalcomma'));e.call(K+'lstrlenW',R(rsi));e.mul(rax,rax,2);e.add(rax,rsi);e.addi(r12,48);putword(rax,0,r12);e.imm(r12,0);putword(rax,2,r12);e.ret()

# Mandatory summary is already available from directory enumeration.
e.begin('metainit');e.mov(r12,rcx);e.call('memzero',R(r12),2048)
e.get(rax,'finddata',28,0);e.shift(rax,32,4);e.get(rbx,'finddata',32,0);e.add(rax,rbx);e.store(r12,1984,rax);e.mov(r13,rax)
e.call(K+'lstrcpyW',R(r12),G('formatptr'));e.call(K+'lstrcatW',R(r12),A('metaseparator'));e.cmpi(r13,1048576);e.jump('sizemb','ge');e.cmpi(r13,1024);e.jump('sizekb','ge')
e.call('uinttext',R(r13),A('numberbuf'));e.lea(r14,'bytesuffix');e.jump('sizesuffix')
e.label('sizekb');e.mov(rax,r13);e.mul(rax,rax,10);e.addi(rax,512);e.imm(rbx,1024);e.div(rbx);e.call('decimaltext',R(rax),A('numberbuf'));e.lea(r14,'kibsuffix');e.jump('sizesuffix')
e.label('sizemb');e.mov(rax,r13);e.mul(rax,rax,10);e.addi(rax,524288);e.imm(rbx,1048576);e.div(rbx);e.call('decimaltext',R(rax),A('numberbuf'));e.lea(r14,'mibsuffix')
e.label('sizesuffix');e.call(K+'lstrcatW',R(r12),A('numberbuf'));e.call(K+'lstrcatW',R(r12),R(r14));e.memlea(rcx,r12,320);e.call(K+'lstrcpyW',R(rcx),A('nodims'));e.ret()

# querymeta(query, destination[160], kind: 0=text, 1=ISO, 2=FNumber).
# Supports the scalar and vector forms actually used by EXIF/WIC.
e.begin('querymeta');e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r14,r8);word(rax,r13);e.test(rax);e.jump('queryexists','ne')
e.call('memzero',A('propvar'),24);e.com(G('mreader'),5,R(r12),A('propvar'));e.check('queryclear')
e.get(rbx,'propvar',0,0);e.andi(rbx,0xffff);e.cmpi(r14,1);e.jump('queryiso','e');e.cmpi(r14,2);e.jump('queryaperture','e')
e.cmpi(rbx,30);e.jump('queryansi','e');e.cmpi(rbx,31);e.jump('querywide','e');e.cmpi(rbx,8);e.jump('querywide','e');e.jump('queryclear')
e.label('querywide');e.call(K+'lstrcpynW',R(r13),G('propvar',8),160);e.jump('queryclear')
e.label('queryansi');e.get(rax,'propvar',8);e.test(rax);e.jump('queryclear','e');e.call(K+'MultiByteToWideChar',65001,0,R(rax),-1,R(r13),160);e.test(rax,0);qs=e.unique();e.jump(qs,'ne');e.call(K+'MultiByteToWideChar',1252,0,G('propvar',8),-1,R(r13),160);e.label(qs);e.jump('queryclear')
e.label('queryiso');e.cmpi(rbx,18);e.jump('isou16','e');e.cmpi(rbx,19);e.jump('isou32','e');e.cmpi(rbx,3);e.jump('isou32','e');e.cmpi(rbx,0x1012);e.jump('isovector','e');e.jump('queryclear')
e.label('isou16');e.lea(rax,'propvar',8);word(r15,rax);e.jump('isofmt')
e.label('isou32');e.get(r15,'propvar',8,0);e.jump('isofmt')
e.label('isovector');e.get(rax,'propvar',8,0);e.test(rax);e.jump('queryclear','e');e.get(rax,'propvar',16);e.test(rax);e.jump('queryclear','e');word(r15,rax)
e.label('isofmt');e.cmpi(r15,1);e.jump('queryclear','l');e.call(K+'lstrcpyW',R(r13),A('isoprefix'));e.call('uinttext',R(r15),A('numberbuf'));e.call(K+'lstrcatW',R(r13),A('numberbuf'));e.jump('queryclear')
e.label('queryaperture');e.cmpi(rbx,21);e.jump('queryclear','ne');e.get(rax,'propvar',8,0);e.get(rdi,'propvar',12,0);e.test(rdi);e.jump('queryclear','e');e.mul(rax,rax,10);e.mov(rbx,rdi);e.shift(rbx,1);e.add(rax,rbx);e.div(rdi);e.cmpi(rax,1);e.jump('queryclear','l');e.mov(r15,rax);e.call(K+'lstrcpyW',R(r13),A('fnumberprefix'));e.call('decimaltext',R(r15),A('numberbuf'));e.call(K+'lstrcatW',R(r13),A('numberbuf'))
e.label('queryclear');e.call(O+'PropVariantClear',A('propvar'));word(rax,r13);e.test(rax);qempty=e.unique();e.jump(qempty,'e');e.imm(rax,1);e.ret();e.label(qempty);e.imm(rax,0);e.ret()
e.label('queryexists');e.imm(rax,1);e.ret()

# Called before thumbnail scaling, so dimensions are the ORIGINAL frame size.
e.begin('readmetadata');e.mov(r12,rcx);e.test(r12);e.jump('metadone','e');e.get(rax,'dw');e.store(r12,1920,rax);e.get(rax,'dh');e.store(r12,1928,rax)
e.memlea(r13,r12,320);e.call('uinttext',G('dw'),R(r13));e.call(K+'lstrcatW',R(r13),A('dimensionsx'));e.call('uinttext',G('dh'),A('numberbuf'));e.call(K+'lstrcatW',R(r13),A('numberbuf'));e.call(K+'lstrcatW',R(r13),A('pixelsuffix'))
e.get(rax,'infoview');e.test(rax);e.jump('metadone','e');e.load(rax,r12,2000);e.test(rax);e.jump('metadone','ne');e.imm(rax,1);e.store(r12,2000,rax);zero('mreader');e.com(G('frame'),8,A('mreader'));e.check('metarelease')
for field,offset,kind in [('camera',640,0),('make',640,0),('date',960,0),('datefallback',960,0),('aperture',1280,2),('iso',1600,1)]:
    done=e.unique('fielddone')
    for i in range(4):
        e.memlea(r13,r12,offset);e.call('querymeta',A('query_'+field+str(i)),R(r13),kind);e.test(rax);e.jump(done,'ne')
    e.label(done)
# EXIF dates use YYYY:MM:DD; make the display easier to read.
e.memlea(r13,r12,960);e.call(K+'lstrlenW',R(r13));e.cmpi(rax,10);dateok=e.unique();e.jump(dateok,'l');word(rax,r13,8);e.cmpi(rax,58);e.jump(dateok,'ne');e.imm(rax,45);putword(r13,8,rax);putword(r13,14,rax);e.label(dateok)
e.label('metarelease');release('mreader')
e.label('metadone');e.ret()

# Metadata icons are our own small outlined shapes, using the same UI renderer.
e.begin('uiline');e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r14,r8);e.mov(r15,r9);e.call(D+'MoveToEx',G('backdc'),R(r12),R(r13),0);e.call(D+'LineTo',G('backdc'),R(r14),R(r15));e.ret()
e.begin('infoicon');e.mov(rbx,rcx);e.mov(rsi,rdx);e.mov(rdi,r8);e.call(D+'SelectObject',G('backdc'),G('iconpen'));e.call(D+'SelectObject',G('backdc'),G('nullbrush'))
def iconline(x1,y1,x2,y2):
    e.memlea(r8,rbx,x1);e.memlea(r9,rsi,y1);e.memlea(r10,rbx,x2);e.memlea(r11,rsi,y2);e.call('uiline',R(r8),R(r9),R(r10),R(r11))
def iconshape(name,l,t,r,b):
    e.memlea(r8,rbx,l);e.memlea(r9,rsi,t);e.memlea(r10,rbx,r);e.memlea(r11,rsi,b);e.call(D+name,G('backdc'),R(r8),R(r9),R(r10),R(r11))
for kind in range(6):e.cmpi(rdi,kind);e.jump('infoicon'+str(kind),'e')
e.jump('iconend')
e.label('infoicon0');iconshape('Rectangle',2,1,13,15);iconline(5,5,10,5);iconline(5,8,10,8);iconline(5,11,9,11);e.jump('iconend')
e.label('infoicon1');iconline(1,6,1,1);iconline(1,1,6,1);iconline(9,1,14,1);iconline(14,1,14,6);iconline(1,9,1,14);iconline(1,14,6,14);iconline(9,14,14,14);iconline(14,14,14,9);e.jump('iconend')
e.label('infoicon2');iconshape('Rectangle',1,4,15,14);iconshape('Ellipse',5,6,11,12);iconline(4,4,5,1);iconline(5,1,10,1);iconline(10,1,11,4);e.jump('iconend')
e.label('infoicon3');iconshape('Rectangle',1,3,15,15);iconline(1,7,14,7);iconline(5,1,5,5);iconline(10,1,10,5);iconline(4,10,7,10);iconline(9,10,12,10);e.jump('iconend')
e.label('infoicon4');iconshape('Ellipse',1,1,15,15);iconshape('Ellipse',5,5,11,11);iconline(7,1,10,5);iconline(14,7,10,10);iconline(7,14,5,10);iconline(1,7,5,5);e.jump('iconend')
e.label('infoicon5');iconshape('Rectangle',1,2,15,14);iconline(4,11,4,8);iconline(7,11,7,5);iconline(10,11,10,7);iconline(13,11,13,4)
e.label('iconend');e.ret()
