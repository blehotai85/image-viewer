"""Emit the native integer colour pipeline, sharpening, preview and histograms."""
def byte(d,base,off=0):e.rex(0,r=d,b=base);e.b(0x0f,0xb6);e.mod(d,base,off)
def clamp255(r):
    lo=e.unique();hi=e.unique();e.cmpi(r,0);e.jump(lo,'ge');e.imm(r,0);e.label(lo);e.cmpi(r,255);e.jump(hi,'le');e.imm(r,255);e.label(hi)
def copyvals(dst,src):
    for off in range(0,72,8):e.val(r10,src);e.load(rax,r10,off);e.val(r11,dst);e.store(r11,off,rax)

e.begin('editorlut')
# Saturation factor Q8, then a hue/saturation matrix Q14.
e.get(rax,'edvalues',16);e.cmpi(rax,0);satneg=e.unique();satdone=e.unique();e.jump(satneg,'l');e.mul(rax,rax,512);e.jump(satdone);e.label(satneg);e.mul(rax,rax,256);e.label(satdone);e.imm(rbx,100);e.div(rbx);e.addi(rax,256);e.mov(r12,rax)
e.get(rax,'edvalues',56);e.addi(rax,180);e.mul(rax,rax,72);e.lea(r13,'huematrices');e.add(r13,rax);e.lea(r14,'edmatrix')
for i in range(9):
    e.load(rax,r13,i*8);e.get(rbx,'lumaweights',(i%3)*8);e.sub(rax,rbx);e.mul(rax,r12);e.shift(rax,8);e.add(rax,rbx);e.store(r14,i*8,rax)
# Three channel tone LUTs, including white/black points, contrast, brightness,
# gamma and temperature. All-zero settings form an exact identity.
e.get(rax,'edvalues',32);e.mul(rax,rax,127);e.imm(rbx,100);e.div(rbx);e.mov(r12,rax) # black
e.get(rax,'edvalues',24);e.mul(rax,rax,127);e.div(rbx);e.imm(r13,255);e.sub(r13,rax);e.sub(r13,r12) # white-black
e.get(rax,'edvalues',8);e.cmpi(rax,0);cneg=e.unique();cdone=e.unique();e.jump(cneg,'l');e.mul(rax,rax,768);e.jump(cdone);e.label(cneg);e.mul(rax,rax,256);e.label(cdone);e.div(rbx);e.addi(rax,256);e.mov(r14,rax)
e.get(rax,'edvalues');e.mul(rax,rax,128);e.div(rbx);e.mov(r15,rax)
e.get(rax,'edvalues',48);e.addi(rax,100);e.mul(rax,rax,256);e.lea(rsi,'gammaluts');e.add(rsi,rax)
e.imm(rdi,0);e.lea(rbx,'edlut')
e.label('lutloop');e.mov(rax,rdi);e.sub(rax,r12);e.mul(rax,rax,255);e.div(r13);e.subi(rax,128);e.mul(rax,r14);e.shift(rax,8);e.addi(rax,128);e.add(rax,r15);clamp255(rax);e.mov(rcx,rsi);e.add(rcx,rax);byte(r8,rcx)
e.get(rax,'edvalues',64);e.mul(rax,rax,40);e.imm(rcx,100);e.div(rcx);e.mov(r9,rax)
e.mov(rax,r8);e.add(rax,r9);clamp255(rax);e.store(rbx,0,rax,0)
e.store(rbx,1024,r8,0);e.mov(rax,r8);e.sub(rax,r9);clamp255(rax);e.store(rbx,2048,rax,0)
e.addi(rbx,4);e.addi(rdi,1);e.cmpi(rdi,256);e.jump('lutloop','l');e.ret()

# process(src,dst,work,width), height is passed in procheight. No heap or CRT.
e.begin('processpixels');e.put('procsrc',rcx);e.put('procdst',rdx);e.put('procwork',r8);e.put('procwidth',r9);e.mul(rax,r9,4);e.put('procstride',rax)
e.mov(r12,rcx);e.mov(r14,r8);e.get(r15,'procheight');e.mul(r15,r9);e.imm(rbx,0)
e.label('colourloop');e.cmp(rbx,r15);e.jump('colourdone','ge');e.load(rdi,r12,0,0)
e.mov(r8,rdi);e.shift(r8,16,5);e.andi(r8,255);e.mov(r9,rdi);e.shift(r9,8,5);e.andi(r9,255);e.mov(r10,rdi);e.andi(r10,255)
e.mov(r11,rdi);e.andi(r11,0xff000000)
for channel,shift in [(0,16),(1,8),(2,0)]:
    e.get(rax,'edmatrix',channel*24);e.mul(rax,r8);e.get(rcx,'edmatrix',channel*24+8);e.mul(rcx,r9);e.add(rax,rcx);e.get(rcx,'edmatrix',channel*24+16);e.mul(rcx,r10);e.add(rax,rcx);e.shift(rax,14);clamp255(rax)
    e.mul(rax,rax,4);e.lea(rcx,'edlut',channel*1024);e.add(rcx,rax);e.load(rax,rcx,0,0)
    if shift:e.shift(rax,shift,4)
    e.op(9,r11,rax)
