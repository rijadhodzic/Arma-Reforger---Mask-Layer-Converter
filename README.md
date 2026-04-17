# 🎭 Arma Reforger – Mask Layer Converter

A simple Python utility that batch-converts PNG layer files into clean black-and-white mask images compatible with **Arma Reforger Workbench**.

---

## 📖 How It Works

The script reads the **alpha (transparency) channel** of each PNG and converts every pixel to either pure black or pure white:

| Input Pixel | Output Pixel |
|---|---|
| Any color / partially transparent (alpha ≥ threshold) | ⬜ White `(255)` |
| Fully transparent (alpha < threshold) | ⬛ Black `(0)` |

The result is a grayscale PNG with **no alpha channel** — exactly the format Arma Reforger Workbench expects for terrain masks.

---

## ⚙️ Requirements

- Python 3.7+
- [Pillow](https://python-pillow.org/)
- [NumPy](https://numpy.org/)

> **Note:** If these libraries are not installed, the script will attempt to install them automatically on first run.

You can also install them manually:

```bash
pip install Pillow numpy
```

---

## 🚀 Usage

```bash
# Default: reads from ./layers, saves to ./output
python convert_masks.py

# Custom input folder
python convert_masks.py -i ./my_layers

# Custom input and output folders
python convert_masks.py -i ./input -o ./masks

# Custom alpha threshold (default is 1)
python convert_masks.py --threshold 10
```

---

## 🔧 Arguments

| Argument | Default | Description |
|---|---|---|
| `-i`, `--input` | `./layers` | Folder containing source PNG files |
| `-o`, `--output` | `./output` | Folder where converted masks will be saved |
| `--threshold` | `1` | Minimum alpha value (0–255) to treat a pixel as white |

### About `--threshold`

- **Default (`1`):** Even a barely visible pixel (alpha = 1/255) becomes white. Best for capturing every painted area.
- **Higher values (e.g. `10`):** Ignores near-invisible or semi-transparent edges. Useful if your layers have feathered/soft edges you want to exclude.

---

## 📁 Folder Structure

```
project/
├── convert_masks.py
├── layers/               ← Put your source PNG layers here
│   ├── forest.png
│   ├── road.png
│   └── water.png
└── output/               ← Converted masks appear here (auto-created)
    ├── forest.png
    ├── road.png
    └── water.png
```

---

## 📊 Output

After processing, the script prints a summary for each file:

```
============================================================
  Arma Reforger Mask Converter
============================================================
  Input:     /path/to/layers
  Output:    /path/to/output
  Threshold: 1 (alpha >= 1 -> white)
  Files:     3
============================================================

  [OK] forest.png
       Coverage: 42.3%  |  White: 1,847,291px  |  Black: 2,520,709px
  [OK] road.png
       Coverage: 8.1%  |  White: 353,894px  |  Black: 4,014,106px
  [OK] water.png
       Coverage: 15.7%  |  White: 685,440px  |  Black: 3,682,560px

============================================================
  Done! Successful: 3  |  Errors: 0
  Masks saved to: /path/to/output
============================================================
```

---

## 🗺️ Arma Reforger Workbench Notes

- Masks must be **grayscale PNGs without an alpha channel** — this script handles that automatically.
- White pixels (`255`) represent areas **covered** by that terrain layer.
- Black pixels (`0`) represent areas **not covered**.
- File names are preserved, so the output files map directly to their corresponding Workbench layer slots.

---

## 📄 License

MIT — free to use, modify, and distribute.
