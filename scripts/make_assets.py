"""Build the Rodan icon sizes from the brand source image.

Runs inside Docker through scripts/make-assets.sh. Reads assets/source/, writes assets/.
Source: https://rodan.io/apple-touch-icon.png (Rodan mark in white on Navy #000034).
"""
import sys
from pathlib import Path
from PIL import Image

repo = Path(sys.argv[1])
src = Image.open(repo / "assets/source/rodan-apple-touch-icon.png").convert("RGB")
assert src.size[0] == src.size[1], "source must be square"

# Square icons: the brand tile at several sizes. Opaque, so JPG or PNG both work.
for size in (1024, 512, 256, 128, 64):
    out = src.resize((size, size), Image.LANCZOS)
    out.save(repo / f"assets/rodan-icon-{size}.png", optimize=True)

# Transparent marks: use the tile's luminance as the alpha channel of a flat colour.
lum = src.convert("L")
navy_bg = lum.getpixel((2, 2))
alpha = lum.point(lambda v: max(0, min(255, int((v - navy_bg) * 255 / (255 - navy_bg)))))
for name, colour in (("white", (255, 255, 255)), ("navy", (0, 0, 52))):
    mark = Image.new("RGBA", src.size, colour + (0,))
    mark.putalpha(alpha)
    mark.resize((512, 512), Image.LANCZOS).save(repo / f"assets/rodan-mark-{name}-512.png", optimize=True)
print("ok")