e.store(r14,0,r11,0);e.addi(r12,4);e.addi(r14,4);e.addi(rbx,1);e.jump('colourloop')
e.label('colourdone');e.get(r12,'procwork');e.get(r13,'procdst');e.imm(rbx,0)
e.label('workcopy');e.cmp(rbx,r15);e.jump('workcopied','ge');e.load(rax,r12,0,0);e.store(r13,0,rax,0);e.addi(r12,4);e.addi(r13,4);e.addi(rbx,1);e.jump('workcopy')
e.label('workcopied');e.get(rax,'edvalues',40);e.test(rax);e.jump('processdone','e');e.get(rax,'procwidth');e.cmpi(rax,3);e.jump('processdone','l');e.get(rax,'procheight');e.cmpi(rax,3);e.jump('processdone','l')
e.get(r12,'procwork');e.get(r13,'procdst');e.get(rax,'procstride');e.add(r12,rax);e.add(r13,rax);e.addi(r12,4);e.addi(r13,4);e.get(r14,'procheight');e.subi(r14,2)
e.label('sharprow');e.get(r15,'procwidth');e.subi(r15,2)
e.label('sharppixel');e.load(r11,r12,0,0);e.andi(r11,0xff000000)
for shift in [0,8,16]:
    e.load(r8,r12,-4,0)
    if shift:e.shift(r8,shift,5)
    e.andi(r8,255);e.load(rax,r12,4,0)
    if shift:e.shift(rax,shift,5)
    e.andi(rax,255);e.add(r8,rax)
    e.get(rbx,'procstride');e.mov(rcx,r12);e.sub(rcx,rbx);e.load(rax,rcx,0,0)
    if shift:e.shift(rax,shift,5)
    e.andi(rax,255);e.add(r8,rax);e.mov(rcx,r12);e.add(rcx,rbx);e.load(rax,rcx,0,0)
    if shift:e.shift(rax,shift,5)
    e.andi(rax,255);e.add(r8,rax);e.load(r9,r12,0,0)
    if shift:e.shift(r9,shift,5)
    e.andi(r9,255);e.mul(rax,r9,4);e.sub(rax,r8);e.get(rbx,'edvalues',40);e.mul(rax,rbx);e.imm(rcx,400);e.div(rcx);e.add(rax,r9);clamp255(rax)
    if shift:e.shift(rax,shift,4)
    e.op(9,r11,rax)
e.store(r13,0,r11,0);e.addi(r12,4);e.addi(r13,4);e.subi(r15,1);e.jump('sharppixel','ne');e.addi(r12,8);e.addi(r13,8);e.subi(r14,1);e.jump('sharprow','ne')
e.label('processdone');e.ret()

e.begin('editorhistogram');e.call('memzero',A('edhist'),4096);e.get(r12,'edpreviewpixels');e.get(r13,'edpw');e.get(rax,'edph');e.mul(r13,rax);e.imm(rbx,0)
e.label('histloop');e.cmp(rbx,r13);e.jump('histdone','ge');e.load(rdi,r12,0,0);e.mov(r8,rdi);e.shift(r8,16,5);e.andi(r8,255);e.mov(r9,rdi);e.shift(r9,8,5);e.andi(r9,255);e.andi(rdi,255)
e.mul(rax,r8,54);e.mul(rcx,r9,183);e.add(rax,rcx);e.mul(rcx,rdi,19);e.add(rax,rcx);e.shift(rax,8,5);e.mov(r10,rax)
for channel,reg in [(0,r8),(1,r9),(2,rdi),(3,r10)]:
    e.mul(rax,reg,4);e.lea(rcx,'edhist',channel*1024);e.add(rcx,rax);e.load(rax,rcx,0,0);e.addi(rax,1);e.store(rcx,0,rax,0)
