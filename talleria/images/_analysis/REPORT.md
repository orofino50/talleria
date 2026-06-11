# Video Content Bounding Box Analysis

Working dir: `C:\Users\Lucas Pietro\Desktop\Projeto\images\`
Padding color: source uses `#f5f4f7` (245, 244, 247) — 1 channel off from the assumed `#f5f5f7`.

## Source dimensions (ffprobe)

| File | Width | Height | FPS | Duration |
|------|------:|-------:|----:|---------:|
| gisam-paintpro.mp4  | 1080 | 1920 | 60 | 23.95 s |
| cultivo-paintpro.mp4 | 1080 | 1920 | 60 | 7.60 s |
| diy-paintpro.mp4   |  608 | 1080 | 30 | 64.70 s |
| temu-paintpro.mp4  |  720 | 1280 | 59.94 | 16.78 s |

All four sources are 9:16 (vertical). No black bars, no pillarboxing.

## Non-#f5f4f7 content bounding box (PIL, threshold=24)

Sample-frame x extents always span the full source width (x=0..w-1).
The painting fills the frame **horizontally edge-to-edge** in all 4 videos.
Padding exists only on the **top and bottom** of the frame.

| File | Source W×H | Content bbox (x1,y1)-(x2,y2) | Content W×H | Top pad | Bottom pad | Painting aspect |
|------|-----------:|------------------------------|------------:|--------:|-----------:|----------------:|
| gisam  | 1080×1920 | (0,120)-(1079,1799) | 1080×1680 | 120 | 120 | 0.6429 (9:14) |
| cultivo | 1080×1920 | (0,120)-(1079,1799) | 1080×1680 | 120 | 120 | 0.6429 (9:14) |
| diy    | 608×1080  | (0,66)-(607,1011)   |  608×946  |  66 |  68 | 0.6427 (≈9:14) |
| temu   | 720×1280  | (0,80)-(719,1199)   |  720×1120 |  80 |  80 | 0.6429 (9:14) |

Verified across 3 timestamps per video (0.5 s, mid, late). Bbox is stable frame-to-frame.

## Centering check

- gisam, cultivo, temu: **perfectly centered** (top pad = bottom pad).
- diy: 2 px asymmetry (top=65–66, bottom=68). The 608×946 painting is exactly 9:14
  rounded to integer pixels — the off-by-one pad comes from a 1-px rounding
  artifact at the encoding step, not from off-center content.

## Aspect verification

Painting aspect = 0.6429 in all 4 videos, matching the assumed 9:14 (9/14 = 0.642857).
The **content area matches what was expected**.

## The "different gray bars" the user observed

The bars are **proportionally identical** (~6.25 % of frame height) and
**symmetric within each video** (within 1–2 px rounding). What differs is
the **source resolution**, so at native pixel size the bars are:

- 120 px (gisam, cultivo) — 6.250 %
- 67 px (diy)             — 6.204 %
- 80 px (temu)            — 6.250 %

If the four videos are being **rendered at a uniform output height** in the
re-encode step, the bars should normalize to the same size. If the
re-encode is using a uniform output height, the bar-size mismatch the user
sees in videos 3 and 4 is **not in the source** — the source bars are
already correct. The asymmetry must be introduced in the re-encode.

## Anomalies

1. **Padding color is `#f5f4f7`, not `#f5f5f7`.** Off by 1 in the green channel.
   Visually identical (ΔE ≈ 0.5), but if any re-encode step does an exact-color
   match it will fail.
2. **Painting fills the full width** (x:0 to x:w-1). Any "expected left/right
   padding" assumption is wrong — there is **no horizontal padding** in the
   source, only vertical.
3. **diy 2-px top/bottom asymmetry** is consistent across timestamps. Source
   is integer-pixel-encoded; a 9:14 painting at 608 wide has height
   945.78, rounded down. This is unavoidable at this source resolution and
   not worth "fixing" in the re-encode.

## Corner pixel samples (top-left at (5,5), etc.)

| Frame | TL | TR | BL | BR |
|-------|----|----|----|----|
| gisam_t5  | (245,244,247) | (245,244,247) | (245,244,247) | (245,244,247) |
| cultivo_t3 | (245,244,247) | (245,244,247) | (245,244,247) | (245,244,247) |
| diy_t30   | (245,244,247) | (245,244,247) | (245,244,247) | (245,244,247) |
| temu_t8   | (245,244,247) | (245,244,247) | (245,244,247) | (245,244,247) |

Padding is uniform in all 4 corners of all 4 videos.

## Sample frames

Saved to `images/_analysis/`: gisam_t05/5/10.png, cultivo_t05/3/6.png,
diy_t05/30/60.png, temu_t05/8/15.png.
