#!/usr/bin/env python3
"""Verify edge pixels and dimensions of extracted frames."""
import os
from PIL import Image

frames = [
    "gisam_t05.png", "gisam_t5.png", "gisam_t10.png",
    "cultivo_t05.png", "cultivo_t3.png", "cultivo_t6.png",
    "diy_t05.png", "diy_t30.png", "diy_t60.png",
    "temu_t05.png", "temu_t8.png", "temu_t15.png",
]
base = r"C:\Users\Lucas Pietro\Desktop\Projeto\images\_analysis"

for f in frames:
    img = Image.open(os.path.join(base, f)).convert("RGB")
    w, h = img.size
    # Sample the column at x = w/2 from y=0 to y=10 and y=h-10 to y=h-1
    mid_x = w // 2
    top_strip = [img.getpixel((mid_x, y)) for y in range(0, 10)]
    bottom_strip = [img.getpixel((mid_x, h - 10 + y)) for y in range(10)]
    # Find where the column transitions from #f5f4f7 to other content
    arr_top = []
    prev = None
    for y in range(0, 200):
        p = img.getpixel((mid_x, y))
        if p != prev:
            arr_top.append((y, p))
            prev = p
        if len(arr_top) > 6:
            break
    arr_bot = []
    prev = None
    for y in range(h - 200, h):
        p = img.getpixel((mid_x, y))
        if p != prev:
            arr_bot.append((y, p))
            prev = p
        if len(arr_bot) > 6:
            break
    print(f"\n{f}  size={w}x{h}")
    print(f"  top edge (mid x): first 10 px = {top_strip[:3]}")
    print(f"  bottom edge (mid x): last 10 px = {bottom_strip[-3:]}")
    print(f"  top transitions: {arr_top[:5]}")
    print(f"  bottom transitions: {arr_bot[-5:]}")
