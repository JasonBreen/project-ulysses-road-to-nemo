"""Fit complete original art to native event apertures; never crop a scene."""
from pathlib import Path
import io
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
NAVY = (8, 22, 33, 255)
SIZES = {'country_event': (210, 176), 'news_event': (397, 153)}

def contain(source, event_type='country_event'):
    """Preserve the entire composition, with deliberate opaque navy padding."""
    size = SIZES[event_type]
    if isinstance(source, Image.Image):
        original = source.convert('RGBA')
    else:
        with Image.open(source) as image:
            original = image.convert('RGBA')
    fitted = ImageOps.contain(original, size, Image.Resampling.LANCZOS)
    image = Image.new('RGBA', size, NAVY)
    image.alpha_composite(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return image

def assert_fits(event_type, size, scale=1, frames=1):
    """Use actual texture frame dimensions and the effective GUI scale."""
    if event_type not in SIZES or frames < 1 or size[0] % frames or scale <= 0:
        raise ValueError('Unsupported event picture/frame/scale contract')
    width, height = size[0] / frames * scale, size[1] * scale
    allowed = SIZES[event_type]
    if width > allowed[0] or height > allowed[1]:
        raise ValueError(f'{event_type} picture exceeds its actual aperture: {width}x{height} > {allowed}')
    return width, height

def same_review_png(left,right):
    """Only review PNG compression may vary; dimensions/RGBA must be exact."""
    try:
        with Image.open(io.BytesIO(left)) as a,Image.open(io.BytesIO(right)) as b:
            return a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
    except (OSError,ValueError):return False
