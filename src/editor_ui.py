"""Emit own editor panel, sliders, histogram charts and modal windows."""
def panelrect(x,y,w,h,content=True):
    e.get(r8,'edpanelx');e.addi(r8,x);e.get(r9,'viewtop');e.addi(r9,y+(48 if content else 0))
    if content:e.get(rax,'edscroll');e.sub(r9,rax)
    e.memlea(r10,r8,w);e.memlea(r11,r9,h);rect(R(r8),R(r9),R(r10),R(r11))
def modalrect(x,y,w,h):
    e.get(r8,'edmx');e.addi(r8,x);e.get(r9,'edmy');e.addi(r9,y);e.memlea(r10,r8,w);e.memlea(r11,r9,h);rect(R(r8),R(r9),R(r10),R(r11))
def field(value,focus,placeholder=None):
    e.get(rax,'edfocus');e.cmpi(rax,focus);notfocus=e.unique();fieldbgdone=e.unique();e.jump(notfocus,'ne');roundfill('brushselect',8);e.jump(fieldbgdone);e.label(notfocus);roundfill('brushbg',8);e.label(fieldbgdone)
    e.get(r8,'textrect',0,0);e.addi(r8,9);e.get(r9,'textrect',4,0);e.get(r10,'textrect',8,0);e.subi(r10,9);e.get(r11,'textrect',12,0);rect(R(r8),R(r9),R(r10),R(r11))
    if placeholder:
        e.val(rax,value);word(rax,rax);e.test(rax);nonempty=e.unique();fielddone=e.unique();e.jump(nonempty,'ne');text(A(placeholder),MUTED);e.jump(fielddone);e.label(nonempty);text(value);e.label(fielddone)
    else:text(value)
    # Keep a visible focus indicator even when the string is ellipsized.
    e.get(rax,'edfocus');e.cmpi(rax,focus);nofocusline=e.unique();e.jump(nofocusline,'ne');e.get(r8,'textrect',0,0);e.get(r9,'textrect',12,0);e.subi(r9,3);e.get(r10,'textrect',8,0);e.memlea(r11,r9,1);rect(R(r8),R(r9),R(r10),R(r11));fill('brushaccent');e.label(nofocusline)

e.begin('editordrawhist');e.mov(r12,rcx);e.mov(r13,rdx);e.mov(r14,r8);e.lea(r15,'edhist');e.mul(rax,r14,1024);e.add(r15,rax);e.imm(rbx,0);e.imm(rsi,1)
e.label('histmaximum');e.mul(rax,rbx,4);e.mov(rcx,r15);e.add(rcx,rax);e.load(rax,rcx,0,0);e.cmp(rax,rsi);hm=e.unique();e.jump(hm,'le');e.mov(rsi,rax);e.label(hm);e.addi(rbx,1);e.cmpi(rbx,256);e.jump('histmaximum','l');e.imm(rbx,0);e.lea(rdi,'edhistpoints')
e.label('histpoints');e.mov(rax,r12);e.add(rax,rbx);e.store(rdi,0,rax,0);e.mul(rax,rbx,4);e.mov(rcx,r15);e.add(rcx,rax);e.load(rax,rcx,0,0);e.mul(rax,rax,23);e.div(rsi);e.memlea(rcx,r13,24);e.sub(rcx,rax);e.store(rdi,4,rcx,0);e.addi(rdi,8);e.addi(rbx,1);e.cmpi(rbx,256);e.jump('histpoints','l')
for i,n in enumerate(['histpenR','histpenG','histpenB','histpenAll']):
    hp=e.unique();e.cmpi(r14,i);e.jump(hp,'ne');e.call(D+'SelectObject',G('backdc'),G(n));e.label(hp)
e.call(D+'Polyline',G('backdc'),A('edhistpoints'),256);e.ret()