e.addi(r12,4);e.addi(rbx,1);e.jump('histloop')
e.label('histdone');e.ret()

e.begin('editordib');e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r14,r8);e.set('bmi',R(r12),4,0);e.imm(rax,0);e.sub(rax,r13);e.put('bmi',rax,8,0);e.call(D+'CreateDIBSection',0,A('bmi'),0,R(r14),0,0);e.ret()
e.begin('editorfreepreview')
for n in ['edbasebmp','edworkbmp','edpreviewbmp']:delobj(n)
for n in ['edbasepixels','edworkpixels','edpreviewpixels']:zero(n)
e.ret()
e.begin('editorclearimage');e.call(U+'KillTimer',G('hwnd'),3);e.call('editorfreepreview');e.call('memzero',A('edvalues'),72);zero('editdirty');zero('edsliderdrag');zero('edfocus');zero('edscroll');e.ret()
e.begin('editorensure');e.get(rax,'edbasebmp');e.test(rax);ensureexists=e.unique();e.jump(ensureexists,'ne')
e.get(r12,'vieww');e.get(r13,'viewh');e.cmpi(r12,1024);ew=e.unique();e.jump(ew,'le');e.mov(rax,r13);e.mul(rax,rax,1024);e.div(r12);e.mov(r13,rax);e.imm(r12,1024);e.label(ew);e.cmpi(r13,1024);eh=e.unique();e.jump(eh,'le');e.mov(rax,r12);e.mul(rax,rax,1024);e.div(r13);e.mov(r12,rax);e.imm(r13,1024);e.label(eh)
for r in [r12,r13]:
    ok=e.unique();e.cmpi(r,1);e.jump(ok,'ge');e.imm(r,1);e.label(ok)
e.put('edpw',r12);e.put('edph',r13)
for bmp,pixels in [('edbasebmp','edbasepixels'),('edworkbmp','edworkpixels'),('edpreviewbmp','edpreviewpixels')]:
    e.call('editordib',R(r12),R(r13),A(pixels));e.put(bmp,rax);e.test(rax);e.jump('ensurefail','e')
e.call(D+'CreateCompatibleDC',0);e.put('edsrcdc',rax);e.call(D+'CreateCompatibleDC',0);e.put('eddstdc',rax);e.call(D+'SelectObject',G('edsrcdc'),G('viewbmp'));e.put('edoldsrc',rax);e.call(D+'SelectObject',G('eddstdc'),G('edbasebmp'));e.put('edolddst',rax);e.call(D+'SetStretchBltMode',G('eddstdc'),4)
e.call(D+'StretchBlt',G('eddstdc'),0,0,R(r12),R(r13),G('edsrcdc'),0,0,G('vieww'),G('viewh'),0x00cc0020)
e.call(D+'SelectObject',G('edsrcdc'),G('edoldsrc'));e.call(D+'SelectObject',G('eddstdc'),G('edolddst'));e.call(D+'DeleteDC',G('edsrcdc'));e.call(D+'DeleteDC',G('eddstdc'))
e.label(ensureexists);e.call('editorapply');e.imm(rax,1);e.ret()
e.label('ensurefail');e.call('editorfreepreview');e.set('error',A('decodeerror'));e.imm(rax,0);e.ret()
e.begin('editorcheckdirty');e.get(r12,'editdirty');e.imm(rbx,0);e.lea(rsi,'edvalues');e.imm(rdi,0)
e.label('dirtyloop');e.load(rax,rsi);e.test(rax);dz=e.unique();e.jump(dz,'e');e.imm(rdi,1);e.label(dz);e.addi(rsi,8);e.addi(rbx,1);e.cmpi(rbx,9);e.jump('dirtyloop','l');e.put('editdirty',rdi);e.call('layout');e.ret()
e.begin('editorapply');e.call(U+'KillTimer',G('hwnd'),3);e.get(rax,'edbasebmp');e.test(rax);applydone=e.unique();e.jump(applydone,'e');e.call('editorlut');e.set('procheight',G('edph'));e.call('processpixels',G('edbasepixels'),G('edpreviewpixels'),G('edworkpixels'),G('edpw'));e.call('editorhistogram');e.call('editorcheckdirty');invalidate();e.label(applydone);e.ret()
e.begin('editorchanged');e.call('editorcheckdirty');e.call(U+'SetTimer',G('hwnd'),3,40,0);invalidate();e.ret()
