"""Create 192x144 load_N_small.dds thumbnails for the HOI4 1.19 main-menu background picker."""
import struct, sys
from PIL import Image
import os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')

SRC = REPO + '/mod/2985041246/gfx/loadingscreens/'


def write_dds_bgra(path, im):
    im = im.convert('RGBA')
    w, h = im.size
    r, g, b, a = im.split()
    data = Image.merge('RGBA', (b, g, r, a)).tobytes()
    DDSD = 0x1 | 0x2 | 0x4 | 0x1000 | 0x8  # caps, height, width, pixelformat, pitch
    pf = struct.pack('<II4sIIIII', 32, 0x41, b'\0\0\0\0', 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    header = struct.pack('<4sIIIIIII44s', b'DDS ', 124, DDSD, h, w, w * 4, 0, 1, b'\0' * 44) + pf + struct.pack('<IIIII', 0x1000, 0, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(header + data)


for n in range(1, 8):
    im = Image.open(f'{SRC}load_{n}.dds')
    # crop to 4:3 around the centre, then thumbnail
    w, h = im.size
    tw = min(w, h * 4 // 3)
    left = (w - tw) // 2
    im = im.crop((left, 0, left + tw, h)).resize((192, 144), Image.LANCZOS)
    write_dds_bgra(f'{SRC}load_{n}_small.dds', im)
    print('wrote', n, im.size)

