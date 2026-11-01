"""Synthetic provider/closure regressions; no private assets or native execution."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/overhaul"))
from audit_consumers import Audit, EffectiveFiles
from capture_dependency_evidence import compact
import capture_dependency_evidence as capture


class EffectiveDependencies(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.engine = Path(self.temp.name) / "engine"
        self.mod = Path(self.temp.name) / "mod"
        self.engine.mkdir(); self.mod.mkdir()

    def put(self, root, relative, data):
        path = root / relative; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode() if isinstance(data,str) else data)
        return path

    def pack(self, key, entries, loose=False):
        relative = "dlc/"+key+"/"+key+".dlc"
        root = "dlc/"+key
        if loose:
            self.put(self.engine,relative,'name="Synthetic pack" path="'+root+'"')
            for name,data in entries.items(): self.put(self.engine/root,name,data)
        else:
            archive = self.engine/root/(key+".zip"); archive.parent.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED) as output:
                for name,data in entries.items(): output.writestr(name,data)
            self.put(self.engine,relative,'name="Synthetic pack" archive="'+root+'/'+key+'.zip"')
        return relative

    @staticmethod
    def profile(*selected, provenance=(), overrides=()):
        return dict(schema=1,name="Synthetic static scenario",enabled_dlc=list(selected),
                    provenance=list(provenance),provider_overrides=list(overrides))

    @staticmethod
    def record(path,data,provider="mod",classification="authored"):
        data=data.encode() if isinstance(data,str) else data
        return dict(path=path,provider=provider,sha256=hashlib.sha256(data).hexdigest(),
                    classification=classification,reason="Synthetic fixture owned by this test",evidence="Synthetic fixture source")

    def window(self):
        self.put(self.mod,"interface/countrydecisionview.gui",'guiTypes={containerWindowType={name="window" iconType={name="panel" spriteType="GFX_panel"}}}')
        self.put(self.mod,"interface/panel.gfx",'spriteTypes={spriteType={name="GFX_panel" texturefile="gfx/panel.dds"}}')
        self.put(self.mod,"gfx/panel.dds",b"synthetic-pixels")
        return self.record("gfx/panel.dds",b"synthetic-pixels")

    def test_installed_archive_is_not_activated_without_an_explicit_profile(self):
        pack=self.pack("pack_one",{"gfx/archive.dds":b"pack-pixels"})
        for profile in (None,self.profile()):
            vfs=EffectiveFiles(self.mod,self.engine,profile)
            self.assertEqual("missing_asset",vfs.resource("gfx/archive.dds")["status"])
            self.assertFalse(vfs.providers.inventory[0]["selected"])
        vfs=EffectiveFiles(self.mod,self.engine,self.profile("engine://"+pack))
        resource=vfs.resource("gfx/archive.dds")
        self.assertEqual("dlc:"+pack,resource["provider"])
        self.assertEqual("engine_asset",resource["status"])
        self.assertIn(".zip!/gfx/archive.dds",resource["source"])
        self.assertEqual("unresolved",resource["classification"])

    def test_directory_pack_and_relative_audio_paths_are_effective_providers(self):
        pack=self.pack("loose_pack",{"sound/clip.asset":'sound={name="clip" file="audiofiles/clip.wav"}',
                                     "sound/audiofiles/clip.wav":b"synthetic-audio"},loose=True)
        audit=Audit(self.mod,self.engine,self.profile(pack))
        sound=audit.resolve("sound","clip")
        self.assertEqual("sound/audiofiles/clip.wav",sound["resources"][0]["path"])
        self.assertEqual("dlc:"+pack,sound["resources"][0]["provider"])
        self.assertEqual("directory",audit.vfs.providers.inventory[0]["payload_kind"])

    def test_integrated_descriptors_need_explicit_hash_pinned_payload_mapping(self):
        local=self.window()
        descriptor="integrated_dlc/embedded/embedded.dlc"
        declaration='name="Synthetic integrated pack" path="dlc/embedded"'
        self.put(self.engine,descriptor,declaration)
        self.put(self.engine,"integrated_dlc/embedded/sound/clip.asset",'sound={name="clip" file="clip.wav"}')
        self.put(self.engine,"integrated_dlc/embedded/sound/clip.wav",b"integrated-sound")
        audit=Audit(self.mod,self.engine,self.profile(descriptor,provenance=[local]))
        self.assertTrue(audit.vfs.providers.errors)
        self.assertEqual("missing_definition",audit.resolve("sound","clip")["status"])
        self.assertEqual("unresolved_provider",audit.vfs.providers.inventory[0]["inspection"])
        mapping=self.record(descriptor,declaration,"dlc:"+descriptor)
        mapping["payload"]="integrated_dlc/embedded"
        approved=self.record("sound/clip.wav",b"integrated-sound","dlc:"+descriptor,"approved_sourced")
        profile=self.profile(descriptor,provenance=[local,approved]);profile["payload_overrides"]=[mapping]
        audit=Audit(self.mod,self.engine,profile)
        self.assertEqual([],audit.vfs.providers.errors)
        row=audit.vfs.providers.inventory[0]
        self.assertEqual("engine://dlc/embedded",row["declared_payload"])
        self.assertEqual("engine://integrated_dlc/embedded",row["payload"])
        self.assertIn("not_native_mount_proof",row["payload_mapping"]["status"])
        self.assertEqual("approved_sourced",audit.resolve("sound","clip")["classification"])
        self.assertTrue(audit.run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])
        stale=copy.deepcopy(profile);stale["payload_overrides"][0]["sha256"]="0"*64
        self.assertTrue(Audit(self.mod,self.engine,stale).vfs.providers.errors)
        unselected=copy.deepcopy(profile);unselected["enabled_dlc"]=[]
        self.assertTrue(Audit(self.mod,self.engine,unselected).vfs.providers.errors)

    def test_capture_profile_maps_empty_declared_integrated_roots_but_keeps_real_payloads(self):
        local=self.window()
        self.put(self.mod,"tools/overhaul/decisions_assets.json",json.dumps({"source_layer":"original procedural artwork",
            "assets":[{"file":local["path"],"sha256":local["sha256"]}]}))
        descriptor="integrated_dlc/embedded/embedded.dlc"
        self.put(self.engine,descriptor,'name="Synthetic integrated pack" path="dlc/embedded"')
        (self.engine/"dlc/embedded").mkdir(parents=True)
        self.put(self.engine,"integrated_dlc/embedded/gfx/asset.dds",b"synthetic")
        with patch.object(capture,"ROOT",self.mod),patch.object(capture,"DEFAULT_MOD",self.mod):
            profiles=capture.profiles(self.engine)
            mappings=profiles["all-installed"]["payload_overrides"]
            self.assertEqual(1,len(mappings))
            self.assertEqual("integrated_dlc/embedded",mappings[0]["payload"])
            self.assertEqual(hashlib.sha256((self.engine/descriptor).read_bytes()).hexdigest(),mappings[0]["sha256"])
            self.put(self.engine,"dlc/embedded/gfx/asset.dds",b"declared-payload")
            self.assertEqual([],capture.profiles(self.engine)["all-installed"]["payload_overrides"])

    def test_archive_gui_template_and_approved_texture_close_the_selected_graph(self):
        local=self.window()
        pack=self.pack("template_pack",{
            "interface/templates.gui":'guiTypes={extendedScrollbarType={name="pack_bar" slider={name="slider" quadTextureSprite="GFX_thumb"}}}',
            "interface/thumb.gfx":'spriteTypes={spriteType={name="GFX_thumb" texturefile="gfx/thumb.dds"}}',
            "gfx/thumb.dds":b"synthetic-thumb"})
        self.put(self.mod,"interface/countrydecisionview.gui",'guiTypes={containerWindowType={name="window" verticalScrollbar="pack_bar" iconType={name="panel" spriteType="GFX_panel"}}}')
        approved=self.record("gfx/thumb.dds",b"synthetic-thumb","dlc:"+pack,"approved_sourced")
        report=Audit(self.mod,self.engine,self.profile(pack,provenance=[local,approved])).run(["countrydecisionview.gui"],True)
        self.assertTrue(report["completed_presentation_gate"]["passed"],report["completed_presentation_gate"]["failures"])
        self.assertTrue(report["gate_covered_screens"]["countrydecisionview.gui"]["templates"])
        self.assertGreater(report["classification_summary"]["approved_sourced"],0)

    def test_differing_fallback_bytes_are_ambiguous_despite_descriptor_order(self):
        self.put(self.engine,"gfx/shared.dds",b"base")
        a=self.pack("a_pack",{"gfx/shared.dds":b"a"})
        b=self.pack("b_pack",{"gfx/shared.dds":b"b"})
        for selected in ((a,b),(b,a)):
            resource=EffectiveFiles(self.mod,self.engine,self.profile(*selected)).resource("gfx/shared.dds")
            self.assertEqual("ambiguous_asset",resource["status"])
            self.assertEqual(3,len(resource["provider_candidates"]))
        chosen=self.record("gfx/shared.dds",b"a","dlc:"+a)
        profile=self.profile(a,b,overrides=[chosen])
        resource=EffectiveFiles(self.mod,self.engine,profile).resource("gfx/shared.dds")
        self.assertEqual("dlc:"+a,resource["provider"])
        self.assertEqual("engine_asset",resource["status"])
        self.put(self.engine,"gfx/shared.dds",b"changed-base")
        changed=copy.deepcopy(profile);changed["provider_overrides"][0]["sha256"]="0"*64
        vfs=EffectiveFiles(self.mod,self.engine,changed)
        self.assertEqual("ambiguous_asset",vfs.resource("gfx/shared.dds")["status"])
        self.assertTrue(vfs.providers.errors)

    def test_ambiguous_fallback_content_cannot_hide_behind_the_explanatory_winner(self):
        local=self.window()
        self.put(self.engine,"common/ideas/content.txt",'# Different potential runtime content\nideas={}')
        pack=self.pack("content_pack",{"common/ideas/content.txt":"ideas={}"})
        report=Audit(self.mod,self.engine,self.profile(pack,provenance=[local])).run(["countrydecisionview.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])
        self.assertIn("provider_ambiguity:common/ideas/content.txt",report["completed_presentation_gate"]["failures"])

    def test_mod_shadow_and_replace_path_apply_to_archive_members(self):
        pack=self.pack("hidden_pack",{"gfx/shared.dds":b"pack", "common/decisions/old.txt":"old={}"})
        self.put(self.mod,"gfx/shared.dds",b"local")
        self.put(self.mod,"descriptor.mod",'replace_path="common/decisions"')
        vfs=EffectiveFiles(self.mod,self.engine,self.profile(pack))
        self.assertEqual("mod",vfs.resource("gfx/shared.dds")["provider"])
        self.assertEqual([],vfs.files("common/decisions"))
        self.assertEqual({},vfs.providers.ambiguities)

    def test_cross_file_sprite_and_template_conflicts_are_not_provider_exemptions(self):
        local=self.window()
        self.put(self.engine,"interface/base.gfx",'spriteTypes={spriteType={name="GFX_same" texturefile="gfx/base.dds"}}')
        self.put(self.engine,"gfx/base.dds",b"base")
        pack=self.pack("conflict_pack",{"interface/extra.gfx":'spriteTypes={spriteType={name="GFX_same" texturefile="gfx/extra.dds"}}',"gfx/extra.dds":b"extra"})
        result=Audit(self.mod,self.engine,self.profile(pack,provenance=[local])).resolve("sprite","GFX_same")
        self.assertEqual("conflicting_definitions",result["status"])
        self.assertEqual("unresolved",result["classification"])
        self.assertTrue(any(".zip!/" in source for source in result["conflicts"]))

    def test_reachable_conflicting_scrollbar_templates_fail_completed_gate(self):
        local=self.window()
        self.put(self.mod,"interface/countrydecisionview.gui",'guiTypes={containerWindowType={name="window" verticalScrollbar="shared_bar"}}')
        self.put(self.engine,"interface/base.gui",'guiTypes={extendedScrollbarType={name="shared_bar" width=10}}')
        pack=self.pack("bar_pack",{"interface/pack.gui":'guiTypes={extendedScrollbarType={name="shared_bar" width=20}}'})
        report=Audit(self.mod,self.engine,self.profile(pack,provenance=[local])).run(["countrydecisionview.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])
        self.assertTrue(any("shared_bar:conflicting_definitions" in failure for failure in report["completed_presentation_gate"]["failures"]))

    def test_identical_definition_text_in_different_relative_media_contexts_is_ambiguous(self):
        definition='sound={name="clip" file="clip.wav"}'
        self.put(self.engine,"sound/base/clip.asset",definition)
        self.put(self.engine,"sound/base/clip.wav",b"base-clip")
        pack=self.pack("relative_pack",{"sound/pack/clip.asset":definition,"sound/pack/clip.wav":b"pack-clip"})
        approved=self.record("sound/pack/clip.wav",b"pack-clip","dlc:"+pack,"approved_sourced")
        result=Audit(self.mod,self.engine,self.profile(pack,provenance=[approved])).resolve("sound","clip")
        self.assertEqual("conflicting_definitions",result["status"])
        self.assertEqual("unresolved",result["classification"])
        self.assertEqual(2,len(result["conflicts"]))

    def test_root_and_source_relative_assets_never_guess_between_different_bytes(self):
        self.put(self.mod,"clip.wav",b"root-outside-audited-roots")
        self.put(self.mod,"sound/clip.wav",b"relative")
        self.put(self.mod,"sound/sound/clip.wav",b"root-conflict")
        vfs=EffectiveFiles(self.mod,self.engine,self.profile())
        resource=vfs.resource("sound/clip.wav","sound/clips.asset")
        self.assertEqual("ambiguous_asset",resource["status"])
        self.assertEqual(2,len(resource["provider_candidates"]))
        self.put(self.mod,"sound/sound/clip.wav",b"relative")
        self.assertEqual("mod_asset",EffectiveFiles(self.mod,self.engine,self.profile()).resource("sound/clip.wav","sound/clips.asset")["status"])

    def test_direct_portrait_and_archive_ui_audio_use_exact_resource_provenance(self):
        local=self.window()
        pack=self.pack("ui_audio",{"sound/ui.asset":'sound={name="click" file="clip.wav"} soundeffect={name="click_effect" sounds={sound=click}}',
            "sound/clip.wav":b"fixture-click", "gfx/portrait.dds":b"fixture-portrait"})
        self.put(self.mod,"interface/countrydecisionview.gui",'guiTypes={containerWindowType={name="window" buttonType={name="button" spriteType="GFX_panel" clickSound="click_effect"}}}')
        self.put(self.mod,"common/characters/example.txt",'characters={office={portraits={civilian={large="gfx/portrait.dds"}}}}')
        approvals=[local,self.record("sound/clip.wav",b"fixture-click","dlc:"+pack,"approved_sourced"),
                   self.record("gfx/portrait.dds",b"fixture-portrait","dlc:"+pack,"approved_sourced")]
        report=Audit(self.mod,self.engine,self.profile(pack,provenance=approvals)).run(["countrydecisionview.gui"],True)
        self.assertTrue(report["completed_presentation_gate"]["passed"],report["completed_presentation_gate"]["failures"])
        self.assertTrue(any(r["consumer_family"]=="portrait" and r["classification"]=="approved_sourced" for r in report["consumers"]))
        self.assertTrue(any(r["consumer_family"]=="audio_consumer" and r["classification"]=="approved_sourced" for r in report["consumers"]))

    def test_archive_portrait_pool_bare_tokens_are_consumers_not_ignored_values(self):
        local=self.window()
        pack=self.pack("portraits_pack",{"portraits/pools.txt":'default={operative={female={"GFX_pool"}}}',
            "interface/pool.gfx":'spriteTypes={spriteType={name="GFX_pool" texturefile="gfx/pool.dds"}}',
            "gfx/pool.dds":b"synthetic-pool"})
        profile=self.profile(pack,provenance=[local])
        report=Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)
        pool=[r for r in report["consumers"] if r["consumer_family"]=="portrait_pool"]
        self.assertEqual(["GFX_pool"],[r["name"] for r in pool])
        self.assertFalse(report["completed_presentation_gate"]["passed"])
        profile["provenance"].append(self.record("gfx/pool.dds",b"synthetic-pool","dlc:"+pack,"approved_sourced"))
        self.assertTrue(Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])

    def test_selected_archive_scripted_gui_bindings_are_part_of_completed_closure(self):
        local=self.window()
        pack=self.pack("scripted_pack",{"common/scripted_guis/binding.txt":'scripted_gui={example={window_name="absent" effects={button_click={}}}}'})
        audit=Audit(self.mod,self.engine,self.profile(pack,provenance=[local]))
        self.assertEqual([],audit.scripted_bindings())
        report=audit.run(["countrydecisionview.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])
        self.assertEqual("missing_binding",report["scripted_gui_bindings"][0]["status"])
        self.assertTrue(any(failure.startswith("binding:") for failure in report["completed_presentation_gate"]["failures"]))

    def model_pack(self):
        return self.pack("model_pack",{
            "gfx/entities/units.asset":'entity={name="base" pdxmesh="body" attach={name="detail" locator="ornament"} state={name="idle" animation="idle" event={sound={soundeffect="clip_effect"}}}} entity={name="ornament" pdxmesh="body"}',
            "gfx/entities/meshes.gfx":'objectTypes={pdxmesh={name="body" file="gfx/models/body.mesh" animation={id="idle" type="idle_clip"} meshsettings={name="skin" texture_diffuse="gfx/skin.dds" texture_normal="gfx/normal.dds" texture_specular="gfx/specular.dds"}}}',
            "gfx/models/clips.asset":'animation={name="idle_clip" file="idle.anim"}',
            "gfx/models/idle.anim":b"synthetic-animation", "gfx/models/body.mesh":b"pdxbin-synthetic-opaque-mesh",
            "gfx/skin.dds":b"skin", "gfx/normal.dds":b"normal", "gfx/specular.dds":b"specular",
            "sound/clips.asset":'sound={name="clip" file="audiofiles/clip.wav"} soundeffect={name="clip_effect" sounds={sound=clip}}',
            "sound/audiofiles/clip.wav":b"synthetic-audio"})

    def test_archive_clone_attachment_material_animation_and_audio_edges_are_followed(self):
        pack=self.model_pack()
        self.put(self.mod,"gfx/entities/local.asset",'entity={name="local" clone="base"}')
        audit=Audit(self.mod,self.engine,self.profile(pack))
        result=audit.resolve("entity","local")
        base=result["dependencies"][0]
        self.assertIn("ornament",[r["name"] for r in base["dependencies"]])
        self.assertIn("clip_effect",[r["name"] for r in base["dependencies"]])
        mesh=next(r for r in base["dependencies"] if r["family"]=="mesh")
        self.assertEqual(["idle"],mesh["declared_animation_ids"])
        self.assertEqual(3,len(mesh["declared_materials"][0]["textures"]))
        clip=mesh["dependencies"][0]
        self.assertEqual("gfx/models/idle.anim",clip["resources"][0]["path"])
        effect=next(r for r in base["dependencies"] if r["family"]=="audio")
        self.assertEqual("sound/audiofiles/clip.wav",effect["dependencies"][0]["resources"][0]["path"])
        self.assertEqual("unresolved",result["classification"])
        self.assertIn("binary_material_dependencies",mesh["resources"][0])

    def test_missing_state_animation_and_binary_materials_cannot_be_certified_by_file_presence(self):
        pack=self.model_pack()
        self.put(self.mod,"gfx/entities/extra.asset",'entity={name="local" clone="base" state={name="special" animation="not_declared"}}')
        result=Audit(self.mod,self.engine,self.profile(pack)).resolve("entity","local")
        self.assertTrue(any(d["family"]=="animation_binding" and d["name"]=="not_declared" for d in result["dependencies"]))
        self.assertEqual("unresolved",result["classification"])
        # Pin every resource in an isolated mesh: unknown embedded bindings must
        # remain unresolved even when the physical file's provenance is known.
        self.put(self.mod,"gfx/models/isolated.gfx",'objectTypes={pdxmesh={name="isolated" file="gfx/models/isolated.mesh"}}')
        self.put(self.mod,"gfx/models/isolated.mesh",b"synthetic-opaque-mesh")
        approved=self.profile(provenance=[self.record("gfx/models/isolated.mesh",b"synthetic-opaque-mesh")])
        mesh=Audit(self.mod,self.engine,approved).resolve("mesh","isolated")
        self.assertEqual("authored",mesh["resources"][0]["classification"])
        self.assertEqual("unresolved",mesh["classification"])

    def test_attachment_animation_ids_cannot_satisfy_parent_state_bindings(self):
        self.put(self.mod,"gfx/models/model.gfx",'objectTypes={pdxmesh={name="parent_mesh" animation={id="idle" type="clip"}} pdxmesh={name="child_mesh" animation={id="run" type="clip"}}}')
        self.put(self.mod,"gfx/models/clip.asset",'animation={name="clip" file="clip.anim"}')
        self.put(self.mod,"gfx/models/clip.anim",b"synthetic-animation")
        self.put(self.mod,"gfx/entities/model.asset",'entity={name="parent" pdxmesh="parent_mesh" attach={name="attachment" locator="child"} state={name="run" animation="run"}} entity={name="child" pdxmesh="child_mesh"}')
        result=Audit(self.mod,self.engine,self.profile()).resolve("entity","parent")
        self.assertEqual(["idle"],result["declared_animation_ids"])
        self.assertTrue(any(d["family"]=="animation_binding" and d["name"]=="run" for d in result["dependencies"]))
        self.put(self.mod,"gfx/entities/override.asset",'entity={name="override" clone="parent" pdxmesh="child_mesh"}')
        result=Audit(self.mod,self.engine,self.profile()).resolve("entity","override")
        self.assertTrue(any(d["family"]=="animation_binding" and d["name"]=="clone_mesh_override" for d in result["dependencies"]))

    def test_selected_music_playlist_requires_its_named_archive_song(self):
        local=self.window()
        pack=self.pack("music_pack",{"music/playlist.txt":'music={song="track" chance={factor=0}}',
            "music/tracks.asset":'music={name="track" file="track.ogg"}',"music/track.ogg":b"synthetic-music"})
        approved=self.record("music/track.ogg",b"synthetic-music","dlc:"+pack,"approved_sourced")
        report=Audit(self.mod,self.engine,self.profile(pack,provenance=[local,approved])).run(["countrydecisionview.gui"],True)
        songs=[row for row in report["consumers"] if row["consumer_family"]=="music_playlist"]
        self.assertEqual(["track"],[r["name"] for r in songs])
        self.assertTrue(report["completed_presentation_gate"]["passed"])
        self.put(self.mod,"music/missing.txt",'music={song="unbound"}')
        report=Audit(self.mod,self.engine,self.profile(pack,provenance=[local,approved])).run(["countrydecisionview.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])
        self.assertTrue(any("unbound" in failure for failure in report["completed_presentation_gate"]["failures"]))

    def test_music_cannot_use_an_approved_image_or_program_as_audio(self):
        local = self.window()
        self.put(self.mod, "music/playlist.txt", 'music={song="track"}')
        for path in ("gfx/fx/not_audio.shader", "gfx/not_audio.dds"):
            with self.subTest(path=path):
                payload = b"synthetic-non-audio"
                self.put(self.mod, path, payload)
                self.put(self.mod, "music/track.asset", 'music={name="track" file="' + path + '"}')
                for classification in ("authored", "approved_sourced"):
                    profile = self.profile(provenance=[local, self.record(path, payload, classification=classification)])
                    audit = Audit(self.mod, self.engine, profile)
                    track = audit.resolve("music", "track")
                    self.assertEqual("unresolved", track["classification"])
                    self.assertEqual("unsupported_resource_kind", track["resources"][0]["status"])
                    self.assertFalse(audit.run(["countrydecisionview.gui"], True)["completed_presentation_gate"]["passed"])

    def test_duplicate_archive_members_fail_before_approval_or_size_checks(self):
        local = self.window()
        first, last = b"x" * (8 * 1024 * 1024 + 1), b"last"
        for names in (("gfx/shared.dds", "gfx/shared.dds"), ("gfx/SHARED.dds", "gfx/shared.dds"), ("gfx\\shared.dds", "gfx/shared.dds")):
            with self.subTest(names=names):
                pack = self.pack("duplicate_pack", {names[0]: first})
                archive_path = self.engine / "dlc/duplicate_pack/duplicate_pack.zip"
                import warnings
                with zipfile.ZipFile(archive_path, "a") as archive, warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    archive.writestr(names[1], last)
                profile = self.profile(pack, provenance=[local, self.record("gfx/shared.dds", last, "dlc:" + pack, "approved_sourced")])
                audit = Audit(self.mod, self.engine, profile)
                self.assertEqual("missing_asset", audit.vfs.resource("gfx/shared.dds")["status"])
                provider = next(row for row in audit.vfs.providers.inventory if row["selected"])
                self.assertEqual(["gfx/shared.dds"], provider["duplicate_members"])
                self.assertEqual("unresolved_provider", provider["inspection"])
                self.assertFalse(audit.run(["countrydecisionview.gui"], True)["completed_presentation_gate"]["passed"])

    def test_scripted_gui_parse_errors_enter_the_completed_gate(self):
        local = self.window()
        for root in (self.mod, self.engine):
            with self.subTest(provider=root.name):
                path = self.put(root, "common/scripted_guis/broken.txt", "scripted_gui={ broken = {")
                report = Audit(self.mod, self.engine, self.profile(provenance=[local])).run(["countrydecisionview.gui"], True)
                self.assertTrue(any(row["source"] == "common/scripted_guis/broken.txt" for row in report["parse_failures"]))
                self.assertIn("parse:common/scripted_guis/broken.txt", report["completed_presentation_gate"]["failures"])
                self.assertFalse(report["completed_presentation_gate"]["passed"])
                path.unlink()

    def test_completed_gate_requires_profile_and_exact_hash_provenance(self):
        local=self.window()
        self.assertFalse(Audit(self.mod,self.engine).run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])
        profile=self.profile(provenance=[local])
        self.assertTrue(Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])
        self.put(self.mod,"gfx/panel.dds",b"changed")
        self.assertFalse(Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])

    def test_engine_art_cannot_be_relabelled_authored_and_shader_is_not_a_pixel_exemption(self):
        self.put(self.engine,"gfx/icon.dds",b"engine-pixels")
        self.put(self.engine,"gfx/fx/basic.shader","synthetic shader program")
        fake=self.record("gfx/icon.dds",b"engine-pixels","engine","authored")
        vfs=EffectiveFiles(self.mod,self.engine,self.profile(provenance=[fake]))
        self.assertEqual("unresolved",vfs.resource("gfx/icon.dds")["classification"])
        self.assertEqual("technical",vfs.resource("gfx/fx/basic.lua",usage="program")["classification"])
        self.assertEqual("engine_service",vfs.resource("gfx/fx/basic.lua",usage="program")["status"])
        self.assertEqual("unresolved",vfs.resource("gfx/fx/basic.lua")["classification"])
        approved=self.record("gfx/icon.dds",b"engine-pixels","engine","approved_sourced")
        self.assertEqual("approved_sourced",EffectiveFiles(self.mod,self.engine,self.profile(provenance=[approved])).resource("gfx/icon.dds")["classification"])

    def test_program_exception_cannot_close_a_texture_or_audio_binding(self):
        self.window()
        self.put(self.engine,"gfx/fx/basic.shader","synthetic shader program")
        self.put(self.mod,"interface/panel.gfx",'spriteTypes={spriteType={name="GFX_panel" texturefile="gfx/fx/basic.lua"}}')
        audit=Audit(self.mod,self.engine,self.profile())
        row=audit.resolve("sprite","GFX_panel")
        self.assertEqual("unresolved",row["classification"])
        self.assertEqual("unsupported_resource_kind",row["resources"][0]["status"])
        self.assertFalse(audit.run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])
        self.put(self.mod,"sound/cue.asset",'sound={name="cue" file="gfx/fx/basic.shader"}')
        self.assertEqual("unresolved",Audit(self.mod,self.engine,self.profile()).resolve("sound","cue")["classification"])

    def test_program_field_keeps_primary_shader_alias_beside_an_authored_texture(self):
        local=self.window()
        self.put(self.engine,"gfx/fx/basic.shader","synthetic shader program")
        self.put(self.mod,"interface/panel.gfx",'spriteTypes={spriteType={name="GFX_panel" texturefile="gfx/panel.dds" effectFile="gfx/fx/basic.lua"}}')
        audit=Audit(self.mod,self.engine,self.profile(provenance=[local]))
        row=audit.resolve("sprite","GFX_panel")
        self.assertEqual("authored",row["classification"])
        program=next(r for r in row["resources"] if r["binding_usage"]=="program")
        self.assertEqual("engine_service",program["status"])
        self.assertEqual("gfx/fx/basic.lua",program["legacy_alias"])
        self.assertTrue(audit.run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])

    def test_unreachable_decisions_have_a_recorded_static_reason(self):
        self.window()
        self.put(self.mod,"common/decisions/retired.txt",'category={retired={allowed={always=no} icon=missing} active={icon=also_missing}}')
        report=Audit(self.mod,self.engine,self.profile()).run(["countrydecisionview.gui"],True)
        retired=report["statically_retired_consumers"]
        self.assertTrue(any(r["owner"]=="retired" and r["classification"]=="unreachable" and r["reason"] for r in retired))
        self.assertFalse(any(r["owner"]=="retired" for r in report["consumers"]))
        self.assertTrue(any(r["owner"]=="active" and r["classification"]=="unresolved" for r in report["consumers"]))

    def test_unsafe_or_missing_providers_fail_without_extracting_any_member(self):
        local=self.window()
        pack=self.pack("unsafe_pack",{"../escape.txt":b"never extracted"})
        profile=self.profile(pack,"dlc/absent/absent.dlc",provenance=[local])
        audit=Audit(self.mod,self.engine,profile)
        self.assertFalse((self.engine/"escape.txt").exists())
        self.assertTrue(audit.vfs.providers.errors)
        unsafe=next(row for row in audit.vfs.providers.inventory if row["selected"])
        self.assertEqual(["../escape.txt"],unsafe["unsafe_members"])
        self.assertEqual("unresolved_provider",unsafe["inspection"])
        report=audit.run(["countrydecisionview.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])

    def test_oversized_archive_definition_is_unresolved_without_decompressing_it(self):
        self.window()
        pack=self.pack("large_pack",{"interface/large.gfx":"#"*(8*1024*1024+1)})
        report=Audit(self.mod,self.engine,self.profile(pack)).run(["countrydecisionview.gui"],True)
        self.assertTrue(any("bounded text-reader" in r["error"] for r in report["parse_failures"]))
        self.assertFalse(report["completed_presentation_gate"]["passed"])

    def test_approval_and_override_wildcards_or_unexplained_records_are_rejected(self):
        local=self.window()
        for field,value in (("path","gfx/*"),("reason"," "),("sha256","bad")):
            record=copy.deepcopy(local);record[field]=value
            with self.assertRaises(ValueError): EffectiveFiles(self.mod,self.engine,self.profile(provenance=[record]))

    def test_cli_completed_gate_exit_status_and_missing_requested_screen(self):
        local=self.window();profile=Path(self.temp.name)/"profile.json"
        profile.write_text(json.dumps(self.profile(provenance=[local])))
        command=[sys.executable,"-B",str(ROOT/"tools/overhaul/audit_consumers.py"),str(self.engine),"--mod-root",str(self.mod),"--profile",str(profile),"--gate-presentation"]
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
        self.assertTrue(json.loads(result.stdout)["completed_presentation_gate"]["passed"])
        self.put(self.mod,"gfx/panel.dds",b"changed")
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(1,result.returncode,result.stdout+result.stderr)
        report=Audit(self.mod,self.engine,self.profile()).run(["absent.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])

    def test_bounded_evidence_keeps_failure_status_totals_and_complete_list_hash(self):
        self.window()
        report=Audit(self.mod,self.engine,self.profile()).run(["countrydecisionview.gui"],True)
        failures=report["completed_presentation_gate"]["failures"][:]
        summary=compact(report)
        gate=summary["completed_presentation_gate"]
        self.assertFalse(gate["passed"])
        self.assertEqual(len(failures),gate["failure_count"])
        self.assertEqual(hashlib.sha256(json.dumps(failures,sort_keys=True).encode()).hexdigest(),gate["complete_failure_list_sha256"])
        self.assertEqual({"authored","approved_sourced","technical","unreachable","unresolved"},set(summary["classification_summary"]))
        self.assertNotIn("consumers",summary)

    def test_animation_overlays_unknown_literal_media_and_map_objects_are_not_hidden(self):
        local=self.window()
        self.put(self.mod,"interface/panel.gfx",'spriteTypes={spriteType={name="GFX_panel" texturefile="gfx/panel.dds" animation={animationmaskfile="gfx/mask.dds" animationtexturefile="gfx/overlay.dds"}}}')
        self.put(self.mod,"gfx/mask.dds",b"mask");self.put(self.mod,"gfx/overlay.dds",b"overlay")
        self.put(self.mod,"interface/arrows.gfx",'objectTypes={arrowType={name="map_arrow" texture="gfx/arrow.dds" effect="gfx/arrow.shader" future_texture_binding="gfx/future.dds"}}')
        self.put(self.mod,"gfx/arrow.dds",b"arrow");self.put(self.mod,"gfx/arrow.shader",b"synthetic shader");self.put(self.mod,"gfx/future.dds",b"future")
        profile=self.profile(provenance=[local])
        audit=Audit(self.mod,self.engine,profile)
        sprite=audit.resolve("sprite","GFX_panel")
        self.assertEqual({"gfx/panel.dds","gfx/mask.dds","gfx/overlay.dds"},{r["path"] for r in sprite["resources"]})
        report=audit.run(["countrydecisionview.gui"],True)
        self.assertFalse(report["completed_presentation_gate"]["passed"])
        arrow=next(r for r in report["consumers"] if r["family"]=="presentation_object")
        self.assertEqual({"gfx/arrow.dds","gfx/arrow.shader","gfx/future.dds"},{r["path"] for r in arrow["resources"]})
        for path,data in (("gfx/mask.dds",b"mask"),("gfx/overlay.dds",b"overlay"),("gfx/arrow.dds",b"arrow"),("gfx/future.dds",b"future")):
            profile["provenance"].append(self.record(path,data))
        self.assertTrue(Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])

    def test_literal_gui_textures_require_resolution_and_provenance(self):
        local=self.window()
        self.put(self.mod,"interface/countrydecisionview.gui",'guiTypes={containerWindowType={name="window" texturefile="gfx/panel.dds"}}')
        profile=self.profile(provenance=[local])
        report=Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)
        self.assertTrue(report["completed_presentation_gate"]["passed"])
        self.assertTrue(any(r["consumer_family"]=="screen_literal" for r in report["consumers"]))
        self.put(self.mod,"gfx/panel.dds",b"changed")
        self.assertFalse(Audit(self.mod,self.engine,profile).run(["countrydecisionview.gui"],True)["completed_presentation_gate"]["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
