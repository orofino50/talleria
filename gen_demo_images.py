from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os, math

OUT = "images"
COLORS = {
    "before": "#8B7355", "after": "#2ecc71", "accent": "#e94560",
    "dark": "#1d1d1f", "light": "#f5f5f7", "white": "#ffffff", "text": "#1d1d1f"
}

def get_font(size, bold=False):
    paths = [
        "C:\\Windows\\Fonts\\inter-bold.ttf" if bold else "C:\\Windows\\Fonts\\inter-regular.ttf",
        "C:\\Windows\\Fonts\\Inter-Bold.ttf" if bold else "C:\\Windows\\Fonts\\Inter-Regular.ttf",
        "C:\\Windows\\Fonts\\ariblk.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_split_before_after(title, left_color, right_color, accent_img_path=None):
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), COLORS["light"])
    draw = ImageDraw.Draw(img)
    mid = W // 2
    lc = hex_to_rgb(left_color)
    rc = hex_to_rgb(right_color)
    
    left = Image.new("RGB", (mid, H), lc)
    left = ImageEnhance.Brightness(left).enhance(0.7)
    left = left.filter(ImageFilter.GaussianBlur(2))
    noise = Image.effect_noise((mid, H), 30).convert("RGB")
    noise = ImageEnhance.Brightness(noise).enhance(0.15)
    left = Image.blend(left, noise, 0.3)
    draw_left = ImageDraw.Draw(left)
    for _ in range(6):
        x = int(math.sin(_ * 1.5) * 50 + mid//2)
        y1 = _ * 130 + 40
        draw_left.line([(x-20, y1), (x+30, y1+60)], fill=(80, 60, 40, 180), width=2)
    img.paste(left, (0, 0))
    
    right = Image.new("RGB", (W - mid, H), rc)
    right = ImageEnhance.Brightness(right).enhance(1.1)
    right = right.filter(ImageFilter.BoxBlur(1))
    img.paste(right, (mid, 0))
    
    draw.line([(mid, 0), (mid, H)], fill=(255, 255, 255), width=4)
    draw.line([(mid-1, 0), (mid-1, H)], fill=(0, 0, 0), width=1)
    
    fnt_large = get_font(40, bold=True)
    fnt_small = get_font(22)
    
    bbox = draw.textbbox((0, 0), "ANTES", font=fnt_large)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    draw.text(((mid - tw) // 2, H - 80), "ANTES", font=fnt_large, fill=(255, 255, 255))
    
    bbox = draw.textbbox((0, 0), "DESPUÉS", font=fnt_large)
    tw = bbox[2]-bbox[0]
    draw.text((mid + (W - mid - tw) // 2, H - 80), "DESPUÉS", font=fnt_large, fill=(255, 255, 255))
    
    bbox = draw.textbbox((0, 0), title, font=fnt_small)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 30), title, font=fnt_small, fill=(0, 0, 0))
    
    if accent_img_path and os.path.exists(accent_img_path):
        badge = Image.open(accent_img_path).convert("RGBA")
        badge.thumbnail((180, 180))
        img.paste(badge, (W - badge.width - 30, 30), badge)
    
    return img

# 1
img = create_split_before_after("PAREDES — Transformaci\u00f3n profesional", "#8B7355", "#D4C5A9", os.path.join(OUT, "hastahoy.webp"))
img.save(os.path.join(OUT, "demo-paredes.jpg"), quality=92)
print(f"1/5 demo-paredes.jpg ({os.path.getsize(os.path.join(OUT, 'demo-paredes.jpg'))//1024}KB)")

# 2
img = create_split_before_after("MUEBLES — Restauraci\u00f3n de superficies", "#6B4226", "#A0785A", os.path.join(OUT, "hastahoy.webp"))
img.save(os.path.join(OUT, "demo-muebles.jpg"), quality=92)
print(f"2/5 demo-muebles.jpg ({os.path.getsize(os.path.join(OUT, 'demo-muebles.jpg'))//1024}KB)")

# 3 - Wood surface
W, H = 1200, 800
img = Image.new("RGB", (W, H), (62, 39, 35))
draw = ImageDraw.Draw(img)
for i in range(20):
    y = i * 40
    shade = 60 + int(50 * math.sin(i * 0.8))
    draw.rectangle([(0, y), (W, y+38)], fill=(shade, shade-20, shade-40))
wood_img = Image.open(os.path.join(OUT, "superficies.webp")).convert("RGBA")
wood_img.thumbnail((W, H))
img.paste(wood_img, (0, 0), wood_img)
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 180))
img.paste(overlay, (0, 0), overlay)
fnt = get_font(36, bold=True)
draw.text((60, 60), "ACABADO EN MADERA", font=fnt, fill=(212, 197, 169))
fnt2 = get_font(24)
draw.text((60, 110), "Resultado uniforme \u2014 Sin imperfecciones", font=fnt2, fill=(245, 245, 247))
draw.text((60, 145), "Pintura profesional sobre madera con PaintPro", font=fnt2, fill=(170, 170, 170))
prod = Image.open(os.path.join(OUT, "hastahoy.webp")).convert("RGBA")
prod.thumbnail((180, 180))
img.paste(prod, (W-prod.width-40, H-prod.height-40), prod)
img.save(os.path.join(OUT, "demo-madera.jpg"), quality=92)
print(f"3/5 demo-madera.jpg ({os.path.getsize(os.path.join(OUT, 'demo-madera.jpg'))//1024}KB)")

# 4 - Metal surface
img = Image.new("RGB", (W, H), (69, 90, 100))
draw = ImageDraw.Draw(img)
for i in range(50):
    x = i * 25
    shade = 70 + int(60 * math.sin(i * 1.2))
    draw.rectangle([(x, 0), (x+22, H)], fill=(shade+30, shade+50, shade+40))
metal_img = Image.open(os.path.join(OUT, "superficies.webp")).convert("RGBA")
metal_img.thumbnail((W, H))
img.paste(metal_img, (0, 0), metal_img)
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 180))
img.paste(overlay, (0, 0), overlay)
fnt = get_font(36, bold=True)
draw.text((60, 60), "ACABADO EN METAL", font=fnt, fill=(144, 164, 174))
fnt2 = get_font(24)
draw.text((60, 110), "Adherencia perfecta \u2014 Sin goteo", font=fnt2, fill=(245, 245, 247))
draw.text((60, 145), "Pintura profesional sobre metal con PaintPro", font=fnt2, fill=(170, 170, 170))
prod = Image.open(os.path.join(OUT, "hastahoy.webp")).convert("RGBA")
prod.thumbnail((180, 180))
img.paste(prod, (W-prod.width-40, H-prod.height-40), prod)
img.save(os.path.join(OUT, "demo-metal.jpg"), quality=92)
print(f"4/5 demo-metal.jpg ({os.path.getsize(os.path.join(OUT, 'demo-metal.jpg'))//1024}KB)")

