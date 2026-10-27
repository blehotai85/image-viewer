"""Emit full-resolution WIC encoding and atomic image replacement."""
e.begin('editorcopyblocks')
for n in ['edsourceDecoder','edsourceFrame','edblockreader','edblockwriter']:zero(n)
e.com(G('factory'),3,A('edoriginalfile'),0,0x80000000,0,A('edsourceDecoder'));e.check('copyblocksdone');e.com(G('edsourceDecoder'),13,0,A('edsourceFrame'));e.check('copyblocksdone');e.com(G('edsourceFrame'),0,A('blockreaderIID'),A('edblockreader'));e.check('copyblocksdone');e.com(G('edframe'),0,A('blockwriterIID'),A('edblockwriter'));e.check('copyblocksdone');e.com(G('edblockwriter'),7,G('edblockreader'))
e.label('copyblocksdone');e.ret()

e.begin('editorencode');zero('edencoded')
for n in ['edstream','edencoder','edframe','edbag','edwicbitmap','edconverter','edsourceDecoder','edsourceFrame','edblockreader','edblockwriter']:zero(n)
# Detect the requested format from the target extension, never from the temp name.
e.call('extension',A('edtarget'));e.mov(r12,rax);e.lea(r13,'containerjpeg');e.call(K+'lstrcmpiW',R(r12),A('png'));e.test(rax,0);notpng=e.unique();formatready=e.unique();e.jump(notpng,'ne');e.lea(r13,'containerpng');e.jump(formatready);e.label(notpng)
for ext in ['heic','heif']:
    e.call(K+'lstrcmpiW',R(r12),A(ext));e.test(rax,0);nextfmt=e.unique();e.jump(nextfmt,'ne');e.lea(r13,'containerheif');e.jump(formatready);e.label(nextfmt)
e.call(K+'lstrcmpiW',R(r12),A('jpg'));e.test(rax,0);e.jump(formatready,'e');e.call(K+'lstrcmpiW',R(r12),A('jpeg'));e.test(rax,0);e.jump('encodecodecerror','ne')
e.label(formatready);e.put('edcontainer',r13);e.com(G('factory'),8,R(r13),0,A('edencoder'));e.check('encodecodecerror')
e.com(G('factory'),14,A('edstream'));e.check('encodeerror');e.com(G('edstream'),15,A('edtempfile'),0x40000000);e.check('encodeerror');e.com(G('edencoder'),3,G('edstream'),2);e.check('encodeerror');e.com(G('edencoder'),10,A('edframe'),A('edbag'));e.check('encodeerror')
e.get(rax,'edbag');e.test(rax);nobag=e.unique();e.jump(nobag,'e');e.call('memzero',A('edqualitybag'),40);e.set('edqualitybag',A('edjpegquality'),16);e.com(G('edbag'),4,1,A('edqualitybag'),A('qualityvariant'));e.label(nobag)
e.com(G('edframe'),3,G('edbag'));e.check('encodeerror');e.com(G('edframe'),4,G('vieww'),G('viewh'));e.check('encodeerror');e.call('movebytes',A('edfmtguid'),A('bgra'),16);e.com(G('edframe'),6,A('edfmtguid'));e.check('encodecodecerror')
e.get(r12,'vieww');e.mul(r12,r12,4);e.get(r13,'viewh');e.mul(r13,r12)
e.com(G('factory'),20,G('vieww'),G('viewh'),A('bgra'),R(r12),R(r13),G('edfullpixels'),A('edwicbitmap'));e.check('encodeerror');e.com(G('factory'),10,A('edconverter'));e.check('encodeerror');e.com(G('edconverter'),8,G('edwicbitmap'),A('edfmtguid'),0,0,0,0);e.check('encodecodecerror')
e.call('editorcopyblocks');e.com(G('edframe'),11,G('edconverter'),0);e.check('encodeerror');e.com(G('edframe'),12);e.check('encodeerror');e.com(G('edencoder'),11);e.check('encodeerror');e.com(G('edstream'),8,0);e.check('encodeerror');e.set('edencoded',1);e.jump('encodecleanup')
e.label('encodecodecerror');e.set('error',A('edcodecfailed'));e.jump('encodecleanup')
e.label('encodeerror');e.set('error',A('edsavefailed'))
e.label('encodecleanup')
for n in ['edblockwriter','edblockreader','edsourceFrame','edsourceDecoder','edconverter','edwicbitmap','edframe','edbag','edencoder','edstream']:release(n)
e.get(rax,'edencoded');e.ret()

