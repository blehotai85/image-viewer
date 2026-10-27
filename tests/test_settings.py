"""Native settings.json round-trips, directory restoration and migration."""
import pathlib,json,ctypes as c
from native_test_host import NativeHost
root=pathlib.Path(__file__).resolve().parent.parent
d=root/'tests'/'.work'/'settings-check';d.mkdir(parents=True,exist_ok=True)
folder=d/'árvíztűrő-tükörfúrógép hosszú mappanév a hatvannégy karakteres korláton túl';folder.mkdir(exist_ok=True)
out=d/'settings.json';temp=d/'settings.json.tmp';legacy=d/'presets.json'
h=NativeHost()
try:
    settings={'version':1,'lastDirectory':str(folder),'presets':[{'name':'User preset "A"','values':[1,2,3,4,5,6,7,8,9]}]}
    h.wide('edjsonwide',json.dumps(settings,ensure_ascii=True));h.call('editorparsepresets')
    assert h.readwide('settingslastdir')==str(folder) and h.get('edpresetcount')==1
    h.wide('path',root);h.call('settingsrestorefolder');assert h.readwide('path')==str(folder)
    h.wide('settingslastdir',folder/'missing');h.wide('path',root);h.call('settingsrestorefolder');assert h.readwide('path')==str(root)
    h.wide('edpresetpath',out);h.wide('edpresettemppath',temp);h.wide('path',folder);h.call('settingsrememberfolder')
    saved=json.loads(out.read_text(encoding='utf8'));assert saved['lastDirectory']==str(folder);assert saved['presets']==settings['presets']
    h.wide('settingslastdir','');h.put('edpresetcount',0);h.call('editorreadpresetfile');assert h.readwide('settingslastdir')==str(folder) and h.get('edpresetcount')==1
    h.wide('path',d);h.call('settingsrememberfolder');assert json.loads(out.read_text(encoding='utf8'))['lastDirectory']==str(d)
    h.wide('path',folder);h.call('loadfolder');assert json.loads(out.read_text(encoding='utf8'))['lastDirectory']==str(folder)
    h.wide('path',folder/'missing');h.call('loadfolder');assert json.loads(out.read_text(encoding='utf8'))['lastDirectory']==str(folder)
    # An existing settings file takes precedence and is never replaced by legacy data.
    legacy.write_text(json.dumps({'version':1,'presets':[]}),encoding='utf8');h.wide('settingslegacypath',legacy);before=out.read_bytes();h.call('settingsmigratelegacy');assert out.read_bytes()==before and legacy.exists()
    # With no settings file, rename the legacy file in place and keep all presets.
    migrated=d/'migrated-settings.json'
    if migrated.exists():migrated.unlink()
    legacy.write_text(json.dumps(settings,ensure_ascii=False),encoding='utf8');h.wide('edpresetpath',migrated);h.call('settingsmigratelegacy');assert migrated.exists() and not legacy.exists();h.call('editorreadpresetfile');assert h.get('edpresetcount')==1 and h.readwide('settingslastdir')==str(folder)
    # UI strings are embedded in English; user names and paths remain Unicode.
    for key,value in [('title','Photo Gallery'),('edyes','Overwrite'),('batchcopy','Save all as copies'),('edpresetfile','settings.json'),('editedsuffix','_szerkesztett')]:assert h.readwide(key)==value
    binary=(root/'Gallery.check.exe').read_bytes()
    for old in ['Mappa megnyitása','Mentetlen módosítások','Összes mentése','Nincs mentetlen módosítás']:assert old.encode('utf-16le') not in binary
    print('PASS: English UI, Unicode/long folder paths, persistence, restore, missing-folder fallback, preset preservation and legacy migration.')
finally:h.close()
