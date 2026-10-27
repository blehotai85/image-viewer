"""Direct AMD64 emission: own UI, tree, folder picker, hit testing and layout."""
data=bytearray();ds={};bss=0
exec(compile((ROOT/'ui_strings_en.py').read_text(encoding='utf8'),'ui_strings_en.py','exec'),globals())
def blob(n,v):
    while len(data)%8:data.append(0)
    ds[n]=len(data);data.extend(v)
def wide(n,v):blob(n,(UI_TEXT.get(n,v)+'\0').encode('utf-16le'))
def reserve(n,size):
    global bss
    bss=align(bss,16);ds[n]=('bss',bss);bss+=size
for n,t in {
 'class':'PureBinaryGallery','title':'Képtár', 'brand':'KÉPTÁR','open':'Mappa megnyitása',
 'gallerytitle':'Képek','folders':'MAPPÁK','sidebarhint':'Kattints a nyílra a kibontáshoz',
 'formats':'PNG  /  JPEG  /  HEIC','empty':'Ebben a mappában még nincs megjeleníthető kép.',
 'galleryhint':'Kattintás: megnyitás    ·    Görgő: lapozás    ·    Esc: kilépés',
 'viewerhint':'Bal kattintás: előző    ·    Jobb kattintás: következő    ·    Húzás: mozgatás    ·    Görgő: nagyítás',
 'decodeerror':'A kép nem olvasható. HEIC esetén Windows HEIF/HEVC-dekóder szükséges.',
 'foldererror':'Ez a mappa nem olvasható. Válassz másik mappát.',
 'pending':'Betöltés…','failed':'Nem olvasható kép','wildcard':'\\*','slash':'\\',
 'parent':'..','dot':'.','png':'.png','jpg':'.jpg','jpeg':'.jpeg','heic':'.heic','heif':'.heif',
 'loading':'Képtár — képek betöltése…','limit':'Képtár — elérted a mappánkénti megjelenítési korlátot',
 'pickerheading':'Mappa megnyitása','pickersub':'Bontsd ki a mappákat, majd válaszd ki a megnyitni kívánt helyet.',
 'choose':'Mappa kiválasztása','cancel':'Mégse','up':'↑','chevron':'›','expanded':'⌄',
 'fontname':'Segoe UI','pickhint':'Enter: kiválasztás    ·    Esc: mégse',
 'thumbview':'Bélyegképek','infoviewlabel':'Info nézet','backtolist':'← Vissza a listához','previous':'‹ Előző','next':'Következő ›',
 'formatpng':'PNG','formatjpg':'JPEG','formatheic':'HEIC','formatheif':'HEIF',
 'bytesuffix':' B','kibsuffix':' KiB','mibsuffix':' MiB','metaseparator':'  ·  ',
 'decimalcomma':',','dimensionsx':' × ','pixelsuffix':' px','nodims':'Méretek nem olvashatók',
 'noexif':'Nincs elérhető EXIF-adat','fnumberprefix':'f/','isoprefix':'ISO ','countersep':' / ',
 'fullscreenlabel':'Teljes képernyő','windowedlabel':'Ablakos nézet',
}.items():wide(n,t)
for field,tag,exif in [('camera',272,False),('make',271,False),('date',36867,True),('datefallback',306,False),('aperture',33437,True),('iso',34855,True)]:
    for i,prefix in enumerate(['/app1/ifd','/ifd','/eXIf/ifd','/exif/ifd']):wide('query_'+field+str(i),prefix+('/exif' if exif else '')+'/{ushort='+str(tag)+'}')
for n,g in [('factorycls','cacaf262-9370-4615-a13b-9f5539da4c0a'),('factoryiid','ec5ec8a9-c395-4314-9c77-54d7a935ff70'),('bgra','6fddc324-4e03-4bfe-b185-3d77768dc90f')]:blob(n,uuid.UUID(g).bytes_le)
blob('bmi',struct.pack('<IiiHHIIiiII',40,1,-1,1,32,0,0,0,0,0,0))
for n,size in [('wc',80),('msg',48),('paint',80),('textrect',16),('finddata',592),('treefind',592),('path',65536),('fullpath',65536),('scratch',65536),('treescratch',65536),('pickpath',65536),('drivebuf',1024),('mainnodes',4096*2112),('picknodes',4096*2112),('images',16384*1056),('metadata',16384*2048),('propvar',24),('numberbuf',128),('metatemp',320),('viewcounter',128)]:reserve(n,size)
for n in ['instance','hwnd','font','fonttitle','fontsmall','nullpen','factory','imagecount','scan','scroll','mode','clientw','clienth','cols','find','dc','backdc','backbmp','oldback','srcdc','oldsrc','viewbmp','vieww','viewh','scale','fit','vx','vy','vw','vh','drag','lastx','lasty','dec','frame','scaler','conv','decodebmp','pixels','dw','dh','maxwidth','source','limited','error','hover','picker','px','py','tbase','tcount','tsel','tscroll','tx','ty','tw','th','savbase','savcount','savsel','savscroll','clip','tfind','treehover']:
    reserve(n,8)
def rgb(v):return ((v&255)<<16)|(v&0xff00)|((v>>16)&255)
colors={'brushbg':0xf2f3f5,'brushside':0xfafafb,'brushtile':0xffffff,'brushblack':0x171a20,
 'brushwhite':0xffffff,'brushline':0xe1e4e8,'brushselect':0xe4edf4,'brushaccent':0x355f78,
 'brushhover':0xe6e9ed,'brushfolder':0xd3ac61,'brushfoldertop':0xe5c583,
 'brushshadow':0xe4e6e9,'brushdim':0xd7dbe0,'brushmuted':0xb7c0c9}
for n in colors:reserve(n,8)
for n in ['infoview','cardw','cardh','tilestep','rowstep','previeww','previewh','viewindex','metatarget','formatptr','mreader','iconpen','nullbrush','moved','downx','downy']:reserve(n,8)
for n,size in [('fullscreen',8),('windowstyle',8),('placement',64),('monitorinfo',40),('probedata',592),('probepath',65536)]:reserve(n,size)
exec(compile((ROOT/'editor_data.py').read_text(encoding='utf8'),'editor_data.py','exec'),globals())
exec(compile((ROOT/'batch_data.py').read_text(encoding='utf8'),'batch_data.py','exec'),globals())
K='kernel32.dll!';U='user32.dll!';D='gdi32.dll!';O='ole32.dll!'
INK=rgb(0x29343e);MUTED=rgb(0x77838e);ACCENT=rgb(0x355f78)
def invalidate():e.call(U+'InvalidateRect',G('hwnd'),0,0)
def zero(n):e.set(n,0)
def word(d,base,off=0):e.rex(0,r=d,b=base);e.b(0x0f,0xb7);e.mod(d,base,off)
def putword(base,off,s):e.b(0x66);e.rex(0,r=s,b=base);e.b(0x89);e.mod(s,base,off)
def release(n):
    skip=e.unique();e.get(rcx,n);e.test(rcx);e.jump(skip,'e');e.com(R(rcx),2);zero(n);e.label(skip)
def delobj(n):
    skip=e.unique();e.get(rcx,n);e.test(rcx);e.jump(skip,'e');e.call(D+'DeleteObject',R(rcx));zero(n);e.label(skip)
def rect(l,t,r,b):
    values=[l,t,r,b]
    for i,v in enumerate(values):
        if isinstance(v,tuple) and v[0]=='r':e.store(rsp,0x140+i*8,v[1])
    for i,v in enumerate(values):
        if not (isinstance(v,tuple) and v[0]=='r'):e.val(rax,v);e.store(rsp,0x140+i*8,rax)
    for i in range(4):e.load(rax,rsp,0x140+i*8);e.put('textrect',rax,i*4,0)
def fill(brush):e.call(U+'FillRect',G('backdc'),A('textrect'),G(brush))
def roundfill(brush,radius=12):e.call('roundbox',G(brush),radius)
def text(value,color=INK,flags=0x8820,font='font'):
    e.val(rax,value);e.store(rsp,0x180,rax)
    e.call(D+'SelectObject',G('backdc'),G(font));e.call(D+'SetTextColor',G('backdc'),color);e.load(r10,rsp,0x180);e.call(U+'DrawTextW',G('backdc'),R(r10),-1,A('textrect'),flags)
def makepath(name):e.call(K+'lstrcpyW',A('fullpath'),A('path'));e.call('appendpath',A('fullpath'),name)
def relative_rect(x,y,w,h):
    # x/y/w/h are integers relative to the picker panel origin.
    e.get(r8,'px');e.addi(r8,x);e.get(r9,'py');e.addi(r9,y);e.mov(r10,r8);e.addi(r10,w);e.mov(r11,r9);e.addi(r11,h);rect(R(r8),R(r9),R(r10),R(r11))

e.begin('entry');e.call(U+'SetProcessDPIAware');e.call(O+'CoInitializeEx',0,2)
e.call(O+'CoCreateInstance',A('factorycls'),0,1,A('factoryiid'),A('factory'));e.check('fatal')
e.call(K+'GetModuleHandleW',0);e.put('instance',rax)
for n,c in colors.items():e.call(D+'CreateSolidBrush',rgb(c));e.put(n,rax)
e.call(D+'CreatePen',0,1,rgb(0xa4adb6));e.put('iconpen',rax);e.call(D+'GetStockObject',5);e.put('nullbrush',rax)
for n,c in [('histpenR',0xc67474),('histpenG',0x6f9e80),('histpenB',0x7492bd),('histpenAll',0x7d8996)]:e.call(D+'CreatePen',0,1,rgb(c));e.put(n,rax)
for n,height,weight in [('font',-16,400),('fontsmall',-13,400),('fonttitle',-24,600)]:
    e.call(D+'CreateFontW',height,0,0,0,weight,0,0,0,1,0,0,5,0,A('fontname'));e.put(n,rax)