e.begin('editorsavefull');zero('error');e.set('edbusy',1);invalidate();e.call(U+'UpdateWindow',G('hwnd'));e.call('editorapply');e.call('editorlut');zero('edfullbmp');zero('edfullwork');zero('edfullpixels')
e.call('editordib',G('vieww'),G('viewh'),A('edfullpixels'));e.put('edfullbmp',rax);e.test(rax);e.jump('savefullbad','e');e.get(r12,'vieww');e.get(rax,'viewh');e.mul(r12,rax);e.mul(r12,r12,4);e.call(K+'VirtualAlloc',0,R(r12),0x3000,4);e.put('edfullwork',rax);e.test(rax);e.jump('savefullbad','e')
e.set('procheight',G('viewh'));e.call('processpixels',G('originalpixels'),G('edfullpixels'),G('edfullwork'),G('vieww'))
e.call(K+'lstrcpyW',A('edtempfile'),A('edtarget'));e.call(K+'lstrcatW',A('edtempfile'),A('edtmpfragment'));e.call(K+'GetCurrentProcessId');e.call('uinttext',R(rax),A('ednumtemp'));e.call(K+'lstrcatW',A('edtempfile'),A('ednumtemp'));e.call(K+'GetTickCount');e.call('uinttext',R(rax),A('ednumtemp'));e.call(K+'lstrcatW',A('edtempfile'),A('ednumtemp'));e.call(K+'lstrcatW',A('edtempfile'),A('edtempsuffix'))
# Reserve a fresh filename. Existing temp files are never truncated.
e.call(K+'CreateFileW',A('edtempfile'),0x40000000,0,0,1,0x80,0);e.cmpi(rax,-1);e.jump('savefullbad','e');e.call(K+'CloseHandle',R(rax));e.call('editorencode');e.test(rax);e.jump('savefullcleanup','e')
e.imm(r12,9);e.get(rax,'batchbusy');e.test(rax);normalreplace=e.unique();e.jump(normalreplace,'e');e.get(rax,'batchcopyflag');e.test(rax);e.jump(normalreplace,'e');e.imm(r12,8);e.label(normalreplace);e.call(K+'MoveFileExW',A('edtempfile'),A('edtarget'),R(r12));e.test(rax,0);e.jump('savefullbad','e');e.set('edencoded',1);e.jump('savefullcleanup')
e.label('savefullbad');e.set('error',A('edsavefailed'));zero('edencoded')
e.label('savefullcleanup');delobj('edfullbmp');e.get(rcx,'edfullwork');e.test(rcx);nowork=e.unique();e.jump(nowork,'e');e.call(K+'VirtualFree',R(rcx),0,0x8000);zero('edfullwork');e.label(nowork);e.get(rax,'edencoded');e.test(rax);savedfull=e.unique();e.jump(savedfull,'ne');e.call(K+'DeleteFileW',A('edtempfile'));e.label(savedfull);zero('edbusy');e.get(rax,'edencoded');e.ret()

# A request can be deferred until the user resolves unsaved changes.
# action 1=navigate(param +/-1), 2=close viewer, 3=close application.
e.begin('editorrequest');e.put('edpending',rcx);e.put('edpendingparam',rdx);e.get(rax,'editdirty');e.test(rax);cleanrequest=e.unique();e.jump(cleanrequest,'e');e.set('edmodal',3);zero('edfocus');invalidate();e.ret();e.label(cleanrequest);e.call('editorrunpending');e.ret()
e.begin('editorrunpending');e.get(r12,'edpending');e.get(r13,'edpendingparam');zero('edpending');zero('edmodal');zero('edfocus');e.cmpi(r12,1);np=e.unique();e.jump(np,'ne');e.call('navigateimage_raw',R(r13));e.ret();e.label(np);e.cmpi(r12,2);np=e.unique();e.jump(np,'ne');e.call('closeimage_raw');e.ret();e.label(np);e.cmpi(r12,3);np=e.unique();e.jump(np,'ne');e.call(U+'DestroyWindow',G('hwnd'));e.label(np);e.ret()
e.begin('navigateimage');e.mov(r12,rcx);e.get(rax,'viewindex');e.add(rax,r12);e.cmpi(rax,0);nonav=e.unique();e.jump(nonav,'l');e.get(rbx,'imagecount');e.cmp(rax,rbx);e.jump(nonav,'ge');e.call('editorrequest',1,R(r12));e.label(nonav);e.ret()
e.begin('closeimage');e.call('editorrequest',2,0);e.ret()