# 5 - In Action
img = Image.new("RGB", (W, H), (44, 44, 44))
draw = ImageDraw.Draw(img)
for y in range(H):
    shade = int(30 + 60 * (y / H))
    draw.line([(0, y), (W, y)], fill=(shade, shade, shade+10))
hero = Image.open(os.path.join(OUT, "hastahoy.webp")).convert("RGBA")
hero.thumbnail((500, 500))
hero_x = (W - hero.width) // 2
hero_y = 60
img.paste(hero, (hero_x, hero_y), hero)
for r in range(120, 250, 15):
    alpha = max(0, int(80 - (r-120) * 0.5))
    draw.ellipse([(W//2-r, hero_y+hero.height//2-r), (W//2+r, hero_y+hero.height//2+r)],
                 outline=(233, 69, 96, alpha), width=2)
fnt = get_font(32, bold=True)
draw.text(((W-600)//2, hero_y + hero.height + 30), "PAINTPRO\u2122 EN ACCI\u00d3N", font=fnt, fill=(233, 69, 96))
fnt2 = get_font(20)
draw.text(((W-500)//2, hero_y + hero.height + 80), "Pulverizaci\u00f3n uniforme \u00b7 Control preciso", font=fnt2, fill=(204, 204, 204))
draw.text(((W-450)//2, hero_y + hero.height + 110), "Sin cables \u00b7 Sin compresor \u00b7 Sin complicaciones", font=fnt2, fill=(153, 153, 153))
img.save(os.path.join(OUT, "demo-accion.jpg"), quality=92)
print(f"5/5 demo-accion.jpg ({os.path.getsize(os.path.join(OUT, 'demo-accion.jpg'))//1024}KB)")