e.call(D+'GetStockObject',8);e.put('nullpen',rax)
e.set('wc',80,0,0);e.set('wc',0x0b,4,0);e.set('wc',A('wndproc'),8);e.set('wc',G('instance'),24)
e.call(U+'LoadCursorW',0,32512);e.put('wc',rax,40);e.set('wc',G('brushbg'),48);e.set('wc',A('class'),64)
e.call(U+'RegisterClassExW',A('wc'));e.test(rax);e.jump('fatal','e')
e.call(U+'CreateWindowExW',0,A('class'),A('title'),0x02cf0000,0x80000000,0x80000000,1240,840,0,0,G('instance'),0)
e.put('hwnd',rax);e.test(rax);e.jump('fatal','e')
e.call(K+'GetModuleFileNameW',0,A('path'),32768);e.call('parentpath',A('path'))
e.call('editorloadpresets')
e.call('batchensurepresets')
e.call('settingsrestorefolder')
e.set('tbase',A('mainnodes'));e.call('treeinit',A('path'),0);e.call('loadfolder')
e.call(U+'ShowWindow',G('hwnd'),5);e.call(U+'UpdateWindow',G('hwnd'))
e.label('messageloop');e.call(U+'GetMessageW',A('msg'),0,0,0);e.cmpi(rax,0);e.jump('exit','le')
e.call(U+'TranslateMessage',A('msg'));e.call(U+'DispatchMessageW',A('msg'));e.jump('messageloop')
e.label('fatal');e.call(K+'ExitProcess',1)
e.label('exit');release('factory');e.call(O+'CoUninitialize');e.call(K+'ExitProcess',0);e.ret()

# Own bounded path operations; no shell path helper library.
e.begin('appendpath');e.mov(rbx,rcx);e.mov(rsi,rdx);e.call(K+'lstrlenW',R(rbx));e.cmpi(rax,0);ap=e.unique();e.jump(ap,'e');e.memlea(rdi,rbx);e.mul(rax,rax,2);e.add(rdi,rax);word(rax,rdi,-2);e.cmpi(rax,92);e.jump(ap,'e');e.imm(rax,92);putword(rdi,0,rax);e.imm(rax,0);putword(rdi,2,rax);e.label(ap);e.call(K+'lstrcatW',R(rbx),R(rsi));e.ret()
e.begin('parentpath');e.mov(rbx,rcx);e.call(K+'lstrlenW',R(rbx));e.mov(rsi,rax);e.cmpi(rsi,3);e.jump('parentdone','le');e.mul(rsi,rsi,2);e.add(rsi,rbx);e.subi(rsi,2);word(rax,rsi);e.cmpi(rax,92);ntrail=e.unique();e.jump(ntrail,'ne');e.subi(rsi,2);e.label(ntrail)
e.label('parentloop');e.cmp(rsi,rbx);e.jump('parentdone','le');word(rax,rsi);e.cmpi(rax,92);e.jump('parentslash','e');e.subi(rsi,2);e.jump('parentloop')
e.label('parentslash');e.memlea(rdi,rbx,4);e.cmp(rsi,rdi);ps=e.unique();e.jump(ps,'ne');e.addi(rsi,2);e.label(ps);e.imm(rax,0);putword(rsi,0,rax)
e.label('parentdone');e.mov(rax,rbx);e.ret()
e.begin('filename');e.mov(rbx,rcx);e.mov(rsi,rcx)
e.label('nameloop');word(rax,rsi);e.test(rax);e.jump('namedone','e');e.cmpi(rax,92);ns=e.unique();e.jump(ns,'ne');e.memlea(rbx,rsi,2);e.label(ns);e.addi(rsi,2);e.jump('nameloop')
e.label('namedone');word(rax,rbx);e.test(rax);ns=e.unique();e.jump(ns,'ne');e.mov(rbx,rcx);e.label(ns);e.mov(rax,rbx);e.ret()
e.begin('extension');e.mov(rbx,rcx);e.mov(rsi,rcx);zeroext=e.unique()
e.label('extloop');word(rax,rsi);e.test(rax);e.jump('extdone','e');e.cmpi(rax,46);es=e.unique();e.jump(es,'ne');e.mov(rbx,rsi);e.label(es);e.addi(rsi,2);e.jump('extloop')
e.label('extdone');e.mov(rax,rbx);e.ret()
# Memmove for overlapping node ranges (all lengths are multiples of eight).
e.begin('movebytes');e.mov(rdi,rcx);e.mov(rsi,rdx);e.mov(rbx,r8);e.test(rbx);e.jump('movedone','e');e.cmp(rdi,rsi);e.jump('moveforward','le');e.add(rdi,rbx);e.add(rsi,rbx)
e.label('moveback');e.subi(rdi,8);e.subi(rsi,8);e.load(rax,rsi);e.store(rdi,0,rax);e.subi(rbx,8);e.jump('moveback','ne');e.jump('movedone')
e.label('moveforward');e.load(rax,rsi);e.store(rdi,0,rax);e.addi(rdi,8);e.addi(rsi,8);e.subi(rbx,8);e.jump('moveforward','ne')
e.label('movedone');e.ret()

# Cache whether a directory has children. A separate enumeration buffer/handle
# keeps probing independent of the expansion iterator. -1=unknown, 0=leaf, 1=branch.
e.begin('probechildren');e.mov(r12,rcx);e.load(rax,r12,2064);e.cmpi(rax,-1);e.jump('probecached','ne')
e.call(K+'lstrcpyW',A('probepath'),R(r12));e.call('appendpath',A('probepath'),A('wildcard',2));e.call(K+'FindFirstFileW',A('probepath'),A('probedata'));e.mov(r13,rax);e.cmpi(rax,-1);e.jump('probeempty','e')
e.label('probeloop');e.get(rax,'probedata',0,0);e.andi(rax,16);e.test(rax);e.jump('probenext','e')
for n in ['dot','parent']:e.call(K+'lstrcmpW',A('probedata',44),A(n));e.test(rax,0);e.jump('probenext','e')
e.call(K+'FindClose',R(r13));e.imm(rax,1);e.store(r12,2064,rax);e.ret()
e.label('probenext');e.call(K+'FindNextFileW',R(r13),A('probedata'));e.test(rax,0);e.jump('probeloop','ne');e.call(K+'FindClose',R(r13))
e.label('probeempty');e.imm(rax,0);e.store(r12,2064,rax)
e.label('probecached');e.ret()

# Visible depth-first tree nodes: UTF-16 path[1024], depth, expanded, child state.
e.begin('treeinit');e.mov(r12,rcx);e.mov(r13,rdx)
for n in ['tcount','tsel','tscroll']:zero(n)
e.call(K+'lstrcpynW',G('tbase'),R(r12),1024);e.get(rbx,'tbase');e.imm(rax,0);e.store(rbx,2048,rax);e.store(rbx,2056,rax);e.imm(rax,-1);e.store(rbx,2064,rax);e.set('tcount',1)
e.call('treetoggle',0);e.test(r13);e.jump('treeinitdone','e')
e.call(K+'GetLogicalDriveStringsW',512,A('drivebuf'));e.lea(r12,'drivebuf')
e.label('driveloop');word(rax,r12);e.test(rax);e.jump('treeinitdone','e');e.get(rbx,'tcount');e.mul(rbx,rbx,2112);e.get(rsi,'tbase');e.add(rsi,rbx);e.call(K+'lstrcpyW',R(rsi),R(r12));e.imm(rax,0);e.store(rsi,2048,rax);e.store(rsi,2056,rax);e.imm(rax,-1);e.store(rsi,2064,rax);e.get(rax,'tcount');e.addi(rax,1);e.put('tcount',rax);e.call(K+'lstrlenW',R(r12));e.mul(rax,rax,2);e.addi(rax,2);e.add(r12,rax);e.jump('driveloop')
e.label('treeinitdone');e.ret()

e.begin('treetoggle');e.mov(r12,rcx);e.get(rax,'tcount');e.cmp(r12,rax);e.jump('toggledone','ge');e.mul(r13,r12,2112);e.get(rax,'tbase');e.add(r13,rax);e.call('probechildren',R(r13));e.test(rax);e.jump('toggledone','e');e.load(r14,r13,2048);e.load(rax,r13,2056);e.test(rax);e.jump('treecollapse','ne');e.addi(r14,1);e.mov(r15,r12);e.addi(r15,1)
e.call(K+'lstrcpyW',A('treescratch'),R(r13));e.call('appendpath',A('treescratch'),A('wildcard',2))
e.call(K+'FindFirstFileW',A('treescratch'),A('treefind'));e.put('tfind',rax);e.cmpi(rax,-1);e.jump('treeunreadable','e')
e.label('treefindloop');e.get(rax,'treefind',0,0);e.andi(rax,16);e.test(rax);e.jump('treenext','e')
for n in ['dot','parent']:e.call(K+'lstrcmpW',A('treefind',44),A(n));e.test(rax,0);e.jump('treenext','e')
e.get(rax,'tcount');e.cmpi(rax,4096);e.jump('treenext','ge')
e.call(K+'lstrlenW',R(r13));e.mov(rbx,rax);e.call(K+'lstrlenW',A('treefind',44));e.add(rax,rbx);e.cmpi(rax,1021);e.jump('treenext','g')
e.get(r8,'tcount');e.sub(r8,r15);e.mul(r8,r8,2112);e.mul(rdx,r15,2112);e.get(rax,'tbase');e.add(rdx,rax);e.memlea(rcx,rdx,2112);e.call('movebytes',R(rcx),R(rdx),R(r8))
e.mul(rsi,r15,2112);e.get(rax,'tbase');e.add(rsi,rax);e.call(K+'lstrcpyW',R(rsi),R(r13));e.call('appendpath',R(rsi),A('treefind',44));e.store(rsi,2048,r14);e.imm(rax,0);e.store(rsi,2056,rax);e.imm(rax,-1);e.store(rsi,2064,rax)
e.get(rax,'tsel');e.cmp(rax,r15);selshift=e.unique();e.jump(selshift,'l');e.addi(rax,1);e.put('tsel',rax);e.label(selshift)
e.get(rax,'tcount');e.addi(rax,1);e.put('tcount',rax);e.addi(r15,1)
e.label('treenext');e.call(K+'FindNextFileW',G('tfind'),A('treefind'));e.test(rax,0);e.jump('treefindloop','ne');e.call(K+'FindClose',G('tfind'));e.mov(rax,r15);e.sub(rax,r12);e.subi(rax,1);branchfound=e.unique();e.cmpi(rax,0);e.jump(branchfound,'e');e.imm(rax,1);e.label(branchfound);e.store(r13,2056,rax);e.store(r13,2064,rax);e.jump('toggledone')
e.label('treeunreadable');e.set('error',A('foldererror'));e.jump('toggledone')
e.label('treecollapse');e.mov(r15,r12);e.addi(r15,1)
e.label('collapsefind');e.get(rax,'tcount');e.cmp(r15,rax);e.jump('collapseshift','ge');e.mul(rbx,r15,2112);e.get(rax,'tbase');e.add(rbx,rax);e.load(rax,rbx,2048);e.cmp(rax,r14);e.jump('collapseshift','le');e.addi(r15,1);e.jump('collapsefind')
e.label('collapseshift');e.mov(rsi,r15);e.sub(rsi,r12);e.subi(rsi,1)
e.get(rax,'tsel');e.cmp(rax,r12);selok=e.unique();selafter=e.unique();e.jump(selok,'le');e.cmp(rax,r15);e.jump(selafter,'ge');e.put('tsel',r12);e.jump(selok);e.label(selafter);e.sub(rax,rsi);e.put('tsel',rax);e.label(selok)
e.mul(rdx,r15,2112);e.get(rax,'tbase');e.add(rdx,rax);e.memlea(rcx,r13,2112);e.get(r8,'tcount');e.sub(r8,r15);e.mul(r8,r8,2112);e.call('movebytes',R(rcx),R(rdx),R(r8));e.get(rax,'tcount');e.sub(rax,rsi);e.put('tcount',rax);e.imm(rax,0);e.store(r13,2056,rax)
e.label('toggledone');invalidate();e.ret()