e.begin('editorstartsave');e.call(K+'lstrcpyW',A('edtarget'),A('edoriginalfile'));e.set('edsavepurpose',0);e.set('edmodal',1);zero('edfocus');invalidate();e.ret()
e.begin('editorstartsaveas');e.set('edmodal',2);zero('edfocus');zero('edformat');e.call(K+'lstrcpyW',A('edoutdir'),A('path'));e.get(rax,'viewindex');e.mul(rax,rax,1056);e.lea(r12,'images');e.add(r12,rax);e.call('extension',R(r12));e.mov(r13,rax);e.call(K+'lstrcpynW',A('edoutname'),R(r12),231);e.call('extension',A('edoutname'));word(rcx,rax);e.cmpi(rcx,46);noorigext=e.unique();e.jump(noorigext,'ne');e.imm(rcx,0);putword(rax,0,rcx);e.label(noorigext);e.call(K+'lstrcatW',A('edoutname'),A('editedsuffix'));word(rax,r13);e.cmpi(rax,46);noext=e.unique();e.jump(noext,'ne');e.call(K+'lstrcatW',A('edoutname'),R(r13));e.label(noext);invalidate();e.ret()
e.begin('editorsaveformat');e.put('edformat',rcx);e.mov(r12,rcx);e.call('extension',A('edoutname'));word(rcx,rax);e.cmpi(rcx,46);nox=e.unique();e.jump(nox,'ne');e.imm(rcx,0);putword(rax,0,rcx);e.label(nox);e.cmpi(r12,1);notp=e.unique();e.jump(notp,'ne');e.call(K+'lstrcatW',A('edoutname'),A('png'));e.jump('saveformatdone');e.label(notp);e.cmpi(r12,2);notj=e.unique();e.jump(notj,'ne');e.call(K+'lstrcatW',A('edoutname'),A('jpg'));e.jump('saveformatdone');e.label(notj);e.call('extension',A('edoriginalfile'));e.call(K+'lstrcatW',A('edoutname'),R(rax))
e.label('saveformatdone');invalidate();e.ret()

e.begin('editorsaveastarget');e.lea(r12,'edoutname');word(rax,r12);e.test(rax);e.jump('invalidsaveas','e');e.call(K+'lstrlenW',R(r12));e.cmpi(rax,255);e.jump('invalidsaveas','g');e.mul(rax,rax,2);e.add(rax,r12);word(rcx,rax,-2);e.cmpi(rcx,46);e.jump('invalidsaveas','e');e.cmpi(rcx,32);e.jump('invalidsaveas','e')
e.label('filenamecheck');word(rax,r12);e.test(rax);e.jump('filenamevalid','e');e.cmpi(rax,32);e.jump('invalidsaveas','l')
for char in ['\\','/',':','*','?','"','<','>','|']:e.cmpi(rax,ord(char));e.jump('invalidsaveas','e')
e.addi(r12,2);e.jump('filenamecheck')
e.label('filenamevalid');e.call(K+'GetFileAttributesW',A('edoutdir'));e.imm(rbx,0xffffffff);e.cmp(rax,rbx);e.jump('invalidsaveas','e');e.andi(rax,16);e.test(rax);e.jump('invalidsaveas','e');e.call(K+'lstrcpyW',A('edtarget'),A('edoutdir'));e.call('appendpath',A('edtarget'),A('edoutname'));e.set('edsavepurpose',1)
e.call(K+'GetFileAttributesW',A('edtarget'));e.imm(rbx,0xffffffff);e.cmp(rax,rbx);freshfile=e.unique();e.jump(freshfile,'e');e.set('edmodal',1);invalidate();e.ret();e.label(freshfile);e.call('editorcommitsave');e.ret()
e.label('invalidsaveas');e.set('error',A('edinvalidname'));invalidate();e.ret()

e.begin('editorcommitsave');e.call('editorsavefull');e.test(rax);savefailed=e.unique();e.jump(savefailed,'e')
# Reopen the committed file as the new baseline, then resume any pending action.
e.get(r12,'edpending');e.get(r13,'edpendingparam');zero('edmodal');e.call('editorclearimage');e.call(K+'lstrcpyW',A('path'),A('edtarget'));e.call('parentpath',A('path'));e.call('treeinit',A('path'),0);e.call('loadfolder');e.call('filename',A('edtarget'));e.mov(r14,rax);e.imm(r15,0)
e.label('findsaved');e.get(rax,'imagecount');e.cmp(r15,rax);notfound=e.unique();e.jump(notfound,'ge');e.mul(rbx,r15,1056);e.lea(rax,'images');e.add(rbx,rax);e.call(K+'lstrcmpiW',R(rbx),R(r14));e.test(rax,0);found=e.unique();e.jump(found,'e');e.addi(r15,1);e.jump('findsaved');e.label(found);e.call('openimage',R(r15));e.jump('reopeneddone');e.label(notfound);e.call('closeimage_raw');e.label('reopeneddone');e.put('edpending',r12);e.put('edpendingparam',r13);e.set('error',A('edsaved'));e.call('editorrunpending');invalidate();e.ret()
e.label(savefailed);e.set('edmodal',2);e.call(K+'lstrcpyW',A('edoutdir'),A('path'));e.call('filename',A('edtarget'));e.call(K+'lstrcpynW',A('edoutname'),R(rax),256);invalidate();e.ret()
