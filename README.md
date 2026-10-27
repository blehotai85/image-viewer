# Photo Gallery — native Windows x64

Run `Gallery.exe`. Python and the source files are not needed at runtime.

This is a small native Windows x64 photo browser and editor. It includes a custom folder picker, gallery, image viewer, editing panel, presets and batch processing. The executable is included in the repository. Local preferences are created automatically in `settings.json` and are not tracked by Git.

## Repository layout

```text
Gallery.exe          Ready-to-run native Windows x64 application
src/                 Python-based x64 instruction emitter and code generators
tests/               Native tests, fixture generation and test runner
README.md            Usage, build and test instructions
settings.json        Local preferences, generated at runtime and Git-ignored
```

## Folders and views

The light-gray interface, folder tree, icons, controls and dialogs are custom drawn. The UI, prompts and errors are in English. Actual file/folder names and user-created preset names are preserved.

**Open folder** opens the custom picker. Arrows appear only beside folders with accessible subfolders. **Thumbnails / Info view** switches between compact cards and cards with file size, original dimensions and available camera, date, aperture and ISO metadata.

PNG, JPEG, HEIC and HEIF use Windows Imaging Component (WIC). HEIC support depends on installed Windows codecs; the application does not install them.

## Settings

Presets and the last successfully opened folder are stored together in **`settings.json` beside `Gallery.exe`**:

```json
{
  "version": 1,
  "lastDirectory": "C:\\Photos",
  "presets": [
    {"name": "My preset", "values": [0, 0, 0, 0, 0, 0, 0, 0, 0]}
  ]
}
```

Value order: brightness, contrast, saturation, white point, black point, sharpening, gamma, hue, temperature.

Folder changes are saved immediately without losing preset order or values. Startup restores the last folder if it exists; otherwise the application folder is used. Failed folder opens do not replace the saved directory. Unicode paths and JSON escaping are supported. Settings are written through a flushed temporary file and atomic replacement.

If `settings.json` does not exist, an older `presets.json` is renamed and loaded. An existing settings file takes precedence. Up to 64 presets with 63 UTF-16-code-unit names are supported. Selecting a preset moves it to the top of the most-recently-used list. Saving the same name updates it.

Built-ins: **kodacolor 400**, **kodacolor 800**, **kodachome 64**, with the requested spelling. These are film-inspired combinations of the available adjustments, not measured film-emulsion profiles or grain simulations. Missing built-ins are added without replacing existing settings with the same name.

## Viewer and editing

- Click a card to open the original-resolution image, initially fitted to the viewport.
- **Previous / Next / Back to gallery** navigate within the folder. Left click: previous; right click: next. Keyboard Left/Right also navigate.
- Wheel zooms around the pointer. Left-button dragging pans without navigating. Double-click fits the image. Single left-click navigation waits for the Windows double-click interval.
- **Full screen** or F11 enters borderless full screen. **Windowed** or F11 restores the previous placement. The first Esc leaves full screen; the next returns to the gallery.
- **Edit** opens a scrollable right panel with live RGB and luminance histograms.

Nine sliders control brightness, contrast, saturation, white point, black point, sharpening, gamma, hue and temperature. Zero is neutral. Hue ranges from -180 to 180 degrees, sharpening from 0 to 100, and other controls from -100 to 100. Gamma and temperature values are relative corrections. Each slider has a reset; **Reset all** clears all adjustments.

Changes are calculated from an unchanged source. The live preview has a maximum edge length of 1024 pixels; saving processes full resolution. Sharpening uses a one-pixel neighborhood, so its visible scale can differ between the reduced preview and full-size output.

**Save / Save as...** appear in a fixed footer at the bottom of the editor panel. They do not move the image or other controls. Save asks for overwrite confirmation and displays the destination path. Save as suggests `original_szerkesztett.extension`, retaining the explicitly requested literal filename tag. Folder and filename are editable; Browse uses the custom picker. Original, PNG and JPEG output can be selected. Existing destinations require confirmation.

The application writes a separate temporary image and replaces the target only after successful encoding and stream commit. PNG preserves alpha; JPEG uses 95% quality. Supported metadata blocks are transferred; JPEG camera/EXIF preservation is tested. Unavailable HEIC encoding can be handled by saving a PNG/JPEG copy while keeping the original.

The saved file becomes the new editing baseline. Unsaved navigation and window closing ask **Save / Discard / Cancel**. Ctrl+S opens save confirmation. Custom fields support cursor keys, Home/End, Backspace/Delete, Ctrl+A and Ctrl+V.

## Selection and batch processing