exec(compile((ROOT/'metadata_codegen.py').read_text(encoding='utf8'),'metadata_codegen.py','exec'),globals())
for editor_module in ['editor_pixels.py','editor_presets.py','settings_codegen.py','editor_save.py','editor_ui.py','editor_input.py','batch_codegen.py','batch_ui.py']:
    exec(compile((ROOT/editor_module).read_text(encoding='utf8'),editor_module,'exec'),globals())
e.begin('loadfolder');e.call('batchclear');zero('error');e.call(U+'KillTimer',G('hwnd'),1);e.imm(rbx,0);e.lea(rsi,'images')
e.label('freeimages');e.get(rax,'imagecount');e.cmp(rbx,rax);e.jump('freed','ge');e.load(rcx,rsi,1024);skip=e.unique();e.test(rcx);e.jump(skip,'e');e.call(D+'DeleteObject',R(rcx));e.label(skip);e.addi(rsi,1056);e.addi(rbx,1);e.jump('freeimages')
e.label('freed')
for n in ['imagecount','scan','scroll','limited']:zero(n)
e.call(U+'SetWindowTextW',G('hwnd'),A('loading'));e.call(K+'lstrcpyW',A('scratch'),A('path'));e.call(K+'lstrcatW',A('scratch'),A('wildcard'))
e.call(K+'FindFirstFileW',A('scratch'),A('finddata'));e.put('find',rax);e.cmpi(rax,-1);e.jump('folderbad','e')
e.label('findloop');e.get(rax,'finddata',0,0);e.andi(rax,16);e.test(rax);e.jump('findnext','ne');e.call('extension',A('finddata',44));e.mov(rbx,rax)
for ext in ['png','jpg','jpeg','heic','heif']:
    e.set('formatptr',A('format'+('jpg' if ext=='jpeg' else ext)));e.call(K+'lstrcmpiW',R(rbx),A(ext));e.test(rax,0);e.jump('imagefound','e')
e.jump('findnext')
e.label('imagefound');e.get(rbx,'imagecount');e.cmpi(rbx,16384);e.jump('hitlimit','ge');e.mul(r14,rbx,2048);e.lea(rax,'metadata');e.add(r14,rax);e.call('metainit',R(r14));e.mul(rbx,rbx,1056);e.lea(rsi,'images');e.add(rsi,rbx)
e.call(K+'lstrcpyW',R(rsi),A('finddata',44));e.imm(rax,0)
for off in [1024,1032,1040,1048]:e.store(rsi,off,rax)
e.get(rax,'imagecount');e.addi(rax,1);e.put('imagecount',rax);e.jump('findnext')
e.label('hitlimit');e.set('limited',1)
e.label('findnext');e.call(K+'FindNextFileW',G('find'),A('finddata'));e.test(rax,0);e.jump('findloop','ne');e.call(K+'FindClose',G('find'));e.call('settingsrememberfolder');e.call(U+'SetTimer',G('hwnd'),1,15,0);invalidate();e.ret()
e.label('folderbad');e.set('error',A('foldererror'));e.call(U+'SetWindowTextW',G('hwnd'),A('title'));invalidate();e.ret()
exec(compile((ROOT/'wic_codegen.py').read_text(encoding='utf8'),'wic_codegen.py','exec'),globals())
e.begin('thumbnail');e.label('thumbscan');e.get(rbx,'scan');e.get(rax,'imagecount');e.cmp(rbx,rax);e.jump('thumbdone','ge');e.mul(rsi,rbx,1056);e.lea(rdi,'images');e.add(rdi,rsi)
e.mul(rsi,rbx,2048);e.lea(rax,'metadata');e.add(rsi,rax);e.put('metatarget',rsi)
e.load(rax,rdi,1048);e.test(rax);thumbdecode=e.unique();e.jump(thumbdecode,'e');e.get(rax,'infoview');e.test(rax);e.jump('thumbskip','e');e.load(rax,rsi,2000);e.test(rax);e.jump('thumbskip','ne');e.label(thumbdecode)
makepath(R(rdi));e.call('decode',A('fullpath'),240);e.mov(r12,rax);e.load(rcx,rdi,1024);td=e.unique();e.test(rcx);e.jump(td,'e');e.call(D+'DeleteObject',R(rcx));e.label(td)
e.store(rdi,1024,r12);e.get(rax,'dw');e.store(rdi,1032,rax);e.get(rax,'dh');e.store(rdi,1040,rax);e.imm(rax,1);e.store(rdi,1048,rax);e.addi(rbx,1);e.put('scan',rbx);invalidate();e.ret()
e.label('thumbskip');e.addi(rbx,1);e.put('scan',rbx);e.jump('thumbscan')
e.label('thumbdone');e.call(U+'KillTimer',G('hwnd'),1);e.call(U+'SetWindowTextW',G('hwnd'),A('title'));e.ret()
exec(compile((ROOT/'view_codegen.py').read_text(encoding='utf8'),'view_codegen.py','exec'),globals())
e.begin('openimage');e.mov(r12,rcx);e.get(rax,'imagecount');e.cmp(r12,rax);e.jump('openbounds','ge');e.cmpi(r12,0);e.jump('openbounds','l');e.mul(rsi,r12,1056);e.lea(rdi,'images');e.add(rdi,rsi);e.mul(rsi,r12,2048);e.lea(rax,'metadata');e.add(rsi,rax);e.put('metatarget',rsi);makepath(R(rdi));e.call('decode',A('fullpath'),0);e.test(rax);e.jump('openbad','e')
e.mov(rsi,rax);e.call('editorclearimage');e.set('originalpixels',G('pixels'));e.call(K+'lstrcpyW',A('edoriginalfile'),A('fullpath'));delobj('viewbmp');e.put('viewbmp',rsi);e.put('viewindex',r12);e.set('vieww',G('dw'));e.set('viewh',G('dh'));e.set('mode',1);zero('hover');zero('error');zero('drag');e.call(U+'KillTimer',G('hwnd'),2);e.call(U+'SetWindowTextW',G('hwnd'),R(rdi));e.call('batchinherit');e.call('layout');e.call('fitview');e.get(rax,'editoropen');e.test(rax);nopreviewopen=e.unique();e.jump(nopreviewopen,'e');e.call('editorensure');e.label(nopreviewopen)
e.mov(rax,r12);e.addi(rax,1);e.call('uinttext',R(rax),A('viewcounter'));e.call(K+'lstrcatW',A('viewcounter'),A('countersep'));e.call('uinttext',G('imagecount'),A('numberbuf'));e.call(K+'lstrcatW',A('viewcounter'),A('numberbuf'));invalidate();e.imm(rax,1);e.ret()
e.label('openbad');e.set('error',A('decodeerror'));invalidate()
e.label('openbounds');e.imm(rax,0);e.ret()
e.begin('navigateimage_raw');e.mov(r12,rcx);e.get(r13,'viewindex')
e.label('navloop');e.add(r13,r12);e.cmpi(r13,0);e.jump('navdone','l');e.get(rax,'imagecount');e.cmp(r13,rax);e.jump('navdone','ge');e.call('openimage',R(r13));e.test(rax);e.jump('navloop','e')
e.label('navdone');e.ret()
e.begin('leavefullscreen');e.get(rax,'fullscreen');e.test(rax);leavefsdone=e.unique();e.jump(leavefsdone,'e');zero('fullscreen');e.call(U+'SetWindowLongPtrW',G('hwnd'),-16,G('windowstyle'));e.call(U+'SetWindowPlacement',G('hwnd'),A('placement'));e.call(U+'SetWindowPos',G('hwnd'),0,0,0,0,0,0x237);e.label(leavefsdone);e.ret()
e.begin('togglefullscreen');e.call(U+'KillTimer',G('hwnd'),2);e.get(rax,'fullscreen');e.test(rax);enterfs=e.unique();e.jump(enterfs,'e');e.call('leavefullscreen');invalidate();e.ret();e.label(enterfs)
e.call(U+'GetWindowLongPtrW',G('hwnd'),-16);e.put('windowstyle',rax);e.set('placement',44,0,0);e.call(U+'GetWindowPlacement',G('hwnd'),A('placement'))
e.call(U+'MonitorFromWindow',G('hwnd'),2);e.mov(rbx,rax);e.set('monitorinfo',40,0,0);e.call(U+'GetMonitorInfoW',R(rbx),A('monitorinfo'));e.test(rax,0);fsfail=e.unique();e.jump(fsfail,'e')
e.set('fullscreen',1);e.call(U+'SetWindowLongPtrW',G('hwnd'),-16,0x92000000)
e.get(rbx,'monitorinfo',4,0);e.get(rsi,'monitorinfo',8,0);e.get(rdi,'monitorinfo',12,0);e.sub(rdi,rbx);e.get(r12,'monitorinfo',16,0);e.sub(r12,rsi);e.call(U+'SetWindowPos',G('hwnd'),0,R(rbx),R(rsi),R(rdi),R(r12),0x260);invalidate();e.label(fsfail);e.ret()
e.begin('closeimage_raw');e.call('leavefullscreen');e.call('editorclearimage');zero('mode');zero('drag');e.call(U+'KillTimer',G('hwnd'),2);e.call(U+'ReleaseCapture');delobj('viewbmp');e.call(U+'SetWindowTextW',G('hwnd'),A('title'));invalidate();e.ret()

