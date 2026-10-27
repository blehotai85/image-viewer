"""Build-time constants for the native pixel editor. No runtime dependencies."""
import math
EDITOR_NAMES=['Fényerő','Kontraszt','Szaturáció','Fehérpont','Feketepont','Élesítés','Gamma','Színárnyalat','Színhőmérséklet']
for i,name in enumerate(EDITOR_NAMES):wide('edlabel'+str(i),name)
for n,t in {
 'editbutton':'Szerkesztés','edtitle':'Korrekciók','edresetall':'Összes reset','edreset':'↺',
 'edhistR':'R','edhistG':'G','edhistB':'B','edhistAll':'Teljes',
 'edsave':'Mentés','edsaveas':'Mentés másként…','edpresetheading':'PRESETEK','edpresetname':'Preset neve',
 'edpresetstore':'Preset mentése','edpresetempty':'Még nincs elmentett preset.',
 'edoverwrite':'Felülírjuk az eredeti fájlt?','edoverwritebody':'A módosított képet a kiválasztott fájl helyére mentjük.',
 'edyes':'Felülírás','edcancel':'Mégse','edunsaved':'Mentetlen módosítások',
 'edunsavedbody':'Szeretnéd elmenteni a képen végzett módosításokat?',
 'eddiscard':'Elvetés','edfilename':'Fájlnév','eddirectory':'Mappa','edbrowse':'Tallózás…',
 'edoriginalformat':'Eredeti','edpng':'PNG','edjpeg':'JPEG','edsaveastitle':'Mentés másként',
 'editedsuffix':'_szerkesztett','edpresetfile':'presets.json','edpresettemp':'presets.json.tmp',
 'edjsonstart':'{"version":1,"presets":[','edjsonentry':'{"name":"','edjsonvalues':'","values":[',
 'edjsonentryend':']}','edjsonend':']}','edcomma':',','edminus':'-',
 'ednamekey':'"name"','edvalueskey':'"values"','edtmpfragment':'.kpt-',
 'edtempsuffix':'.tmp','edsaving':'A teljes felbontású kép mentése…',
 'edsaved':'A kép mentése sikerült.','edsavefailed':'A mentés nem sikerült. Az eredeti fájl megmaradt.',
 'edcodecfailed':'Ehhez a formátumhoz nincs működő kódoló. Válassz PNG-t vagy JPEG-et.',
 'edpresetfailed':'A presetek nem menthetők a program könyvtárába.',
 'edpresetbad':'A presetfájl nem olvasható. Az új preset mentése felülírhatja.',
 'edpresetok':'A presetet elmentettük.','ednameempty':'Adj nevet a presetnek.',
 'edinvalidname':'Adj érvényes fájlnevet és létező célmappát.',
 'edjpegquality':'ImageQuality','eddirtyhint':'A mentetlen változtatások csak mentéskor kerülnek a fájlba.',
 'edclean':'Nincs mentetlen módosítás',
}.items():wide(n,t)
for n,g in [('containerpng','1b7cfaf4-713f-473c-bbcd-6137425faeaf'),('containerjpeg','19e4a5aa-5662-4fc5-a0c0-1758028e1057'),('containerheif','e1e62521-6787-405b-a339-500715b5763f'),('blockreaderIID','feaa2a8d-b3f3-43e4-b25c-d1de990a1ae1'),('blockwriterIID','08fb9676-b444-41e8-8dbe-6a53a542bff1')]:blob(n,uuid.UUID(g).bytes_le)
gamma=bytearray()
for value in range(-100,101):
    power=2.0**(-value/100.0)
    gamma.extend(max(0,min(255,round(255*(i/255)**power))) for i in range(256))
blob('gammaluts',gamma)
hues=bytearray()
for angle in range(-180,181):
    c=math.cos(math.radians(angle));s=math.sin(math.radians(angle))
    m=[.213+.787*c-.213*s,.715-.715*c-.715*s,.072-.072*c+.928*s,
       .213-.213*c+.143*s,.715+.285*c+.140*s,.072-.072*c-.283*s,
       .213-.213*c-.787*s,.715-.715*c+.715*s,.072+.928*c+.072*s]
    for v in m:hues.extend(struct.pack('<q',round(v*16384)))
blob('huematrices',hues)
blob('lumaweights',struct.pack('<qqq',3490,11714,1180))
blob('qualityvariant',struct.pack('<HHHHf12x',4,0,0,0,.95))
for n,size in {
 'edvalues':72,'edmatrix':72,'edlut':3*256*4,'edhist':4*256*4,'edhistpoints':256*8,
 'edpresets':64*256,'edname':128,'edoutname':1024,'edoutdir':65536,'edtarget':65536,
 'edtempfile':65536,'edoriginalfile':65536,'edpresetpath':65536,'edpresettemppath':65536,
 'edjsonwide':131072,'edjsonbytes':131072,'ednumtemp':128,'edfmtguid':16,'edqualitybag':40,
 'edmetadataPV':24,'edtextsize':8,'edcarettemp':1024,'edpresetentrytemp':256,
}.items():reserve(n,size)
for n in ['editoropen','editdirty','edscroll','edsliderdrag','edmodal','edfocus','edselectall','edcaret',
 'edpresetcount','edpresetscroll','edpending','edpendingparam','edpickerpurpose','edformat','edbusy',
 'edbasebmp','edbasepixels','edworkbmp','edworkpixels','edpreviewbmp','edpreviewpixels','edpw','edph',
 'originalpixels','edsrcdc','eddstdc','edoldsrc','edolddst','edpanelx','edpaneltop','edpanelheight',
 'viewportw','viewporth','viewtop','procsrc','procdst','procwork','procwidth','procheight','procstride',
 'edfullbmp','edfullpixels','edfullwork','edstream','edencoder','edframe','edbag','edwicbitmap','edconverter',
 'edsourceDecoder','edsourceFrame','edblockreader','edblockwriter','edwritehandle','edbyteswritten',
 'edreadhandle','edbytesread','edjsoncursor','edjsonendptr','edtemporary','edsavepurpose','edpresetloaded',
 'histpenR','histpenG','histpenB','histpenAll','edrange','edcapturekind','edmx','edmy','edencoded','edcontainer']:
    reserve(n,8)
wide('settingslastkey','"lastDirectory"');wide('settingspresetsstart','","presets":[');wide('settingslegacyname','presets.json')
reserve('settingslastdir',65536);reserve('settingsescape',8192);reserve('settingslegacypath',65536);reserve('settingsdirty',8)
