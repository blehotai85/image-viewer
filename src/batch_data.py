"""Build-time constants for gallery selection and batch processing."""
BUILTIN_PRESETS=[('kodacolor 400',[3,8,-8,-4,-3,8,2,0,8]),('kodacolor 800',[6,3,-12,-8,-5,10,6,0,12]),('kodachome 64',[-2,28,22,8,4,18,-4,0,4])]
for i,(name,values) in enumerate(BUILTIN_PRESETS):wide('builtinname'+str(i),name);blob('builtinvalues'+str(i),struct.pack('<9q',*values))
for n,t in {'batchall':'Összes','batchnone':'Semelyik','batchselectedsuffix':' kijelölve','batchchoose':'Válassz presetet…',
 'batchsave':'Összes mentése','batchcopy':'Összes mentése másolatként','batchcheck':'✓','batchoverwrite':'Kijelölt képek felülírása',
 'batchconfirmbody':'A kiválasztott presetet alkalmazzuk, és az összes kijelölt eredeti fájlt felülírjuk.',
 'batchstart':'Felülírás indítása','batchcancel':'Mégse','batchworking':'Képek feldolgozása','batchstop':'Leállítás a kép után',
 'batchdoneheading':'Kötegelt feldolgozás kész','batchdoneprefix':'Mentve: ','batcherrorprefix':'    Sikertelen: ','batchok':'Rendben',
 'batchneedpreset':'Előbb válassz egy presetet a kijelölt képekhez.','batchunderscore':'_','batchunknown':'Nem sikerült feldolgozni a képet.',
 'batchstopped':'A feldolgozást leállítottuk.','batchcopycollision':'Nem található szabad másolatnév.','batchfirsterror':'Első sikertelen fájl:',
}.items():wide(n,t)
for n,size in [('batchselection',16384*8),('batchversions',16384*8),('batchvalues',72),('batchcounttext',128),('batchsummary',256),('batchsourcepath',65536),('batcherrorpath',65536),('batchcounter',128),('batchnamebase',1024),('batchext',64),('batchtrack',24)]:reserve(n,size)
for n in ['batchcount','batchhover','batchgeneration','batchscan','batchhaspreset','batchdropdown','batchdropfirst','batchconfirm','batchbusy','batchcancelled','batchcursor','batchprocessed','batchfailed','batchcopyflag','batchsourcebmp','batchdone','batchtotal','batchadded']:
    reserve(n,8)
for n in ['batchpreviewbmp','batchpreviewpixels','batchpreviewwork','batcherrorreason','batchdropheight']:reserve(n,8)
reserve('batchpresetname',128);reserve('batchforcepng',8)
