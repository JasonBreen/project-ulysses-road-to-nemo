# Event-picture fit repair

This source-only repair fits authored artwork to the installed event controls.
It changes **40 country textures and24 news picture bindings**. No GUI layout,
event ID, localization, option, gameplay effect, flag, calendar or campaign
outcome changes. Native testing remains paused.

| Actual consumer | Installed primary texture | Current GUI geometry | Repaired payload |
| --- | --- | --- | --- |
| Country event | 210×176 | `EventWindow/bottom_Window/event_picture`, at5,5; options begin atx215; no scale override | RC14, SNP18 and FATO/South Belka8 textures contain their entire existing master inside210×176, with opaque navy padding |
| News event | 397×153 | `EventWindow_News/top_Window/event_picture`, at59,91; image ends aty244; title begins aty260; no scale override | Anea3 events share one separate original-master derivative; UCW21 events use six separate news-only original briefing compositions |

The reference is installed HOI4 **1.19.4.1**, verified through
`launcher-settings.json#rawVersion`. PE ProductVersion1.0 is not the game-build
identifier. [The capture](../tools/event_picture_fit/contract.json) records
primary GUI/header hashes and dimensions; no installed artwork pixels or full
engine scripts are copied into this package. The existing GUI is protected by
its unchanged normalized hash and actual required-control assertions.

The old640×260 country illustrations extended430 pixels into the options column;
the old450×150 illustrations extended240 pixels into it. The210×176 country
format ends exactly at the column's x215 boundary. In news, the reused176-pixel
country images extended seven pixels beyond the title's start. Separate153-pixel
news images leave the intended16-pixel vertical gap. These are source-relative
geometry findings, not observations of engine rendering.

## Original sources and separate presentation

All existing wide RC/SNP editable masters and all eight original FATO narrative
masters remain byte-for-byte unchanged. The new country DDS use a full-source
Lanczos contain operation; they do not crop people, subjects, or text. Existing
Anea200×160 and older210×176 country pictures, story textures, established flags
and all108 Anea focus DDS remain unchanged.

UCW's six old country pictures are inherited photographic mod material. They
remain intact. Its **new news-only art** uses the repository's original editable
glyph vocabulary: dispatch, accord, operations, institution, command liaison and
campaign assessment. All21 actual news scenes have an explicit mapping and their
actual English title in [ucw_assets.json](../tools/event_picture_fit/ucw_assets.json).
No artwork asserts an unearned winner, extra destruction, new historical incident,
government identity or national flag. The new sources are Python compositions
and six retained794×306 PNG masters, packaged to397×153 without baked captions.
The existing Anea reconstruction scene supplies the separate Anea news image.

As a small, separate review-artifact correction, the Anea focus contact sheet
now uses shipped bitmap glyphs and actual advances rather than FreeType labels.
Its offline cells retain complete titles. The existing bitmap helper was
extracted into a standalone module without generator dependency cycles. Review
PNG checks require identical dimensions and decoded RGBA pixels; **DDS, GFX,
manifests and original master hashes retain exact checks**. No focus texture
pixels or in-game typography changed.

## Preservation and evidence

The scoped audit follows each actual explicit event picture through its sprite,
texture header, frame count and effective GUI scale. It currently covers425
explicit consumers in seven declared files. All32 picture-implicit entries in
that scope are hidden technical replies and are listed separately. The result
is not an all-mod or all-DLC visual-closure claim.

The additional effective-screen ownership audit is retained separately in
[effective-eventwindow.json](evidence/event-picture-fit/effective-eventwindow.json).
The existing decision-screen gate passes, while the **whole event window retains
15 inherited engine fallbacks**: two typewriter font aliases and thirteen default,
leader/operative, agency and frame/clip sprites. That broader ownership gate
fails and is not claimed as closed by this fit repair. It uses inventory-only
DLC context, not observed active-DLC/native rendering. The existing twelve
reference parse failures also remain separately reported. A future defaults/style
packet must address those consumers without changing this captured layout or
pretending to complete the wider portrait and agency families.

The picture-only proof permits exactly `ac_anea.10–12` and the21 enumerated UCW
news IDs to acquire their reviewed new bindings. It restores only those picture
properties and compares the **whole ordered event AST** to the original source.
Negative fixtures reject changed rewards, description keys, country pictures
and unreviewed news bindings. All548 captured original files,108 Anea focus DDS,
and the original LAND1050/AIR1107/NAVAL1110 preservation maps remain exact.
Neither changed event-definition file is in those military maps; no original
capture was refreshed or weakened, and the existing financial exceptions remain
under their original owner.

The [offline gallery](evidence/event-picture-fit/gallery.html) shows actual old
and new image extents and links all40 full-source fits. Previous country-image
pixels are reproduced from the protected masters and checked against their
captured pre-repair RGBA hashes. This review artifact has annotation offsets
outside product geometry and is explicitly not a native screenshot.

Save-game outcomes are unaffected by the authored changes; no setup grant or
event replay is added. Rendering of queued events, actual native clipping,
display configurations and save/reload remain native acceptance work.
Publication, installation synchronization and native testing are separate actions.