e.begin('editordrawpanel');e.get(rax,'editoropen');e.test(rax);dpdone=e.unique();e.jump(dpdone,'e');e.get(r8,'edpanelx');e.get(r9,'viewtop');rect(R(r8),R(r9),G('clientw'),G('clienth'));fill('brushwhite')
panelrect(0,0,1,1600,False);fill('brushline');panelrect(16,8,148,34,False);text(A('edtitle'));panelrect(166,8,158,34,False);roundfill('brushbg',8);text(A('edresetall'),ACCENT,0x25,'fontsmall')
e.call(D+'SaveDC',G('backdc'));e.put('clip',rax);e.get(r8,'edpanelx');e.get(r9,'viewtop');e.addi(r9,48);e.get(r11,'clienth');e.subi(r11,84);e.call(D+'IntersectClipRect',G('backdc'),R(r8),R(r9),G('clientw'),R(r11))
for i,name in enumerate(['edhistR','edhistG','edhistB','edhistAll']):
    panelrect(16,8+i*32,48,26);text(A(name),MUTED,0x8820,'fontsmall');panelrect(70,8+i*32,256,26);roundfill('brushbg',4);e.get(rcx,'edpanelx');e.addi(rcx,70);e.get(rdx,'viewtop');e.addi(rdx,48+8+i*32);e.get(rax,'edscroll');e.sub(rdx,rax);e.call('editordrawhist',R(rcx),R(rdx),i)
for i in range(9):
    y=168+i*54
    panelrect(18,y,198,23);text(A('edlabel'+str(i)),INK,0x8820,'fontsmall')
    e.get(r12,'edvalues',i*8);e.cmpi(r12,0);positive=e.unique();valuefmt=e.unique();e.jump(positive,'ge');e.call(K+'lstrcpyW',A('ednumtemp'),A('edminus'));e.imm(rax,0);e.sub(rax,r12);e.call('uinttext',R(rax),A('numberbuf'));e.call(K+'lstrcatW',A('ednumtemp'),A('numberbuf'));e.jump(valuefmt);e.label(positive);e.call('uinttext',R(r12),A('ednumtemp'));e.label(valuefmt)
    panelrect(224,y,60,23);text(A('ednumtemp'),ACCENT,0x22,'fontsmall');panelrect(294,y,32,25);roundfill('brushbg',6);text(A('edreset'),MUTED,0x25)
    panelrect(18,y+33,256,4);roundfill('brushline',4)
    e.get(rax,'edvalues',i*8);lo=0 if i==5 else (-180 if i==7 else -100);hi=180 if i==7 else 100;e.subi(rax,lo);e.mul(rax,rax,256);e.imm(rbx,hi-lo);e.div(rbx);e.mov(r12,rax)
    e.get(r8,'edpanelx');e.addi(r8,18);e.get(r9,'viewtop');e.addi(r9,48+y+33);e.get(rax,'edscroll');e.sub(r9,rax);e.mov(r10,r8);e.add(r10,r12);e.memlea(r11,r9,4);rect(R(r8),R(r9),R(r10),R(r11));roundfill('brushaccent',4)
    e.get(r8,'edpanelx');e.addi(r8,18-6);e.add(r8,r12);e.get(r9,'viewtop');e.addi(r9,48+y+29);e.get(rax,'edscroll');e.sub(r9,rax);e.memlea(r10,r8,13);e.memlea(r11,r9,13);rect(R(r8),R(r9),R(r10),R(r11));e.call(D+'SelectObject',G('backdc'),G('brushaccent'));e.call(D+'SelectObject',G('backdc'),G('nullpen'));e.get(r8,'textrect',0,0);e.get(r9,'textrect',4,0);e.get(r10,'textrect',8,0);e.get(r11,'textrect',12,0);e.call(D+'Ellipse',G('backdc'),R(r8),R(r9),R(r10),R(r11))