# Folder selection is an in-canvas modal. No dialog, child HWND or shell control.
e.begin('openpicker');zero('error');zero('hover');e.set('picker',1)
for n in ['base','count','sel','scroll']:e.set('sav'+n,G('t'+n))
e.get(rax,'edpickerpurpose');e.test(rax);normalpickpath=e.unique();pickpathdone=e.unique();e.jump(normalpickpath,'e');e.call(K+'lstrcpyW',A('pickpath'),A('edoutdir'));e.jump(pickpathdone);e.label(normalpickpath);e.call(K+'lstrcpyW',A('pickpath'),A('path'));e.label(pickpathdone);e.set('tbase',A('picknodes'));e.call('treeinit',A('pickpath'),1);e.call('layout');invalidate();e.ret()
e.begin('cancelpicker');zero('picker');zero('error');zero('hover');zero('edpickerpurpose')
for n in ['base','count','sel','scroll']:e.set('t'+n,G('sav'+n))
e.call('layout');invalidate();e.ret()
e.begin('acceptpicker');e.call(K+'GetFileAttributesW',A('pickpath'));e.imm(rbx,0xffffffff);e.cmp(rax,rbx);e.jump('acceptbad','e');e.andi(rax,16);e.test(rax);e.jump('acceptbad','e')
e.get(rax,'edpickerpurpose');e.test(rax);normalaccept=e.unique();e.jump(normalaccept,'e');e.call(K+'lstrcpyW',A('edoutdir'),A('pickpath'));e.call('cancelpicker');invalidate();e.ret();e.label(normalaccept)
e.call(K+'lstrcpyW',A('path'),A('pickpath'));e.call('cancelpicker');e.call('treeinit',A('path'),0);e.call('loadfolder');e.ret()
e.label('acceptbad');e.set('error',A('foldererror'));invalidate();e.ret()

# Shared layout drives both rendering and hit testing.
e.begin('layout');e.set('cardw',186);e.set('cardh',186);e.set('tilestep',200);e.set('rowstep',204);e.set('previeww',160);e.set('previewh',124)
e.set('viewtop',60);e.get(rax,'clientw');e.subi(rax,340);e.put('edpanelx',rax);e.get(rbx,'editoropen');e.test(rbx);layoutwithoutpanel=e.unique();e.jump(layoutwithoutpanel,'ne');e.get(rax,'clientw');e.label(layoutwithoutpanel);e.put('viewportw',rax);e.get(rax,'clienth');e.get(rbx,'viewtop');e.sub(rax,rbx);e.subi(rax,32);e.put('viewporth',rax)
e.get(rax,'infoview');e.test(rax);basiclayout=e.unique();e.jump(basiclayout,'e');e.set('cardw',266);e.set('cardh',350);e.set('tilestep',282);e.set('rowstep',368);e.set('previeww',240);e.set('previewh',148);e.label(basiclayout)
e.get(rax,'clientw');e.subi(rax,304);e.get(rbx,'tilestep');e.div(rbx);e.cmpi(rax,1);colsok=e.unique();e.jump(colsok,'ge');e.imm(rax,1);e.label(colsok);e.put('cols',rax)
e.get(rax,'clientw');e.subi(rax,720);e.shift(rax,1);e.put('px',rax);e.get(rax,'clienth');e.subi(rax,560);e.shift(rax,1);e.put('py',rax)
e.get(rax,'picker');e.test(rax);normal=e.unique();e.jump(normal,'e')
e.get(rax,'px');e.addi(rax,24);e.put('tx',rax);e.get(rax,'py');e.addi(rax,148);e.put('ty',rax);e.set('tw',672);e.set('th',318);e.ret()
e.label(normal);e.set('tx',16);e.set('ty',124);e.set('tw',248);e.get(rax,'clienth');e.subi(rax,164);e.put('th',rax);e.ret()
e.begin('setview');e.put('infoview',rcx);zero('scroll');zero('scan');e.call('layout');e.call(U+'SetTimer',G('hwnd'),1,15,0);e.get(rax,'batchcount');e.test(rax);noreschedule=e.unique();e.jump(noreschedule,'e');e.call('batchschedule');e.label(noreschedule);invalidate();e.ret()

# Drawing primitives. Brushes, glyphs, icons and hit regions belong to this UI.
e.begin('roundbox');e.mov(rbx,rcx);e.mov(rsi,rdx);e.call(D+'SelectObject',G('backdc'),R(rbx));e.call(D+'SelectObject',G('backdc'),G('nullpen'))
for reg,off in [(rbx,0),(rdi,4),(r12,8),(r13,12)]:e.get(reg,'textrect',off,0)
e.call(D+'RoundRect',G('backdc'),R(rbx),R(rdi),R(r12),R(r13),R(rsi),R(rsi));e.ret()
e.begin('foldericon');e.mov(rbx,rcx);e.mov(rsi,rdx);e.memlea(r8,rbx,9);e.memlea(r9,rsi,5);rect(R(rbx),R(rsi),R(r8),R(r9));roundfill('brushfoldertop',3)
e.memlea(r8,rbx,19);e.memlea(r9,rsi,15);e.memlea(r10,rsi,3);rect(R(rbx),R(r10),R(r8),R(r9));roundfill('brushfolder',4)
e.memlea(r8,rbx,19);e.memlea(r9,rsi,7);e.memlea(r10,rsi,4);rect(R(rbx),R(r10),R(r8),R(r9));fill('brushfoldertop');e.ret()

e.begin('drawtree');e.call(D+'SaveDC',G('backdc'));e.put('clip',rax)
e.get(r8,'tx');e.get(r9,'ty');e.get(r10,'tw');e.add(r10,r8);e.get(r11,'th');e.add(r11,r9);e.call(D+'IntersectClipRect',G('backdc'),R(r8),R(r9),R(r10),R(r11))
e.get(rbx,'tscroll');e.get(rsi,'ty');e.get(r15,'ty');e.get(rax,'th');e.add(r15,rax)
e.label('treedrawloop');e.get(rax,'tcount');e.cmp(rbx,rax);e.jump('treedrawdone','ge');e.cmp(rsi,r15);e.jump('treedrawdone','ge')
e.mul(r12,rbx,2112);e.get(rax,'tbase');e.add(r12,rax);e.load(r14,r12,2048);e.mul(r14,r14,18);e.get(rax,'tx');e.add(r14,rax)
e.get(rax,'tsel');e.cmp(rbx,rax);nsel=e.unique();e.jump(nsel,'ne');e.get(r8,'tx');e.get(r10,'tw');e.add(r10,r8);e.memlea(r9,rsi,30);rect(R(r8),R(rsi),R(r10),R(r9));roundfill('brushselect',8);e.label(nsel)
# Tree connectors are deliberately low contrast. One spine for each ancestor.
e.load(rdi,r12,2048);e.imm(r13,0)
e.label('treeancestor');e.cmp(r13,rdi);e.jump('treebranch','ge');e.mul(r8,r13,18);e.get(rax,'tx');e.add(r8,rax);e.addi(r8,8);e.memlea(r10,r8,1);e.memlea(r9,rsi,32);rect(R(r8),R(rsi),R(r10),R(r9));fill('brushline');e.addi(r13,1);e.jump('treeancestor')
e.label('treebranch');e.cmpi(rdi,0);norootline=e.unique();e.jump(norootline,'e');e.memlea(r8,r14,-10);e.memlea(r10,r14,0);e.memlea(r9,rsi,15);e.memlea(r11,rsi,16);rect(R(r8),R(r9),R(r10),R(r11));fill('brushline');e.label(norootline)
arrowdone=e.unique();e.call('probechildren',R(r12));e.test(rax);e.jump(arrowdone,'e')
e.memlea(r8,r14,0);e.memlea(r10,r14,16);e.memlea(r9,rsi,2);e.memlea(r11,rsi,28);rect(R(r8),R(r9),R(r10),R(r11));e.load(rax,r12,2056);e.test(rax);collapsed=e.unique();e.jump(collapsed,'e');text(A('expanded'),MUTED,0x25);e.jump(arrowdone);e.label(collapsed);text(A('chevron'),MUTED,0x25);e.label(arrowdone)
e.memlea(rcx,r14,20);e.memlea(rdx,rsi,8);e.call('foldericon',R(rcx),R(rdx));e.call('filename',R(r12));e.mov(rdi,rax)
e.memlea(r8,r14,48);e.memlea(r9,rsi,0);e.get(r10,'tx');e.get(rax,'tw');e.add(r10,rax);e.subi(r10,8);e.memlea(r11,rsi,30);rect(R(r8),R(r9),R(r10),R(r11));text(R(rdi))
e.addi(rbx,1);e.addi(rsi,32);e.jump('treedrawloop')
e.label('treedrawdone');e.call(D+'RestoreDC',G('backdc'),G('clip'))
# A slim custom scrollbar, shown only when necessary.
e.get(rax,'tcount');e.mul(rax,rax,32);e.get(rbx,'th');e.cmp(rax,rbx);noscroll=e.unique();e.jump(noscroll,'le');e.mov(rsi,rax);e.mul(rax,rbx);e.mov(rax,rbx);e.mul(rax,rbx);e.div(rsi);e.cmpi(rax,20);thumbok=e.unique();e.jump(thumbok,'ge');e.imm(rax,20);e.label(thumbok);e.mov(rdi,rax)
e.get(rax,'tscroll');e.mul(rax,rax,32);e.mul(rax,rbx);e.div(rsi);e.get(r9,'ty');e.add(r9,rax);e.get(r8,'tx');e.get(rax,'tw');e.add(r8,rax);e.subi(r8,4);e.memlea(r10,r8,3);e.mov(r11,r9);e.add(r11,rdi);rect(R(r8),R(r9),R(r10),R(r11));roundfill('brushmuted',3);e.label(noscroll);e.ret()

