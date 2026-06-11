#!/usr/bin/env python3
"""Analyze video frames to find the actual content (painting) bounding box.

The expected padding color is #f5f5f7 (245, 245, 247). We find the bounding box
of pixels that differ from this color by more than a threshold.
"""
import os
from PIL import Image
import numpy as np

TARGET = (245, 245, 247)

def find_content_bbox(img, threshold=12):
    """Return (x1, y1, x2, y2, w, h) of non-#f5f5f7 content above threshold."""
    arr = np.array(img.convert("RGB"))
    # Compute per-pixel euclidean distance from target color
    diff = arr.astype(np.int16) - np.array(TARGET, dtype=np.int16)
    dist = np.sqrt((diff ** 2).sum(axis=2))
    mask = dist > threshold
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    x1, x2 = int(xs.min()), int(xs.max())
    y1, y2 = int(ys.min()), int(ys.max())
    return (x1, y1, x2, y2, x2 - x1 + 1, y2 - y1 + 1)

def sample_corners(img, n=5):
    """Sample 4 corners and report their colors to detect if padding is uniform."""
    w, h = img.size
    corners = {
        "TL": (n, n),
        "TR": (w - n - 1, n),
        "BL": (n, h - n - 1),
        "BR": (w - n - 1, h - n - 1),
        "TM": (w // 2, n),
        "BM": (w // 2, h - n - 1),
        "LM": (n, h // 2),
        "RM": (w - n - 1, h // 2),
    }
    return {k: img.getpixel(v) for k, v in corners.items()}

def analyze(path):
    img = Image.open(path)
    w, h = img.size
    print(f"\n=== {os.path.basename(path)} ===")
    print(f"Source dimensions: {w} x {h}  (aspect {w/h:.4f})")

    corners = sample_corners(img)
    print(f"Corner samples: {corners}")

    for th in (8, 16, 24, 32):
        bbox = find_content_bbox(img, threshold=th)
        if bbox is None:
            print(f"  threshold={th:>2}: NO content above threshold (uniform color)")
            continue
        x1, y1, x2, y2, bw, bh = bbox
        pad_l, pad_r = x1, w - x2 - 1
        pad_t, pad_b = y1, h - y2 - 1
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        offset_x = cx - (w / 2)
        offset_y = cy - (h / 2)
        aspect = bw / bh
        print(f"  threshold={th:>2}: bbox=({x1},{y1})..({x2},{y2}) size={bw}x{bh} "
              f"aspect={aspect:.4f} center_offset=({offset_x:+.1f},{offset_y:+.1f}) "
              f"pads L/R/T/B={pad_l}/{pad_r}/{pad_t}/{pad_b}")

frames = [
    "gisam_t05.png", "gisam_t5.png", "gisam_t10.png",
    "cultivo_t05.png", "cultivo_t3.png", "cultivo_t6.png",
    "diy_t05.png", "diy_t30.png", "diy_t60.png",
    "temu_t05.png", "temu_t8.png", "temu_t15.png",
]
base = r"C:\Users\Lucas Pietro\Desktop\Projeto\images\_analysis"
for f in frames:
    analyze(os.path.join(base, f))