A checkbox appears in the upper-right of a card on hover and stays visible while selected. With a selection, **All / None** appear in the menu and a batch bar appears below the gallery. Choose a preset to update selected previews. Deselecting restores the original thumbnail. Opening a selected image carries its preset into the individual editor.

**Save all** asks for one shared confirmation and processes the selected originals automatically. **Save all as copies** writes `name_szerkesztett.extension`; existing names receive `_2`, `_3`, etc. Previous copies are never replaced.

Batch processing uses the same full-resolution pixel routines and atomic saves as individual editing. **Stop after this image** or Esc stops between files. A failed image does not stop the others. The completion dialog reports saved/failed counts and the first failed file, then refreshes the folder and clears selection. If HEIC encoding fails in copy mode, a PNG copy is attempted automatically. An unencodable HEIC original is never replaced with a different format.

## How the binary is built

`make_binary.py` contains a custom x64 instruction emitter and PE builder. Generator modules describe explicit registers, instructions, labels and Windows API/COM calls. Python emits machine-code bytes, resolves relative addresses and constructs PE32+ headers, imports and static data.

The emitter performs assembler/linker-like work itself. No **external** C/C++ compiler, assembler or linker is invoked. Python and test libraries are not embedded in the finished executable. Direct imports are Windows USER32, GDI32, KERNEL32 and OLE32; image codecs are accessed through WIC. No .NET, browser engine, native EDIT/BUTTON/tree controls or shell folder dialog is used.

- `src/native_ui.py`, `src/ui_strings_en.py`: UI generation and English strings.
- `src/wic_codegen.py`, `src/metadata_codegen.py`, `src/view_codegen.py`: decoding, metadata and viewport.
- `src/editor_*.py`: editor controls, pixel processing, saving and presets.
- `src/settings_codegen.py`: settings migration and last-folder persistence.
- `src/batch_*.py`: selection, previews and batch processing.
- `tests/`: development-only checks and generated fixtures.
- `binary-map.json`: generated symbols and imports, excluded from Git.

Build from the repository root with Python's standard library:

```powershell
python src/make_binary.py
```

This writes `Gallery.exe` and a Git-ignored `binary-map.json` at the repository root. An optional output name can be provided, for example `python src/make_binary.py Gallery.check.exe`. The emitted executable uses RIP-relative addressing, ASLR and NX. Close a running executable before rebuilding that same file.

## Running the tests

The native test suite requires Windows x64, 64-bit Python, a working Windows WIC decoder/encoder, and Pillow for synthetic test-image generation. Pillow is a test dependency only.

```powershell
python -m pip install -r tests/requirements.txt
python tests/run_tests.py --download-fixtures
```

The first run with `--download-fixtures` downloads the public libheif HEIC example into `tests/.work/input/`. Subsequent runs can use the cached fixture without network access:

```powershell
python tests/run_tests.py
```

To supply a local HEIC fixture instead of downloading one:

```powershell
$env:GALLERY_HEIC_FIXTURE = 'C:\Photos\sample.heic'
python tests/run_tests.py
```

Tests build a separate `Gallery.check.exe`, generate their own synthetic inputs and write outputs under `tests/.work/`. All test binaries, maps, fixture downloads, caches and outputs are Git-ignored. Tests do not modify images outside their generated workspace. `tests/debug_binary.py` is an optional debugger-based startup smoke check that opens the application; it is not part of the default suite.

## Validation and limits

Native pixel tests cover 39 cases: identity, all sliders, extremes, combined settings, alpha and sharpening edges. JSON tests cover Unicode, escaping, disk reload, clamping and MRU ordering. Settings tests cover long Unicode paths, successful/failed folder opens, restoration, missing folders, migration and preset preservation. Encoding/re-decoding is tested for PNG/JPEG/HEIC. Batch tests cover previews, collision-free copies, overwrites, corrupt images, cancellation and HEIC-to-PNG fallback. UI tests include custom controls, confirmations, the fixed save footer and automatic processing of two selected images.

Limits: 16,384 images per folder, 4096 visible tree nodes, 1023-character stored folder paths and 200 megapixels per original. Slow decoding or full-size processing can occupy the UI thread; batch cancellation takes effect between images. EXIF orientation is not separately corrected. The picker lists local and mapped drives. Some encoders may not preserve every metadata block.

Synthetic fixtures and test outputs are generated under `tests/.work/`. The optional HEIC example comes from [the libheif repository](https://github.com/strukturag/libheif/blob/master/examples/example.heic). Neither that downloaded image nor libheif code is committed with this project.