panelrect(18,680,300,24);text(A('edpresetheading'),MUTED,0x8820,'fontsmall');panelrect(18,712,308,34);field(A('edname'),1,'edpresetname');panelrect(18,758,308,34);roundfill('brushaccent',8);text(A('edpresetstore'),rgb(0xffffff),0x25)
e.get(rax,'edpresetcount');e.test(rax);haspresets=e.unique();e.jump(haspresets,'ne');panelrect(18,812,308,30);text(A('edpresetempty'),MUTED,0x8820,'fontsmall');e.jump('drawpresetsdone');e.label(haspresets);e.imm(r12,0)
e.label('drawpresetlist');e.get(rax,'edpresetcount');e.cmp(r12,rax);e.jump('drawpresetsdone','ge');e.mul(r13,r12,256);e.lea(rax,'edpresets');e.add(r13,rax);e.mul(r14,r12,34);e.addi(r14,810);e.get(r8,'edpanelx');e.addi(r8,18);e.get(r9,'viewtop');e.addi(r9,48);e.add(r9,r14);e.get(rax,'edscroll');e.sub(r9,rax);e.memlea(r10,r8,308);e.memlea(r11,r9,30);rect(R(r8),R(r9),R(r10),R(r11));e.call(K+'lstrcmpiW',R(r13),A('edname'));e.test(rax,0);unselected=e.unique();presetbg=e.unique();e.jump(unselected,'ne');roundfill('brushselect',6);e.jump(presetbg);e.label(unselected);roundfill('brushbg',6);e.label(presetbg);text(R(r13),INK,0x8820,'fontsmall');e.addi(r12,1);e.jump('drawpresetlist')
e.label('drawpresetsdone');e.call(D+'RestoreDC',G('backdc'),G('clip'))
# A fixed footer belongs to the panel, so dirty/clean transitions never move UI.
e.get(r8,'edpanelx');e.get(r9,'clienth');e.subi(r9,84);e.get(r11,'clienth');e.subi(r11,32);rect(R(r8),R(r9),G('clientw'),R(r11));fill('brushwhite');e.get(r8,'edpanelx');e.get(r9,'clienth');e.subi(r9,84);e.memlea(r11,r9,1);rect(R(r8),R(r9),G('clientw'),R(r11));fill('brushline')
e.get(rax,'editdirty');e.test(rax);cleanfooter=e.unique();savefooterdone=e.unique();e.jump(cleanfooter,'e')
for x,w,caption in [(16,96,'edsave'),(124,200,'edsaveas')]:
    e.get(r8,'edpanelx');e.addi(r8,x);e.get(r9,'clienth');e.subi(r9,75);e.memlea(r10,r8,w);e.memlea(r11,r9,34);rect(R(r8),R(r9),R(r10),R(r11));roundfill('brushaccent',8);text(A(caption),rgb(0xffffff),0x25,'fontsmall')
e.jump(savefooterdone);e.label(cleanfooter);e.get(r8,'edpanelx');e.addi(r8,16);e.get(r9,'clienth');e.subi(r9,75);e.memlea(r10,r8,308);e.memlea(r11,r9,34);rect(R(r8),R(r9),R(r10),R(r11));text(A('edclean'),MUTED,0x25,'fontsmall');e.label(savefooterdone);e.label(dpdone);e.ret()