e.begin('drawmetadata');e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r14,r8);e.imm(r15,0)
for kind,offset in enumerate([0,320,640,960,1280,1600]):
    missing=e.unique();e.memlea(rsi,r12,offset)
    if kind>=2:
        word(rax,rsi);e.test(rax);e.jump(missing,'e');e.addi(r15,1)
    e.memlea(rdx,r14,3);e.call('infoicon',R(r13),R(rdx),kind)
    e.memlea(r8,r13,26);e.memlea(r10,r13,238);e.memlea(r11,r14,23);rect(R(r8),R(r14),R(r10),R(r11));text(R(rsi),MUTED,0x8820,'fontsmall');e.addi(r14,24);e.label(missing)
e.test(r15);hasexif=e.unique();e.jump(hasexif,'ne');e.memlea(r8,r13,26);e.memlea(r10,r13,238);e.memlea(r11,r14,23);rect(R(r8),R(r14),R(r10),R(r11));text(A('noexif'),MUTED,0x8820,'fontsmall');e.label(hasexif);e.ret()

# The canvas is double-buffered; no native child controls are created.
e.begin('paintwindow');e.call(U+'BeginPaint',G('hwnd'),A('paint'));e.put('dc',rax);e.get(rax,'clientw');e.cmpi(rax,1);e.jump('paintend','l');e.get(rax,'clienth');e.cmpi(rax,1);e.jump('paintend','l')
e.call(D+'CreateCompatibleDC',G('dc'));e.put('backdc',rax);e.call(D+'CreateCompatibleBitmap',G('dc'),G('clientw'),G('clienth'));e.put('backbmp',rax);e.call(D+'SelectObject',G('backdc'),G('backbmp'));e.put('oldback',rax);e.call(D+'SetBkMode',G('backdc'),1);e.call(D+'CreateCompatibleDC',G('dc'));e.put('srcdc',rax);e.call(D+'SetStretchBltMode',G('backdc'),4)
e.get(rax,'batchbusy');e.get(rbx,'batchconfirm');e.add(rax,rbx);e.get(rbx,'batchdone');e.add(rax,rbx);e.test(rax);e.jump('paintbatchmodal','ne');e.get(rax,'picker');e.test(rax);e.jump('paintpicker','ne');e.get(rax,'edbusy');e.test(rax);e.jump('painteditmodal','ne');e.get(rax,'edmodal');e.test(rax);e.jump('painteditmodal','ne');rect(0,0,G('clientw'),G('clienth'));e.get(rax,'mode');e.test(rax);e.jump('paintviewer','ne');fill('brushbg')
# Menu bar and sidebar.
rect(0,0,G('clientw'),56);fill('brushwhite');rect(0,55,G('clientw'),56);fill('brushline')
rect(18,10,211,44);e.get(rax,'hover');e.cmpi(rax,1);nohover=e.unique();menudrawn=e.unique();e.jump(nohover,'ne');roundfill('brushhover',9);e.jump(menudrawn);e.label(nohover);roundfill('brushside',9);e.label(menudrawn)
e.call('foldericon',30,19);rect(60,10,205,44);text(A('open'),ACCENT)
rect(244,10,514,44);roundfill('brushhover',9);e.get(rax,'infoview');e.test(rax);selectinfo=e.unique();selectviewdone=e.unique();e.jump(selectinfo,'ne');rect(246,12,396,42);roundfill('brushwhite',7);e.jump(selectviewdone);e.label(selectinfo);rect(398,12,512,42);roundfill('brushwhite',7);e.label(selectviewdone)
rect(250,10,392,44);text(A('thumbview'),ACCENT,0x25);rect(400,10,510,44);text(A('infoviewlabel'),ACCENT,0x25)
e.get(rax,'clientw');e.subi(rax,150);rect(R(rax),12,G('clientw'),42);text(A('brand'),MUTED,0x25,'fontsmall')
rect(0,56,280,G('clienth'));fill('brushside');rect(279,56,280,G('clienth'));fill('brushline');rect(24,78,255,103);text(A('folders'),MUTED,0x8820,'fontsmall');e.call('drawtree')
e.get(rax,'clienth');e.subi(rax,30);rect(20,R(rax),270,G('clienth'));text(A('sidebarhint'),MUTED,0x8820,'fontsmall')
rect(304,72,G('clientw'),102);text(A('gallerytitle'),INK,0x8820,'fonttitle');rect(304,104,G('clientw'),127);text(A('path'),MUTED,0x8820,'fontsmall')
e.get(rax,'scroll');e.get(rbx,'cols');e.mul(rax,rbx);e.mov(rbx,rax);e.imm(r12,0);e.imm(r13,148)
e.label('tileloop');e.get(rax,'imagecount');e.cmp(rbx,rax);e.jump('galleryfooter','ge');e.get(rax,'clienth');e.subi(rax,32);e.cmp(r13,rax);e.jump('galleryfooter','ge')
e.mul(r14,rbx,1056);e.lea(rsi,'images');e.add(rsi,r14);e.get(r14,'tilestep');e.mul(r14,r12);e.addi(r14,304)
e.memlea(r8,r14,1);e.memlea(r9,r13,3);e.get(r10,'cardw');e.add(r10,r14);e.addi(r10,1);e.get(r11,'cardh');e.add(r11,r13);e.addi(r11,3);rect(R(r8),R(r9),R(r10),R(r11));roundfill('brushshadow',14)
e.get(rdi,'cardw');e.add(rdi,r14);e.get(r15,'cardh');e.add(r15,r13);rect(R(r14),R(r13),R(rdi),R(r15));roundfill('brushtile',14)
e.memlea(r8,r14,9);e.memlea(r9,r13,9);e.get(r10,'cardw');e.add(r10,r14);e.subi(r10,9);e.get(r11,'previewh');e.add(r11,r13);e.addi(r11,19);rect(R(r8),R(r9),R(r10),R(r11));roundfill('brushbg',8)
e.load(rax,rsi,1024);e.test(rax);e.jump('tileplaceholder','e');e.call(D+'SelectObject',G('srcdc'),R(rax));e.put('oldsrc',rax)
e.load(rdi,rsi,1032);e.load(r15,rsi,1040);e.get(rcx,'previeww');e.cmp(rdi,rcx);short=e.unique();e.jump(short,'le');e.mov(rax,r15);e.mul(rax,rcx);e.div(rdi);e.mov(r15,rax);e.mov(rdi,rcx);e.label(short)
e.get(rcx,'previewh');e.cmp(r15,rcx);short=e.unique();e.jump(short,'le');e.mov(rax,rdi);e.mul(rax,rcx);e.div(r15);e.mov(rdi,rax);e.mov(r15,rcx);e.label(short)
e.get(rax,'cardw');e.sub(rax,rdi);e.shift(rax,1);e.add(rax,r14);e.mov(r8,rax);e.get(rax,'previewh');e.addi(rax,28);e.sub(rax,r15);e.shift(rax,1);e.add(rax,r13);e.load(r10,rsi,1032);e.load(r11,rsi,1040)
e.call(D+'StretchBlt',G('backdc'),R(r8),R(rax),R(rdi),R(r15),G('srcdc'),0,0,R(r10),R(r11),0x00cc0020);e.call(D+'SelectObject',G('srcdc'),G('oldsrc'));e.jump('tilecaption')
e.label('tileplaceholder');e.memlea(r8,r14,12);e.memlea(r9,r13,46);e.get(r10,'cardw');e.add(r10,r14);e.subi(r10,12);e.memlea(r11,r13,108);rect(R(r8),R(r9),R(r10),R(r11));e.load(rax,rsi,1048);e.test(rax);pend=e.unique();penddone=e.unique();e.jump(pend,'e');text(A('failed'),MUTED,0x11,'fontsmall');e.jump(penddone);e.label(pend);text(A('pending'),MUTED,0x11,'fontsmall');e.label(penddone)
e.label('tilecaption');e.memlea(r8,r14,13);e.get(r9,'previewh');e.add(r9,r13);e.addi(r9,27);e.get(r10,'cardw');e.add(r10,r14);e.subi(r10,13);e.memlea(r11,r9,27);rect(R(r8),R(r9),R(r10),R(r11));text(R(rsi))
e.get(rax,'infoview');e.test(rax);nometadraw=e.unique();e.jump(nometadraw,'e');e.mul(rcx,rbx,2048);e.lea(rax,'metadata');e.add(rcx,rax);e.memlea(rdx,r14,14);e.memlea(r8,r13,198);e.call('drawmetadata',R(rcx),R(rdx),R(r8));e.label(nometadraw)
e.call('batchdrawcheck',R(rbx),R(r14),R(r13));e.addi(rbx,1);e.addi(r12,1);e.get(rax,'cols');e.cmp(r12,rax);e.jump('tileloop','l');e.imm(r12,0);e.get(rax,'rowstep');e.add(r13,rax);e.jump('tileloop')
e.label('galleryfooter');e.get(rax,'imagecount');e.test(rax);notempty=e.unique();e.jump(notempty,'ne');rect(320,200,G('clientw'),250);text(A('empty'),MUTED);e.label(notempty)
e.get(rax,'clienth');e.subi(rax,32);rect(280,R(rax),G('clientw'),G('clienth'));fill('brushbg');e.get(rax,'clienth');e.subi(rax,28);rect(304,R(rax),G('clientw'),G('clienth'));e.get(rax,'error');e.test(rax);noerror=e.unique();footdone=e.unique();e.jump(noerror,'e');text(R(rax),rgb(0xb44d44),0x8820,'fontsmall');e.jump(footdone);e.label(noerror);text(A('galleryhint'),MUTED,0x8820,'fontsmall');e.label(footdone);e.call('batchdrawbar');e.jump('paintblit')

