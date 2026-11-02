"""Check real Git filters preserve binary art despite folder text rules."""
import io
from pathlib import Path
import subprocess
import unittest

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def filtered(data,path=None):
    command=['git','-c','core.safecrlf=false','hash-object','--stdin']
    command+=['--path',path]if path else['--no-filters']
    return subprocess.check_output(command,cwd=ROOT,input=data,stderr=subprocess.DEVNULL).strip()


class AssetFilters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        buffer=io.BytesIO();Image.new('RGBA',(3,2),(8,22,33,255)).save(buffer,format='PNG')
        cls.data=buffer.getvalue();cls.raw=filtered(cls.data)

    def test_binary_masters_keep_raw_bytes_under_every_forced_text_folder(self):
        folders=['mod/2985041246/gfx']
        for line in(ROOT/'.gitattributes').read_text().splitlines():
            words=line.split()
            if words and not words[0].startswith('#')and words[0].endswith('/**')and'text'in words[1:]:
                folders.append(words[0][:-3]+'/source')
        self.assertGreater(len(folders),1)
        for folder in folders:
            for extension in('png','PNG','DdS','bmp','TGA','wav','ttf','otf','jpg','JPEG','webp','OGG'):
                with self.subTest(folder=folder,extension=extension):
                    path=folder+'/synthetic-git-filter-master.'+extension
                    self.assertEqual(self.raw,filtered(self.data,path),path)

    def test_text_control_demonstrates_the_filter_can_change_the_fixture(self):
        self.assertNotEqual(self.raw,filtered(self.data,'synthetic-git-filter-control.txt'))


if __name__=='__main__':unittest.main(verbosity=2)
