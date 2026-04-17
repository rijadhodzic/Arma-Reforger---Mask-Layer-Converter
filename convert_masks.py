#!/usr/bin/env python3
"""
Arma Reforger - Mask Layer Converter
=====================================
Skenira folder s PNG layerima i svaki konvertira u crno-bijelu masku:
  - Svaki pixel koji ima IKAKVU boju (pa i djelomicno transparentan) -> 100% BIJELA
  - Svaki transparentan pixel -> 100% CRNA

Koristenje:
    python convert_masks.py                     # konvertira iz ./layers, sprema u ./output
    python convert_masks.py -i ./moj_folder     # custom input folder
    python convert_masks.py -i ./in -o ./out    # custom input i output folder
    python convert_masks.py --threshold 10      # prag transparencije (default: 1)
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Instaliram potrebne biblioteke...")
    os.system(f"{sys.executable} -m pip install Pillow numpy --quiet")
    from PIL import Image
    import numpy as np


def convert_layer_to_mask(input_path: Path, output_path: Path, threshold: int = 1):
    """
    Konvertira jedan PNG layer u crno-bijelu masku.
    
    threshold: minimalna alpha vrijednost (0-255) da se pixel smatra "popunjenim"
               default=1 znaci da i najmanji trag boje/transparencije postaje bijelo
    """
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)

    # Alpha kanal je 4. kanal (index 3), vrijednosti 0-255
    alpha = data[:, :, 3]

    # Kreiraj novu sliku: crna pozadina
    mask = np.zeros((data.shape[0], data.shape[1]), dtype=np.uint8)

    # Sve sto ima alpha >= threshold postaje bijelo (255)
    mask[alpha >= threshold] = 255

    # Spremi kao grayscale PNG (bez alpha kanala - Workbench treba cisti BW)
    result = Image.fromarray(mask, mode="L")
    result.save(output_path, "PNG")

    # Statistika
    total_pixels = mask.size
    white_pixels = np.count_nonzero(mask)
    black_pixels = total_pixels - white_pixels
    coverage = (white_pixels / total_pixels) * 100

    return white_pixels, black_pixels, coverage


def process_folder(input_folder: str, output_folder: str, threshold: int = 1):
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        print(f"GRESKA: Input folder ne postoji: {input_path.absolute()}")
        sys.exit(1)

    # Nadji sve PNG fajlove
    png_files = list(input_path.glob("*.png")) + list(input_path.glob("*.PNG"))

    if not png_files:
        print(f"Nema PNG fajlova u: {input_path.absolute()}")
        sys.exit(1)

    # Kreiraj output folder ako ne postoji
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Arma Reforger Mask Converter")
    print(f"{'='*60}")
    print(f"  Input:     {input_path.absolute()}")
    print(f"  Output:    {output_path.absolute()}")
    print(f"  Threshold: {threshold} (alpha >= {threshold} -> bijelo)")
    print(f"  Fajlova:   {len(png_files)}")
    print(f"{'='*60}\n")

    success = 0
    errors = 0

    for png_file in sorted(png_files):
        out_file = output_path / png_file.name
        try:
            white, black, coverage = convert_layer_to_mask(png_file, out_file, threshold)
            print(f"  [OK] {png_file.name}")
            print(f"       Pokrivenost: {coverage:.1f}%  |  Bijelo: {white:,}px  |  Crno: {black:,}px")
            success += 1
        except Exception as e:
            print(f"  [GRESKA] {png_file.name}: {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"  Gotovo! Uspjesno: {success}  |  Greske: {errors}")
    print(f"  Maske spremljene u: {output_path.absolute()}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Konvertira PNG layere u crno-bijele maske za Arma Reforger Workbench"
    )
    parser.add_argument(
        "-i", "--input",
        default="./layers",
        help="Folder s PNG layerima (default: ./layers)"
    )
    parser.add_argument(
        "-o", "--output",
        default="./output",
        help="Folder gdje ce se spremiti maske (default: ./output)"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1,
        choices=range(0, 256),
        metavar="0-255",
        help="Minimalna alpha vrijednost da se pixel smatra popunjenim (default: 1)"
    )

    args = parser.parse_args()
    process_folder(args.input, args.output, args.threshold)


if __name__ == "__main__":
    main()