e.label('paintpicker');rect(0,0,G('clientw'),G('clienth'));fill('brushdim');relative_rect(3,6,720,560);roundfill('brushmuted',20);relative_rect(0,0,720,560);roundfill('brushwhite',20)
relative_rect(28,20,660,35);text(A('pickerheading'),INK,0x8820,'fonttitle');relative_rect(28,60,660,25);text(A('pickersub'),MUTED,0x8820,'fontsmall')
relative_rect(24,98,672,38);roundfill('brushbg',9);relative_rect(26,100,36,34);text(A('up'),ACCENT,0x25);relative_rect(74,100,606,34);text(A('pickpath'),INK,0x8820,'fontsmall')
e.call('drawtree');relative_rect(24,478,672,1);fill('brushline');relative_rect(24,496,340,38)
e.get(rax,'error');e.test(rax);picknoerror=e.unique();pickfootdone=e.unique();e.jump(picknoerror,'e');text(R(rax),rgb(0xb44d44),0x8810,'fontsmall');e.jump(pickfootdone);e.label(picknoerror);text(A('pickhint'),MUTED,0x8820,'fontsmall');e.label(pickfootdone)
relative_rect(422,496,94,38);roundfill('brushbg',9);text(A('cancel'),INK,0x25)
relative_rect(528,496,168,38);roundfill('brushaccent',9);text(A('choose'),rgb(0xffffff),0x25);e.jump('paintblit')

e.label('paintbatchmodal');e.call('batchdrawmodal');e.jump('paintblit')
e.label('painteditmodal');e.call('editordrawmodal');e.jump('paintblit')
e.label('paintviewer');fill('brushblack');e.get(rbx,'viewbmp');e.get(rdi,'vieww');e.get(rsi,'viewh');e.get(rax,'edpreviewbmp');e.test(rax);renderoriginal=e.unique();e.jump(renderoriginal,'e');e.get(rax,'editoropen');e.get(rcx,'editdirty');e.add(rax,rcx);e.test(rax);e.jump(renderoriginal,'e');e.get(rbx,'edpreviewbmp');e.get(rdi,'edpw');e.get(rsi,'edph');e.label(renderoriginal);e.call(D+'SelectObject',G('srcdc'),R(rbx));e.put('oldsrc',rax);e.call(D+'StretchBlt',G('backdc'),G('vx'),G('vy'),G('vw'),G('vh'),G('srcdc'),0,0,R(rdi),R(rsi),0x00cc0020);e.call(D+'SelectObject',G('srcdc'),G('oldsrc'))
rect(0,0,G('clientw'),60);fill('brushblack')
rect(16,12,184,48);roundfill('brushaccent',9);text(A('backtolist'),rgb(0xffffff),0x25)
rect(196,12,304,48);roundfill('brushaccent',9);e.get(rax,'viewindex');e.test(rax);prevdisabled=e.unique();prevdrawn=e.unique();e.jump(prevdisabled,'e');text(A('previous'),rgb(0xffffff),0x25);e.jump(prevdrawn);e.label(prevdisabled);text(A('previous'),rgb(0x8ca0ad),0x25);e.label(prevdrawn)
rect(316,12,444,48);roundfill('brushaccent',9);e.get(rax,'viewindex');e.addi(rax,1);e.get(rbx,'imagecount');e.cmp(rax,rbx);nextdisabled=e.unique();nextdrawn=e.unique();e.jump(nextdisabled,'ge');text(A('next'),rgb(0xffffff),0x25);e.jump(nextdrawn);e.label(nextdisabled);text(A('next'),rgb(0x8ca0ad),0x25);e.label(nextdrawn)
rect(456,12,602,48);roundfill('brushaccent',9);e.get(rax,'fullscreen');e.test(rax);fsbutton=e.unique();fsbuttondone=e.unique();e.jump(fsbutton,'ne');text(A('fullscreenlabel'),rgb(0xffffff),0x25);e.jump(fsbuttondone);e.label(fsbutton);text(A('windowedlabel'),rgb(0xffffff),0x25);e.label(fsbuttondone);e.call('editordrawtoolbar');e.call('editordrawpanel')
e.get(rax,'clientw');e.subi(rax,150);rect(R(rax),12,G('clientw'),48);text(A('viewcounter'),rgb(0xd9dfe6),0x25)
e.get(rax,'clienth');e.subi(rax,30);rect(0,R(rax),G('clientw'),G('clienth'));fill('brushblack');e.get(rax,'clienth');e.subi(rax,28);rect(16,R(rax),G('clientw'),G('clienth'));e.get(rax,'error');e.test(rax);viewerok=e.unique();viewerfootdone=e.unique();e.jump(viewerok,'e');text(R(rax),rgb(0xe8a39d),0x8820,'fontsmall');e.jump(viewerfootdone);e.label(viewerok);text(A('viewerhint'),rgb(0xd9dfe6),0x8820,'fontsmall');e.label(viewerfootdone)
e.label('paintblit');e.call(D+'BitBlt',G('dc'),0,0,G('clientw'),G('clienth'),G('backdc'),0,0,0x00cc0020);e.call(D+'SelectObject',G('backdc'),G('oldback'));e.call(D+'DeleteObject',G('backbmp'));e.call(D+'DeleteDC',G('srcdc'));e.call(D+'DeleteDC',G('backdc'))
e.label('paintend');e.call(U+'EndPaint',G('hwnd'),A('paint'));e.ret()

# Mouse and keyboard handlers use the exact same layout as the renderer.
def mousecoords():e.mov(rbx,r15);e.shift(rbx,48,4);e.shift(rbx,48);e.mov(rsi,r15);e.shift(rsi,32,4);e.shift(rsi,48)
e.begin('treeclick') # coordinates RCX/RDX; R8 = force toggle
e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r15,r8);e.get(rax,'ty');e.sub(r13,rax);e.cmpi(r13,0);e.jump('treeclickdone','l');e.get(rax,'th');e.cmp(r13,rax);e.jump('treeclickdone','ge');e.get(rax,'tx');e.cmp(r12,rax);e.jump('treeclickdone','l');e.get(rbx,'tw');e.add(rbx,rax);e.cmp(r12,rbx);e.jump('treeclickdone','ge');e.mov(rax,r13);e.imm(rbx,32);e.div(rbx);e.get(rbx,'tscroll');e.add(rax,rbx);e.get(rbx,'tcount');e.cmp(rax,rbx);e.jump('treeclickdone','ge');e.mov(r14,rax);e.mul(rdi,r14,2112);e.get(rax,'tbase');e.add(rdi,rax)
e.load(rax,rdi,2048);e.mul(rax,rax,18);e.get(rbx,'tx');e.add(rax,rbx);e.addi(rax,18);e.test(r15);e.jump('clicktoggle','ne');e.cmp(r12,rax);e.jump('clicktoggle','l')
e.put('tsel',r14);zero('error');e.get(rax,'picker');e.test(rax);mainselect=e.unique();e.jump(mainselect,'e');e.call(K+'lstrcpyW',A('pickpath'),R(rdi));invalidate();e.jump('treeclickdone')
e.label(mainselect);e.call(K+'lstrcpyW',A('path'),R(rdi));e.call('loadfolder');e.jump('treeclickdone')
e.label('clicktoggle');e.call('treetoggle',R(r14))
e.label('treeclickdone');e.ret()