e.begin('editormodallayout');e.get(rax,'edmodal');e.cmpi(rax,2);smallmodal=e.unique();layoutmodaldone=e.unique();e.jump(smallmodal,'ne');e.imm(rbx,720);e.imm(rsi,430);e.jump(layoutmodaldone);e.label(smallmodal);e.imm(rbx,640);e.imm(rsi,280);e.label(layoutmodaldone);e.get(rax,'clientw');e.sub(rax,rbx);e.shift(rax,1);e.put('edmx',rax);e.get(rax,'clienth');e.sub(rax,rsi);e.shift(rax,1);e.put('edmy',rax);e.ret()
e.begin('editordrawmodal');e.call('editormodallayout');rect(0,0,G('clientw'),G('clienth'));fill('brushdim');e.get(rax,'edmodal');e.cmpi(rax,2);smallpaint=e.unique();e.jump(smallpaint,'ne');modalrect(0,0,720,430);roundfill('brushwhite',18);e.jump('modalpaintbody');e.label(smallpaint);modalrect(0,0,640,280);roundfill('brushwhite',18)
e.label('modalpaintbody');e.get(rax,'edbusy');e.test(rax);notbusy=e.unique();e.jump(notbusy,'e');modalrect(28,72,580,84);text(A('edsaving'),INK,0x8810,'fonttitle');e.jump('modalpaintdone');e.label(notbusy)
e.get(rax,'edmodal');e.cmpi(rax,2);e.jump('paintsaveas','e');e.cmpi(rax,3);e.jump('paintunsaved','e')
modalrect(26,22,588,40);text(A('edoverwrite'),INK,0x8820,'fonttitle');modalrect(26,82,588,34);text(A('edoverwritebody'));modalrect(26,122,588,44);text(A('edtarget'),MUTED,0x8810,'fontsmall');modalrect(330,212,126,38);roundfill('brushbg',8);text(A('edcancel'),INK,0x25);modalrect(468,212,146,38);roundfill('brushaccent',8);text(A('edyes'),rgb(0xffffff),0x25);e.jump('modalpaintdone')
e.label('paintunsaved');modalrect(26,22,588,40);text(A('edunsaved'),INK,0x8820,'fonttitle');modalrect(26,82,588,48);text(A('edunsavedbody'));modalrect(26,134,588,36);text(A('edoriginalfile'),MUTED,0x8820,'fontsmall')
for x,w,caption,brush,color in [(208,112,'edsave','brushaccent',rgb(0xffffff)),(332,112,'eddiscard','brushbg',INK),(456,158,'edcancel','brushbg',INK)]:modalrect(x,212,w,38);roundfill(brush,8);text(A(caption),color,0x25)
e.jump('modalpaintdone')
e.label('paintsaveas');modalrect(26,20,668,40);text(A('edsaveastitle'),INK,0x8820,'fonttitle');modalrect(24,70,672,24);text(A('eddirectory'),MUTED,0x8820,'fontsmall');modalrect(24,96,552,36);field(A('edoutdir'),3);modalrect(588,96,108,36);roundfill('brushbg',8);text(A('edbrowse'),ACCENT,0x25,'fontsmall');modalrect(24,150,672,24);text(A('edfilename'),MUTED,0x8820,'fontsmall');modalrect(24,176,672,36);field(A('edoutname'),2)
for i,cap in enumerate(['edoriginalformat','edpng','edjpeg']):
    modalrect(24+i*160,232,148,36);e.get(rax,'edformat');e.cmpi(rax,i);formatnotselected=e.unique();formatpainted=e.unique();e.jump(formatnotselected,'ne');roundfill('brushselect',8);e.jump(formatpainted);e.label(formatnotselected);roundfill('brushbg',8);e.label(formatpainted);text(A(cap),ACCENT,0x25)
e.get(rax,'error');e.test(rax);nomodalerror=e.unique();e.jump(nomodalerror,'e');modalrect(24,282,672,58);text(G('error'),rgb(0xb44d44),0x8810,'fontsmall');e.label(nomodalerror);modalrect(416,356,100,38);roundfill('brushbg',8);text(A('edcancel'),INK,0x25);modalrect(528,356,168,38);roundfill('brushaccent',8);text(A('edsave'),rgb(0xffffff),0x25)
e.label('modalpaintdone');e.ret()

e.begin('editordrawtoolbar');rect(614,12,728,48);e.get(rax,'editoropen');e.test(rax);editclosed=e.unique();edbuttondone=e.unique();e.jump(editclosed,'e');roundfill('brushselect',9);text(A('editbutton'),ACCENT,0x25);e.jump(edbuttondone);e.label(editclosed);roundfill('brushaccent',9);text(A('editbutton'),rgb(0xffffff),0x25);e.label(edbuttondone)
e.ret()
