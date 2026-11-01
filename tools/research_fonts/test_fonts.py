"""Actual research font consumers and strict unchanged-control contracts."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/land_program')]
from script import parse,get
from research_fonts.build import SOURCE,inventory,outputs
from research_fonts.policy import BINDINGS
from research_fonts.migration import migrate,restore
from research_fonts.metrics import envelope,text_ink,fits
from render_review import Atlas
spec=importlib.util.spec_from_file_location('research_font_land_ui',ROOT/'tools/land_program/build_ui.py')
land=importlib.util.module_from_spec(spec);spec.loader.exec_module(land)


def nodes(tree):
    for row in tree:
        yield row
        if isinstance(row[2],list):yield from nodes(row[2])


def mod_fonts():
    result={}
    for path in sorted((MOD/'interface').glob('*.gfx')):
        for kind,_,body in nodes(parse(path.read_text(encoding='utf-8-sig'))):
            if kind.lower()=='bitmapfont':
                name=get(body,'name','').strip('"')
                if name.startswith(('ACResearch','ACBriefing')):
                    if name in result:raise ValueError('Conflicting authored font '+name)
                    result[name]=body
    return result


class ResearchFonts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=SOURCE.read_text(encoding='utf-8-sig');cls.original=parse(cls.source)
        cls.current=parse(land.TARGET.read_text(encoding='utf-8-sig'));cls.fonts=mod_fonts()
        cls.primary=json.loads((ROOT/'tools/research_fonts/primary_contract.json').read_text())

    def test_source_and_all_1050_protected_inputs_keep_original_fingerprints(self):
        self.assertEqual('d63f9f14304714a7359280fa2abb57addad229412a54ce05b3db80e0c0ad51f6',hashlib.sha256(self.source.replace('\r\n','\n').encode()).hexdigest())
        manifest=json.loads((ROOT/'tools/land_program/preserved_sources.json').read_text())
        self.assertEqual(1050,len(manifest['protected_sources_sha256']))
        for name,expected in manifest['protected_sources_sha256'].items():
            actual=hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
            repair=manifest.get('reviewed_source_repairs',{}).get(name)
            self.assertEqual(repair['new_normalized_sha256']if repair else expected,actual,name)

    def test_every_actual_font_consumer_resolves_to_exact_authored_font_resources(self):
        old=inventory(self.original);now=inventory(self.current)
        self.assertEqual(301,len(old));self.assertEqual(set(BINDINGS),{r['font']for r in old})
        self.assertEqual(inventory(parse(land.generated()[0])),now)
        self.assertEqual(301,sum(r['font'].startswith('ACResearch')for r in now))
        self.assertEqual({b.name for b in BINDINGS.values()}|{'ACBriefing16','ACBriefing20'},{r['font']for r in now})
        self.assertFalse(set(BINDINGS)&{r['font']for r in now})
        for row in now:
            font=self.fonts[row['font']];base=get(font,'path').strip('"')
            self.assertTrue(base.startswith('gfx/fonts/ACBriefing'))
            self.assertTrue((MOD/(base+'.fnt')).is_file());self.assertTrue((MOD/(base+'.dds')).is_file())
        profile=json.loads((ROOT/'tools/research_fonts/audit_profile.json').read_text())
        self.assertEqual([],profile['enabled_dlc']);self.assertEqual(4,len(profile['provenance']))
        for row in profile['provenance']:
            self.assertEqual(('mod','authored'),(row['provider'],row['classification']))
            self.assertEqual(row['sha256'],hashlib.sha256((MOD/row['path']).read_bytes()).hexdigest())

    def test_font_migration_restores_only_reviewed_fields_and_preserves_key_controls(self):
        restored=land.normalized(self.current)
        self.assertEqual(self.original,restored)
        self.assertEqual(parse(self.source),restore(parse(migrate(self.source)),self.source))
        self.assertEqual(migrate(self.source),migrate(migrate(self.source)))
        original_keys=[(k,v)for k,_,v in nodes(self.original)if k.lower()in('shortcut','clicksound','pdx_tooltip')]
        current_keys=[(k,v)for k,_,v in nodes(restored)if k.lower()in('shortcut','clicksound','pdx_tooltip')]
        self.assertEqual(original_keys,current_keys)
        self.assertIn(('shortcut','"ESCAPE"'),current_keys);self.assertIn(('shortcut','"RETURN"'),current_keys)

    def test_reverted_alias_and_even_an_unreviewed_authored_alias_fail_restoration(self):
        for replacement in('hoi_36header','ACBriefing16'):
            changed=copy.deepcopy(self.current)
            target=next(r for r in nodes(changed)if r[0]=='font'and r[2]=='"ACResearchHeader"')
            target[2]='"'+replacement+'"'
            with self.assertRaisesRegex(ValueError,'font binding reverted or changed'):land.normalized(changed)
        current=land.TARGET.read_text().replace('"ACResearchHeader"','"hoi_36header"',1)
        self.assertTrue(set(BINDINGS)&{r['font']for r in inventory(parse(current))})

    def test_geometry_changes_and_unregistered_added_controls_cannot_hide_in_normalization(self):
        changed=copy.deepcopy(self.current)
        box=next(v for k,_,v in nodes(changed)if isinstance(v,list)and get(v,'name')=='"technology_info_window"')
        point=get(box,'position');point[0][2]=str(int(point[0][2])+1)
        self.assertNotEqual(self.original,land.normalized(changed))
        changed=copy.deepcopy(self.current);changed[0][2].append(['containerWindowType','=',[['name','=','"unregistered_page"']]])
        with self.assertRaisesRegex(ValueError,'Unregistered research GUI structure'):land.normalized(changed)

    def test_comments_and_display_strings_are_not_font_assignments(self):
        source='guiTypes={instantTextBoxType={name="sample" font="hoi_20b" text="font = hoi_20b"}} # font="hoi_20b"\n'
        new=migrate(source)
        self.assertIn('font="ACResearchAction"',new);self.assertIn('text="font = hoi_20b"',new)
        self.assertTrue(new.endswith('# font="hoi_20b"\n'));self.assertEqual(parse(source),restore(parse(new),source))

    def test_actual_inline_state_colors_remain_and_navy_label_value_roles_are_distinct(self):
        self.assertEqual('1.19.4.1',self.primary['version'])
        for old,binding in BINDINGS.items():
            body=self.fonts[binding.name]
            colors={key:[int(k)for k,_,v in value]for key,_,value in get(body,'textcolors',[])}
            self.assertEqual(self.primary['fonts'][old]['text_colors'],colors,old)
            self.assertEqual(binding.color,get(body,'color'))
        self.assertNotEqual(get(self.fonts['ACResearchLabel'],'color'),get(self.fonts['ACResearchValue'],'color'))
        self.assertNotEqual(get(self.fonts['ACResearchHeading'],'color'),get(self.fonts['ACResearchHeader'],'color'))

    def test_actual_atlas_line_heights_fit_all_inherited_declared_rectangles(self):
        atlases={name:Atlas(name)for name in('ACBriefing16','ACBriefing20')}
        for row in inventory(self.original):
            font=atlases[BINDINGS[row['font']].atlas]
            if row['max_height']is not None:self.assertLessEqual(font.height,int(row['max_height']),row['path'])
            text=(row['text']or'').strip('"')
            if re.fullmatch(r'\d{4}',text):
                self.assertLessEqual(font.measure(text),int(row['max_width']),row['path'])
        cases=[('ACBriefing20','INFANTRY SYSTEMS',200,62),('ACBriefing20','Electronic engineering',200,122),
            ('ACBriefing16','Service equipment',160,20),('ACBriefing16','Maximum speed',160,20),
            ('ACBriefing16','+125.5%',100,20),('ACBriefing20','RESEARCH',261,34)]
        for name,text,width,height in cases:
            font=atlases[name];self.assertLessEqual(len(font.wrap(text,width))*font.height,height,(name,text))

    def test_actual_alpha_envelopes_and_accented_names_fit_vertical_budgets(self):
        atlases={name:Atlas(name)for name in('ACBriefing16','ACBriefing20')}
        envelopes={name:envelope(font)for name,font in atlases.items()}
        for row in inventory(self.original):
            shape=envelopes[BINDINGS[row['font']].atlas]
            self.assertEqual(361,shape['glyph_count'])
            self.assertGreaterEqual(shape['ink_top'],0,row['path'])
            if row['max_height']is not None:self.assertLessEqual(shape['ink_bottom'],int(row['max_height']),row['path'])
        # Real alpha from the shipped atlases, rather than FNT lineHeight/base alone.
        self.assertEqual((1,19),(envelopes['ACBriefing16']['ink_top'],envelopes['ACBriefing16']['ink_bottom']))
        self.assertEqual((2,25),(envelopes['ACBriefing20']['ink_top'],envelopes['ACBriefing20']['ink_bottom']))
        for name,text,width,height in [('ACBriefing16','Émile Černý',160,20),
                ('ACBriefing16','ÂÊÎÔÛ ĂŮŴ',160,20),('ACBriefing16','Électronic systems',200,20),
                ('ACBriefing20','ÉLECTRONIC SYSTEMS',300,32)]:
            font=atlases[name];self.assertTrue(fits(text_ink(font,font.wrap(text,width)),width,height),(name,text))
        # A source check must catch the tempting compact-baseline adapter: its
        # declared line height can fit while accented ink is cut off at the top.
        for name,delta in [('ACBriefing16',-3),('ACBriefing20',-4)]:
            shifted=copy.copy(atlases[name]);shifted.rows=copy.deepcopy(shifted.rows)
            for glyph in shifted.rows.values():glyph['yoffset']+=delta
            self.assertLess(envelope(shifted)['ink_top'],0)
            self.assertFalse(fits(text_ink(shifted,['ÂÉÎ']),300,32))
        # Do not silently certify arbitrary runtime names: these authored fonts
        # have known side bearings, whose clipping remains a native coverage item.
        self.assertFalse(fits(text_ink(atlases['ACBriefing16'],['j']),160,20))
        self.assertTrue(envelopes['ACBriefing16']['left_overhangs'])

    def test_alias_and_land_generators_reproduce_without_touching_captured_sources(self):
        for path,data in outputs().items():self.assertEqual(data,path.read_bytes())
        for command in(['tools/research_fonts/build.py','--check'],['tools/land_program/build_ui.py','--check']):
            result=subprocess.run([sys.executable,'-B',*command],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