e.begin('wndproc');e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r14,r8);e.mov(r15,r9)
for msg,label in [(1,'wmcreate'),(5,'wmsize'),(0x24,'wmminmax'),(15,'wmpaint'),(20,'wmerase'),(0x10,'wmclose'),(0x113,'wmtimer'),(0x100,'wmkey'),(0x102,'wmchar'),(0x302,'wmpaste'),(0x201,'wmdown'),(0x202,'wmup'),(0x205,'wmrightup'),(0x200,'wmmove'),(0x2a3,'wmmouseleave'),(0x20a,'wmwheel'),(0x203,'wmdouble'),(2,'wmdestroy'),(0x215,'wmcapture')]:e.cmpi(r13,msg);e.jump(label,'e')
e.call(U+'DefWindowProcW',R(r12),R(r13),R(r14),R(r15));e.ret()
e.label('wmcreate');e.put('hwnd',r12);e.jump('returnzero')
e.label('wmminmax');e.imm(rax,920);e.store(r15,24,rax,0);e.imm(rax,700);e.store(r15,28,rax,0);e.jump('returnzero')
e.label('wmsize');e.mov(rax,r15);e.andi(rax,0xffff);e.put('clientw',rax);e.mov(rax,r15);e.shift(rax,16,5);e.andi(rax,0xffff);e.put('clienth',rax);e.get(rax,'clientw');e.subi(rax,304);e.imm(rbx,200);e.div(rbx);e.cmpi(rax,1);cok=e.unique();e.jump(cok,'ge');e.imm(rax,1);e.label(cok);e.put('cols',rax);e.call('layout');e.get(rax,'mode');e.test(rax);sz=e.unique();e.jump(sz,'e');e.get(rax,'viewbmp');e.test(rax);e.jump(sz,'e');e.call('fitview');e.label(sz);invalidate();e.jump('returnzero')
e.label('wmpaint');e.call('paintwindow');e.jump('returnzero')
e.label('wmerase');e.imm(rax,1);e.ret()
e.label('wmclose');e.get(rax,'batchbusy');e.test(rax);notbatchclose=e.unique();e.jump(notbatchclose,'e');e.set('batchcancelled',1);e.jump('returnzero');e.label(notbatchclose);e.call('editorrequest',3,0);e.jump('returnzero')
e.label('wmchar');e.get(rax,'picker');e.test(rax);e.jump('returnzero','ne');e.call('editorchar',R(r14));e.jump('returnzero')
e.label('wmpaste');e.get(rax,'edfocus');e.test(rax);e.jump('returnzero','e');e.call('editorpaste');e.jump('returnzero')
e.label('wmtimer');e.cmpi(r14,5);notbatchtimer=e.unique();e.jump(notbatchtimer,'ne');e.call('batchstep');e.jump('returnzero');e.label(notbatchtimer);e.cmpi(r14,4);notpreviewtimer=e.unique();e.jump(notpreviewtimer,'ne');e.call('batchpreview');e.jump('returnzero');e.label(notpreviewtimer);e.get(rax,'batchbusy');e.test(rax);e.jump('returnzero','ne');e.cmpi(r14,3);notedittimer=e.unique();e.jump(notedittimer,'ne');e.call('editorapply');e.jump('returnzero');e.label(notedittimer);e.cmpi(r14,2);thumbtimer=e.unique();e.jump(thumbtimer,'ne');e.call(U+'KillTimer',G('hwnd'),2);e.get(rax,'mode');e.test(rax);e.jump('returnzero','e');e.call('navigateimage',-1);e.jump('returnzero');e.label(thumbtimer);e.get(rax,'mode');e.test(rax);e.jump('returnzero','ne');e.get(rax,'picker');e.test(rax);e.jump('returnzero','ne');e.call('thumbnail');e.jump('returnzero')
e.label('wmkey');e.call('batchkey',R(r14));e.test(rax);e.jump('returnzero','ne');e.call('editorkey',R(r14));e.test(rax);e.jump('returnzero','ne');e.cmpi(r14,27);notesc=e.unique();e.jump(notesc,'ne');e.get(rax,'picker');e.test(rax);notpick=e.unique();e.jump(notpick,'e');e.call('cancelpicker');e.jump('returnzero');e.label(notpick);e.get(rax,'mode');e.test(rax);keyexit=e.unique();e.jump(keyexit,'e');e.get(rax,'fullscreen');e.test(rax);escviewer=e.unique();e.jump(escviewer,'e');e.call('leavefullscreen');e.jump('returnzero');e.label(escviewer);e.call('closeimage');e.jump('returnzero');e.label(keyexit);e.call(U+'DestroyWindow',R(r12));e.jump('returnzero');e.label(notesc)
e.cmpi(r14,122);notf11=e.unique();e.jump(notf11,'ne');e.get(rax,'mode');e.test(rax);e.jump('returnzero','e');e.call('togglefullscreen');e.jump('returnzero');e.label(notf11)
e.get(rax,'picker');e.test(rax);pickkeys=e.unique();e.jump(pickkeys,'ne');e.get(rax,'mode');e.test(rax);e.jump('returnzero','e');e.cmpi(r14,37);keynext=e.unique();e.jump(keynext,'ne');e.call('navigateimage',-1);e.jump('returnzero');e.label(keynext);e.cmpi(r14,39);e.jump('returnzero','ne');e.call('navigateimage',1);e.jump('returnzero');e.label(pickkeys);e.cmpi(r14,13);notenter=e.unique();e.jump(notenter,'ne');e.call('acceptpicker');e.jump('returnzero');e.label(notenter)
e.cmpi(r14,37);e.jump('keytoggle','e');e.cmpi(r14,39);e.jump('keytoggle','e');e.cmpi(r14,38);e.jump('keyup','e');e.cmpi(r14,40);e.jump('keydown','e');e.jump('returnzero')
e.label('keytoggle');e.get(rbx,'tsel');e.mul(rsi,rbx,2112);e.get(rax,'tbase');e.add(rsi,rax);e.load(rax,rsi,2056);e.cmpi(r14,37);kt=e.unique();e.jump(kt,'ne');e.test(rax);e.jump('returnzero','e');e.call('treetoggle',R(rbx));e.jump('returnzero');e.label(kt);e.test(rax);e.jump('returnzero','ne');e.call('treetoggle',R(rbx));e.jump('returnzero')
e.label('keyup');e.get(rbx,'tsel');e.subi(rbx,1);e.cmpi(rbx,0);e.jump('returnzero','l');e.jump('keyselect')
e.label('keydown');e.get(rbx,'tsel');e.addi(rbx,1);e.get(rax,'tcount');e.cmp(rbx,rax);e.jump('returnzero','ge')
e.label('keyselect');e.put('tsel',rbx);e.mul(rsi,rbx,2112);e.get(rax,'tbase');e.add(rsi,rax);e.call(K+'lstrcpyW',A('pickpath'),R(rsi));e.get(rax,'tscroll');e.cmp(rbx,rax);ks=e.unique();e.jump(ks,'ge');e.put('tscroll',rbx);e.label(ks);e.get(rax,'th');e.imm(rdi,32);e.div(rdi);e.get(rdi,'tscroll');e.add(rdi,rax);e.cmp(rbx,rdi);ks=e.unique();e.jump(ks,'l');e.mov(rdi,rbx);e.sub(rdi,rax);e.addi(rdi,1);e.put('tscroll',rdi);e.label(ks);invalidate();e.jump('returnzero')

