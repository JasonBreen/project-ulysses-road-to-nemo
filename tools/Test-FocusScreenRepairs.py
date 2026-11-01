"""October31 screenshot regressions using actual GUI geometry and font advances.

Offline projections and pixel contracts are not native rendering acceptance.
"""
import json
import re
import subprocess
import sys
import unittest
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/2985041246'
SRC=ROOT/'tools/usea_expansion'
sys.path.insert(0,str(SRC))
from script import parse,get,walk


def read(relative):return parse((MOD/relative).read_text(encoding='utf-8-sig'))
def named(tree,name):return next(node for _,node in walk(tree) if get(node,'name','').strip('"')==name)
def point(node):
    position=get(node,'position')
    return int(get(position,'x')),int(get(position,'y'))


def font_metrics():
    text=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text()
    height=int(re.search(r'common lineHeight=(\d+)',text)[1])
    advances={int(match[0]):int(match[1]) for match in re.findall(r'char id=(\d+).*?xadvance=(\d+)',text)}
    return height,advances


def wrapped_lines(text,width,advances):
    text=re.sub(r'§.','',text)
    result=[]
    for paragraph in text.replace('\\n','\n').splitlines():
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if line and sum(advances.get(ord(c),8) for c in candidate)>width:
                result.append(line);line=word
            else:line=candidate
        result.append(line)
    return result


def title_variants(text,localization,scripted):
    match=re.search(r'\[(?:Root\.)?(\w+)\]',text)
    if not match:return [text]
    name=match[1]
    if name not in scripted:raise AssertionError('Unresolved dynamic focus title: '+name)
    result=[]
    for key in scripted[name]:
        if key not in localization:raise AssertionError('Missing dynamic title localization: '+key)
        value=text[:match.start()]+localization[key]+text[match.end():]
        result.extend(title_variants(value,localization,scripted))
    return result


def resolved_tree_positions():
    """Resolve explicit imports, their shared descendants and relative anchors.

    Descendant closure is deliberately conservative: it also checks shared
    children inherited from imported roots, even if a particular branch is not
    currently available. Availability does not hide a focus caption.
    """
    shared={};trees=[];children=defaultdict(set)
    for path in sorted((MOD/'common/national_focus').glob('*.txt')):
        for kind,_,node in parse(path.read_text(encoding='utf-8-sig')):
            if kind=='shared_focus' and isinstance(node,list):shared[get(node,'id')]=node
            if kind=='focus_tree':trees.append(node)
    for ident,node in shared.items():
        for kind,_,child in node:
            if kind=='prerequisite':
                for key,_,value in child:
                    if key=='focus':children[value].add(ident)
    result={}
    for tree in trees:
        ident=get(tree,'id')
        nodes={get(node,'id'):node for kind,_,node in tree if kind=='focus' and isinstance(node,list)}
        pending=[node for kind,_,node in tree if kind=='shared_focus' and isinstance(node,str)]
        while pending:
            ref=pending.pop()
            if ref in nodes:continue
            if ref not in shared:raise AssertionError('Missing shared focus import: '+ident+':'+ref)
            nodes[ref]=shared[ref]
            pending.extend(children[ref])
        positions={}
        def resolve(ref,stack=()):
            if ref in positions:return positions[ref]
            if ref in stack:raise AssertionError('Cyclic relative focus position: '+str(stack+(ref,)))
            node=nodes.get(ref,shared.get(ref))
            if node is None:raise AssertionError('Missing relative focus anchor: '+ident+':'+ref)
            x=float(get(node,'x','0'));y=float(get(node,'y','0'))
            parent=get(node,'relative_position_id')
            if parent:
                px,py=resolve(parent,stack+(ref,));x+=px;y+=py
            positions[ref]=(x,y)
            return x,y
        result[ident]={ref:resolve(ref) for ref in nodes}
    return result


class FocusScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gui=read('interface/nationalfocusview.gui')
        cls.specs=json.loads((SRC/'ui_assets.json').read_text())
        cls.assets={row['file']:row for row in json.loads((SRC/'assets.json').read_text())}

    def test_three_line_captions_fit_each_runtime_state_background(self):
        item=named(self.gui,'national_focus_item')
        caption=named([['item','=',item]],'name')
        background=named([['item','=',item]],'bg')
        line_height,_=font_metrics()
        self.assertEqual(54,int(get(caption,'maxHeight')))
        self.assertEqual(3*line_height,int(get(caption,'maxHeight')))
        self.assertEqual((96,160),point(named(self.gui,'focus_spacing')))
        for spec in self.specs:
            if not re.match(r'GFX_focus_(unavailable|can_start|current|completed)(?:_|$)',spec['name']):continue
            with self.subTest(state=spec['name']):
                with Image.open(MOD/'gfx/interface/ac_expansion/ui'/(spec['name']+'.dds')) as image:
                    self.assertEqual(64,image.height)
                    x,y=point(caption);bx,by=point(background)
                    self.assertGreaterEqual(x,bx);self.assertGreaterEqual(y,by)
                    self.assertLessEqual(x+int(get(caption,'maxWidth')),bx+image.width//spec['frames'])
                    self.assertLessEqual(y+int(get(caption,'maxHeight')),by+image.height)

    def test_authored_localized_focus_titles_fit_using_shipped_font_advances(self):
        line_height,advances=font_metrics()
        localization={}
        files=sorted((MOD/'localisation/english').glob('*.yml'))+sorted((MOD/'localisation/english/replace').glob('*.yml'))
        for path in files:
            for match in re.finditer(r'^\s*([\w.]+):\d*\s+"(.*)"',path.read_text(encoding='utf-8-sig'),re.M):
                localization[match[1]]=match[2]
        caption=named([['item','=',named(self.gui,'national_focus_item')]],'name')
        width=int(get(caption,'maxWidth'));height=int(get(caption,'maxHeight'))
        scripted={}
        for path in (MOD/'common/scripted_localisation').glob('*.txt'):
            for kind,_,node in parse(path.read_text(encoding='utf-8-sig')):
                if kind=='defined_text':
                    scripted[get(node,'name').strip('"')]=[get(body,'localization_key').strip('"')
                         for key,_,body in node if key=='text' and get(body,'localization_key')]
        checked=set()
        for path in (MOD/'common/national_focus').glob('*.txt'):
            for kind,node in walk(parse(path.read_text(encoding='utf-8-sig'))):
                if kind not in ('focus','shared_focus') or not get(node,'id'):continue
                ident=get(node,'id')
                if ident not in localization:continue # Missing localization is owned by the full reference gate.
                checked.add(ident)
                for title in title_variants(localization[ident],localization,scripted):
                    with self.subTest(focus=ident,title=title):
                        lines=wrapped_lines(title,width,advances)
                        self.assertLessEqual(len(lines)*line_height,height)
                        self.assertTrue(all(sum(advances.get(ord(c),8) for c in line)<=width for line in lines))
        # This covers877 current authored localized IDs. Other inherited or
        # unresolved IDs belong to the separate consumer/reference audit.
        self.assertGreaterEqual(len(checked),850)
        self.assertEqual('North Gebadia Factories',localization['GEB_north_gebadia_factories'])
        self.assertGreater(len(localization['GEB_north_gebadia_factories_desc']),100)

    def test_normal_icon_and_caption_footprints_fit_the_new_row_pitch(self):
        item=named(self.gui,'national_focus_item')
        symbol=named([['item','=',item]],'symbol')
        background=named([['item','=',item]],'bg')
        self.assertEqual('yes',get(symbol,'centerposition'))
        self.assertEqual('CENTER',get(symbol,'Orientation'))
        height=int(get(get(item,'size'),'height'))
        #Resolve the centred96px icon in local control coordinates.
        icon_top=height//2+point(symbol)[1]-48
        icon_bottom=icon_top+96
        frame_top=point(background)[1];frame_bottom=frame_top+64
        self.assertEqual((-56,40),(icon_top,icon_bottom))
        self.assertLessEqual(icon_bottom,frame_top)
        self.assertLessEqual(frame_bottom-icon_top,point(named(self.gui,'focus_spacing'))[1])
        grid=named([['window','=',named(self.gui,'grid_window')]],'grid')
        self.assertGreaterEqual(point(grid)[1]+icon_top,0)

    def test_resolved_caption_rectangles_never_overlap_between_nodes(self):
        caption=named([['item','=',named(self.gui,'national_focus_item')]],'name')
        width=int(get(caption,'maxWidth'));height=int(get(caption,'maxHeight'))
        self.assertEqual(147,width)
        pitch_x,pitch_y=point(named(self.gui,'focus_spacing'))
        actual=set();trees=resolved_tree_positions()
        for tree,positions in trees.items():
            for a,b in combinations(sorted(positions),2):
                ax,ay=positions[a];bx,by=positions[b]
                if abs(ax-bx)*pitch_x<width and abs(ay-by)*pitch_y<height:
                    actual.add((tree,a,b,positions[a],positions[b]))
        self.assertFalse(actual,'Resolved focus caption overlaps: '+repr(actual))
        # Twenty-five is the repaired baseline, not a ceiling on new campaigns.
        # Every resolved tree above still participates in the geometry checks;
        # each expansion owner separately asserts its exact definition budget.
        self.assertGreaterEqual(len(trees),25)
        self.assertGreaterEqual(sum(len(nodes) for nodes in trees.values()),940)
        for tree in ('ac_exp_fcu_opening','ac_ucw_fcu_tree'):
            self.assertIn(tree,trees)
            self.assertFalse([pair for pair in actual if pair[0]==tree])
        self.assertEqual((10.,2.),trees['belka_start']['ac_belkan_industrial_mobilization'])
        for suffix,y in (('settlement',3.),('legacy',4.)):
            self.assertEqual((4.,y),trees['ac_belkan_postwar']['ac_postwar_unclassified_'+suffix])
        for suffix in ('brief','costs','demobilize','loyalty','commitments','legacy'):
            self.assertEqual(70.,trees['sap_focus']['SAP_pwi_'+suffix][0])

    def test_exclusion_marker_and_line_bounds_are_above_the_caption(self):
        caption=named([['item','=',named(self.gui,'national_focus_item')]],'name')
        top=point(caption)[1]
        exclusion=named(self.gui,'national_focus_exclusive_item')
        for offset in ('exclusive_offset','exclusive_offset_left'):
            base_y=point(exclusion)[1]+point(named(self.gui,offset))[1]
            for _,control in walk([['exclusion','=',exclusion]]):
                sprite=get(control,'spriteType')
                if not sprite:continue
                spec=next(row for row in self.specs if row['name']==sprite.strip('"'))
                bottom=base_y+point(control)[1]+spec['height']
                self.assertLessEqual(bottom,top,(offset,get(control,'name')))

    def test_directional_tiles_have_aligned_ports_and_straight_seams(self):
        count=0
        for spec in self.specs:
            if not spec['name'].startswith('GFX_focus_link') or 'exclusive' in spec['name']:continue
            count+=1
            suffix=spec['name'].removeprefix('GFX_focus_link').strip('_')
            directions=set(suffix.split('_')) if suffix else {'up','down'}
            with Image.open(MOD/'gfx/interface/ac_expansion/ui'/(spec['name']+'.dds')) as image:
                width=image.width//spec['frames'];height=image.height
                xband={width//2-1,width//2};yband={height//2-1,height//2}
                reference=None
                for frame in range(spec['frames']):
                    alpha=image.crop((frame*width,0,(frame+1)*width,height)).getchannel('A')
                    mask=alpha.tobytes()
                    if reference is None:reference=mask
                    self.assertEqual(reference,mask, spec['name'])
                    ports={'left':{y for y in range(height) if alpha.getpixel((0,y))},
                           'right':{y for y in range(height) if alpha.getpixel((width-1,y))},
                           'up':{x for x in range(width) if alpha.getpixel((x,0))},
                           'down':{x for x in range(width) if alpha.getpixel((x,height-1))}}
                    for port,pixels in ports.items():
                        self.assertEqual((yband if port in ('left','right') else xband) if port in directions else set(),pixels,(spec['name'],frame,port))
                    if directions=={'left','right'}:
                        for x in range(width):self.assertEqual(yband,{y for y in range(height) if alpha.getpixel((x,y))})
                    if directions=={'up','down'}:
                        for y in range(height):self.assertEqual(xband,{x for x in range(width) if alpha.getpixel((x,y))})
        self.assertGreaterEqual(count,12)

    def test_continuous_icons_and_captions_fit_scrollable_rows(self):
        item=named(self.gui,'continuous_national_focus_item')
        caption=named([['item','=',item]],'name')
        symbol=named([['item','=',item]],'symbol')
        background=named([['item','=',item]],'bg')
        self.assertEqual((40,0),point(symbol))
        self.assertGreaterEqual(point(background)[1],point(symbol)[1]+96)
        self.assertGreaterEqual(point(caption)[1],point(background)[1])
        self.assertLessEqual(point(caption)[1]+int(get(caption,'maxHeight')),point(background)[1]+64)
        window=named(self.gui,'continuous_focus_window')
        entries=named([['window','=',window]],'entries')
        grid=named([['entries','=',entries]],'list')
        self.assertEqual('yes',get(entries,'clipping'))
        self.assertEqual('"ac_exp_right_vertical_slider"',get(entries,'verticalScrollbar'))
        self.assertGreaterEqual(int(get(get(grid,'slotsize'),'height')),point(background)[1]+64)
        self.assertLessEqual(point(entries)[1]+int(get(get(entries,'size'),'height')),int(get(get(window,'size'),'height')))
        description=named([['window','=',window]],'continuous_focus_desc')
        self.assertLessEqual(point(description)[1]+int(get(description,'maxHeight')),point(entries)[1])

    def test_opening_continuous_panels_clear_tree_and_fit_primary_view(self):
        pitch_x,pitch_y=point(named(self.gui,'focus_spacing'))
        window=named(self.gui,'continuous_focus_window')
        panel_w=int(get(get(window,'size'),'width'));panel_h=int(get(get(window,'size'),'height'))
        for tag in ('ERU','FCU'):
            tree=get(read('common/national_focus/'+tag+'_opening.txt'),'focus_tree')
            position=get(tree,'continuous_focus_position');px=int(get(position,'x'));py=int(get(position,'y'))
            focuses=[node for kind,_,node in tree if kind=='focus']
            imports=[value for kind,_,value in tree if kind=='shared_focus' and isinstance(value,str)]
            for path in (MOD/'common/national_focus').glob('*.txt'):
                focuses.extend(node for kind,_,node in parse(path.read_text(encoding='utf-8-sig'))
                               if kind=='shared_focus' and get(node,'id') in imports)
            right=max(int(get(node,'x'))*pitch_x+169 for node in focuses)
            self.assertGreater(px,right+32)
            self.assertLessEqual(50+px+panel_w,3440)
            self.assertLessEqual(78+47+66+py+panel_h,1440)
            self.assertLess(py,100)
        canvas=named(self.gui,'tree')
        self.assertIn('horizontalScrollbar',[key for key,_,_ in canvas])
        self.assertIn('verticalScrollbar',[key for key,_,_ in canvas])
        self.assertEqual({'left','middle'},{key for key,_,_ in get(canvas,'drag_scroll')})

    def test_sources_reproduce_without_rewriting_other_surfaces(self):
        for args in (['tools/usea_expansion/build_ui.py','--check'],
                     ['tools/usea_expansion/build_art.py','--focus-ui-only','--check'],
                     ['tools/usea_expansion/build_content.py','--check'],
                     ['tools/build_peace_we_inherit.py','--check']):
            result=subprocess.run([sys.executable,'-B']+args,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
