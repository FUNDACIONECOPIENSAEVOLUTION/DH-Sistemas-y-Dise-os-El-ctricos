#!/usr/bin/env python3
"""Recortar exclusivamente las fotografias de los posters, sin titulos incrustados."""
from pathlib import Path
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "assets" / "servicios"
dest = ROOT / "assets" / "servicios-v2"
dest.mkdir(parents=True, exist_ok=True)
total = 0
for path in sorted(src.glob("*.webp")):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # Los primeros 38% contienen los titulares decorativos ya impresos.
    # Preservamos el sector fotografico de la derecha.
    photographic_area = im.crop((int(w * 0.38), 0, w, h))
    photo = ImageOps.fit(photographic_area, (780, 490), method=Image.Resampling.LANCZOS, centering=(0.57, 0.5))
    photo.save(dest / path.name, "WEBP", quality=85, method=6)
    total += 1
print(f"Fotografias limpias creadas: {total}")