e.label('wmdown');mousecoords();zero('error');e.call('batchclick',R(rbx),R(rsi));e.test(rax);e.jump('returnzero','ne');e.call('editorclick',R(rbx),R(rsi));e.test(rax);e.jump('returnzero','ne');zero('edfocus');e.get(rax,'picker');e.test(rax);e.jump('pickerdown','ne');e.get(rax,'mode');e.test(rax);e.jump('viewerdown','ne')
e.cmpi(rsi,56);notmenu=e.unique();e.jump(notmenu,'ge');e.cmpi(rbx,220);viewswitch=e.unique();e.jump(viewswitch,'ge');e.call('openpicker');e.jump('returnzero');e.label(viewswitch);e.cmpi(rbx,244);e.jump('returnzero','l');e.cmpi(rbx,514);e.jump('returnzero','ge');e.cmpi(rbx,398);toinfo=e.unique();e.jump(toinfo,'ge');e.call('setview',0);e.jump('returnzero');e.label(toinfo);e.call('setview',1);e.jump('returnzero');e.label(notmenu)
e.cmpi(rbx,280);e.jump('maintreeclick','l');e.cmpi(rsi,148);e.jump('returnzero','l');e.get(rax,'clienth');e.subi(rax,32);e.cmp(rsi,rax);e.jump('returnzero','ge');e.subi(rbx,304);e.cmpi(rbx,0);e.jump('returnzero','l');e.mov(rax,rbx);e.get(rdi,'tilestep');e.div(rdi);e.get(rdi,'cardw');e.cmp(rdx,rdi);e.jump('returnzero','ge');e.mov(rbx,rax);e.get(rax,'cols');e.cmp(rbx,rax);e.jump('returnzero','ge');e.subi(rsi,148);e.mov(rax,rsi);e.get(rdi,'rowstep');e.div(rdi);e.get(rdi,'cardh');e.cmp(rdx,rdi);e.jump('returnzero','ge');e.get(rdi,'scroll');e.add(rax,rdi);e.get(rdi,'cols');e.mul(rax,rdi);e.add(rax,rbx);e.call('openimage',R(rax));e.jump('returnzero')
e.label('maintreeclick');e.call('treeclick',R(rbx),R(rsi),0);e.jump('returnzero')
e.label('pickerdown');e.get(rax,'px');e.sub(rbx,rax);e.get(rax,'py');e.sub(rsi,rax);e.cmpi(rsi,496);notbuttons=e.unique();e.jump(notbuttons,'l');e.cmpi(rsi,534);e.jump('returnzero','ge');e.cmpi(rbx,528);notchoose=e.unique();e.jump(notchoose,'l');e.cmpi(rbx,696);e.jump('returnzero','ge');e.call('acceptpicker');e.jump('returnzero');e.label(notchoose);e.cmpi(rbx,422);e.jump('returnzero','l');e.cmpi(rbx,516);e.jump('returnzero','ge');e.call('cancelpicker');e.jump('returnzero');e.label(notbuttons)
e.cmpi(rsi,98);notup=e.unique();e.jump(notup,'l');e.cmpi(rsi,136);e.jump(notup,'ge');e.cmpi(rbx,24);e.jump(notup,'l');e.cmpi(rbx,64);e.jump(notup,'ge');e.call('parentpath',A('pickpath'));e.call('treeinit',A('pickpath'),1);invalidate();e.jump('returnzero');e.label(notup);mousecoords();e.call('treeclick',R(rbx),R(rsi),0);e.jump('returnzero')
e.label('viewerdown');e.get(rax,'viewtop');e.cmp(rsi,rax);viewbody=e.unique();e.jump(viewbody,'ge');e.cmpi(rsi,12);e.jump('returnzero','l');e.cmpi(rsi,48);e.jump('returnzero','ge');e.cmpi(rbx,16);e.jump('returnzero','l');e.cmpi(rbx,184);viewprev=e.unique();e.jump(viewprev,'ge');e.call('closeimage');e.jump('returnzero');e.label(viewprev);e.cmpi(rbx,196);e.jump('returnzero','l');e.cmpi(rbx,304);viewnext=e.unique();e.jump(viewnext,'ge');e.call('navigateimage',-1);e.jump('returnzero');e.label(viewnext);e.cmpi(rbx,316);e.jump('returnzero','l');e.cmpi(rbx,444);viewfs=e.unique();e.jump(viewfs,'ge');e.call('navigateimage',1);e.jump('returnzero');e.label(viewfs);e.cmpi(rbx,456);e.jump('returnzero','l');e.cmpi(rbx,602);e.jump('returnzero','ge');e.call('togglefullscreen');e.jump('returnzero');e.label(viewbody)
e.get(rax,'clienth');e.subi(rax,32);e.cmp(rsi,rax);e.jump('returnzero','ge');e.set('lastx',R(rbx));e.set('lasty',R(rsi));e.set('downx',R(rbx));e.set('downy',R(rsi));zero('moved');e.set('drag',1);e.call(U+'SetCapture',R(r12));e.call(U+'LoadCursorW',0,32646);e.call(U+'SetCursor',R(rax));e.jump('returnzero')
e.label('wmup');e.get(rax,'edsliderdrag');e.test(rax);noteditsliderup=e.unique();e.jump(noteditsliderup,'e');zero('edsliderdrag');e.call(U+'ReleaseCapture');e.call('editorapply');e.jump('returnzero');e.label(noteditsliderup);e.get(rax,'drag');e.test(rax);e.jump('returnzero','e');e.get(rbx,'moved');zero('drag');e.call(U+'ReleaseCapture');e.test(rbx);e.jump('returnzero','ne');e.call(U+'GetDoubleClickTime');e.call(U+'SetTimer',G('hwnd'),2,R(rax),0);e.jump('returnzero')
e.label('wmrightup');e.get(rax,'picker');e.test(rax);e.jump('returnzero','ne');e.get(rax,'edmodal');e.test(rax);e.jump('returnzero','ne');e.get(rax,'mode');e.test(rax);e.jump('returnzero','e');mousecoords();e.get(rax,'editoropen');e.test(rax);notpanelright=e.unique();e.jump(notpanelright,'e');e.get(rax,'edpanelx');e.cmp(rbx,rax);e.jump('returnzero','ge');e.label(notpanelright);e.call(U+'KillTimer',G('hwnd'),2);e.call('navigateimage',1);e.jump('returnzero')
e.label('wmcapture');zero('drag');zero('edsliderdrag');e.jump('returnzero')
e.label('wmmove');e.get(rax,'edsliderdrag');e.test(rax);noteditslidermove=e.unique();e.jump(noteditslidermove,'e');e.subi(rax,1);e.mov(rdi,rax);mousecoords();e.call('editorslidervalue',R(rdi),R(rbx));e.jump('returnzero');e.label(noteditslidermove);e.get(rax,'drag');e.test(rax);e.jump('hovermove','e');mousecoords();e.get(rax,'moved');e.test(rax);dragready=e.unique();e.jump(dragready,'ne');e.get(rax,'downx');e.mov(rdi,rbx);e.sub(rdi,rax);dragthreshold=e.unique();e.cmpi(rdi,5);e.jump(dragthreshold,'g');e.cmpi(rdi,-5);e.jump(dragthreshold,'l');e.get(rax,'downy');e.mov(rdi,rsi);e.sub(rdi,rax);e.cmpi(rdi,5);e.jump(dragthreshold,'g');e.cmpi(rdi,-5);e.jump(dragthreshold,'l');e.jump('returnzero');e.label(dragthreshold);e.set('moved',1);e.label(dragready)
e.get(rax,'lastx');e.mov(rdi,rbx);e.sub(rdi,rax);e.get(rax,'vx');e.add(rax,rdi);e.put('vx',rax);e.put('lastx',rbx);e.get(rax,'lasty');e.mov(rdi,rsi);e.sub(rdi,rax);e.get(rax,'vy');e.add(rax,rdi);e.put('vy',rax);e.put('lasty',rsi);e.call('clampview');invalidate();e.jump('returnzero')
e.label('wmmouseleave');zero('batchhover');invalidate();e.jump('returnzero')
e.label('hovermove');mousecoords();e.call('batchhovermove',R(rbx),R(rsi));e.imm(rdi,0);e.get(rax,'picker');e.test(rax);hoverdone=e.unique();e.jump(hoverdone,'ne');e.cmpi(rsi,56);e.jump(hoverdone,'ge');e.cmpi(rbx,220);e.jump(hoverdone,'ge');e.imm(rdi,1);e.label(hoverdone);e.get(rax,'hover');e.cmp(rax,rdi);e.jump('returnzero','e');e.put('hover',rdi);invalidate();e.jump('returnzero')
e.label('wmdouble');e.get(rax,'picker');e.test(rax);dbnormal=e.unique();e.jump(dbnormal,'e');mousecoords();e.call('treeclick',R(rbx),R(rsi),1);e.jump('returnzero');e.label(dbnormal);e.get(rax,'edmodal');e.test(rax);e.jump('returnzero','ne');e.get(rax,'mode');e.test(rax);e.jump('returnzero','e');mousecoords();e.get(rax,'viewtop');e.cmp(rsi,rax);e.jump('returnzero','l');e.get(rax,'editoropen');e.test(rax);dbimage=e.unique();e.jump(dbimage,'e');e.get(rax,'edpanelx');e.cmp(rbx,rax);e.jump('returnzero','ge');e.label(dbimage);e.call(U+'KillTimer',G('hwnd'),2);e.set('moved',1);e.call('fitview');invalidate();e.jump('returnzero')

e.label('wmwheel');e.mov(rcx,r14);e.shift(rcx,32,4);e.shift(rcx,48);e.call('batchwheel',R(rcx));e.test(rax);e.jump('returnzero','ne');e.get(rax,'picker');e.test(rax);skipeditorwheel=e.unique();e.jump(skipeditorwheel,'e');e.mov(rsi,r14);e.shift(rsi,32,4);e.shift(rsi,48);e.jump('treewheel');e.label(skipeditorwheel);e.call(U+'GetCursorPos',A('textrect'));e.call(U+'ScreenToClient',R(r12),A('textrect'));e.get(rcx,'textrect',0,0);e.mov(rdx,r14);e.shift(rdx,32,4);e.shift(rdx,48);e.call('editorwheel',R(rcx),R(rdx));e.test(rax);e.jump('returnzero','ne');e.get(rax,'mode');e.test(rax);e.jump('zoomwheel','ne');e.mov(rsi,r14);e.shift(rsi,32,4);e.shift(rsi,48);mousecoords();e.set('textrect',R(rbx),0,0);e.set('textrect',R(rsi),4,0);e.call(U+'ScreenToClient',R(r12),A('textrect'));e.get(rbx,'textrect',0,0);e.mov(rsi,r14);e.shift(rsi,32,4);e.shift(rsi,48);e.cmpi(rbx,280);e.jump('treewheel','l')
e.get(rbx,'scroll');e.cmpi(rsi,0);wu=e.unique();wc=e.unique();e.jump(wu,'g');e.addi(rbx,1);e.jump(wc);e.label(wu);e.subi(rbx,1);e.label(wc);e.get(rax,'imagecount');e.get(rdi,'cols');e.add(rax,rdi);e.subi(rax,1);e.div(rdi);e.mov(rdi,rax);e.get(rax,'clienth');e.subi(rax,180);e.get(rcx,'batchcount');e.test(rcx);nobatchscroll=e.unique();e.jump(nobatchscroll,'e');e.subi(rax,116);e.label(nobatchscroll);e.get(rcx,'rowstep');e.div(rcx);e.cmpi(rax,1);vr=e.unique();e.jump(vr,'ge');e.imm(rax,1);e.label(vr);e.sub(rdi,rax);e.cmp(rbx,rdi);wr=e.unique();e.jump(wr,'le');e.mov(rbx,rdi);e.label(wr);e.cmpi(rbx,0);wr=e.unique();e.jump(wr,'ge');e.imm(rbx,0);e.label(wr);e.put('scroll',rbx);invalidate();e.jump('returnzero')
e.label('treewheel');e.get(rbx,'tscroll');e.cmpi(rsi,0);tu=e.unique();tc=e.unique();e.jump(tu,'g');e.addi(rbx,3);e.jump(tc);e.label(tu);e.subi(rbx,3);e.label(tc);e.get(rax,'th');e.imm(rdi,32);e.div(rdi);e.get(rdi,'tcount');e.sub(rdi,rax);e.cmp(rbx,rdi);tr=e.unique();e.jump(tr,'le');e.mov(rbx,rdi);e.label(tr);e.cmpi(rbx,0);tr=e.unique();e.jump(tr,'ge');e.imm(rbx,0);e.label(tr);e.put('tscroll',rbx);invalidate();e.jump('returnzero')
e.label('zoomwheel');e.call(U+'GetCursorPos',A('textrect'));e.call(U+'ScreenToClient',R(r12),A('textrect'));e.get(rbx,'scale');e.mov(rsi,r14);e.shift(rsi,32,4);e.shift(rsi,48);e.mov(rax,rbx);e.cmpi(rsi,0);zo=e.unique();za=e.unique();e.jump(zo,'l');e.mul(rax,rax,5);e.imm(rdi,4);e.div(rdi);e.jump(za);e.label(zo);e.mul(rax,rax,4);e.imm(rdi,5);e.div(rdi);e.label(za);e.get(rdi,'fit');e.shift(rdi,2);e.cmpi(rdi,1);zmin=e.unique();e.jump(zmin,'ge');e.imm(rdi,1);e.label(zmin);e.cmp(rax,rdi);zmin=e.unique();e.jump(zmin,'ge');e.mov(rax,rdi);e.label(zmin);e.get(rdi,'fit');e.cmpi(rdi,32768);zmax=e.unique();e.jump(zmax,'ge');e.imm(rdi,32768);e.label(zmax);e.cmp(rax,rdi);zmax=e.unique();e.jump(zmax,'le');e.mov(rax,rdi);e.label(zmax);e.mov(rsi,rax);e.put('scale',rax)
for off,pos in [(0,'vx'),(4,'vy')]:e.get(rdi,'textrect',off,0);e.get(rax,pos);e.mov(rcx,rdi);e.sub(rcx,rax);e.mov(rax,rcx);e.mul(rax,rsi);e.div(rbx);e.sub(rdi,rax);e.put(pos,rdi)
e.call('clampview');invalidate();e.jump('returnzero')
e.label('wmdestroy');e.call(U+'KillTimer',R(r12),1);e.call(U+'KillTimer',R(r12),2);e.call(U+'KillTimer',R(r12),3);e.call(U+'PostQuitMessage',0);e.jump('returnzero')
e.label('returnzero');e.imm(rax,0);e.ret()
