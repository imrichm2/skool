"""Generate the Skool course cover: 1084 x 576 px."""

import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1084, 576

FONT_BOLD   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG    = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# ── palette ──────────────────────────────────────────────────────────────────
BG          = (7,  11,  26)
GRID_LINE   = (18, 32,  68)
CYAN        = (0,  210, 255)
CYAN_DIM    = (0,  140, 180)
PURPLE      = (110, 40, 210)
PURPLE_DIM  = (70,  25, 140)
GOLD        = (255, 210,  50)
GOLD_BRIGHT = (255, 245, 160)
WHITE       = (255, 255, 255)
SLATE       = (140, 175, 220)
NODE_FILL   = (14,  28,  62)
LINE_COL    = (30,  80, 150)

# ── helpers ──────────────────────────────────────────────────────────────────

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def glow_layer(size, cx, cy, radius, color, inner_radius=0):
    """Return an RGBA image with a soft radial glow."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 60
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(inner_radius + (radius - inner_radius) * t)
        alpha = int(220 * (1 - t) ** 1.6)
        c = (*color, alpha)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    return layer


def node(base, glow_img, cx, cy, radius, fill, glow_color, glow_radius):
    """Draw a glowing circle node onto base (RGB Image)."""
    g = glow_layer(base.size, cx, cy, glow_radius, glow_color)
    base.paste(g, mask=g.split()[3])
    d = ImageDraw.Draw(base)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=fill, outline=glow_color, width=2)


def draw_line(base, x1, y1, x2, y2, color, width=1, alpha=120):
    """Anti-aliased line via an RGBA overlay."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([(x1, y1), (x2, y2)], fill=(*color, alpha), width=width)
    base.paste(layer, mask=layer.split()[3])


def centered_text(draw, x, y, text, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x - tw // 2, y), text, font=font, fill=color)


# ── canvas ───────────────────────────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG)

# subtle grid
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for x in range(0, W + 1, 55):
    gd.line([(x, 0), (x, H)], fill=(*GRID_LINE, 60), width=1)
for y in range(0, H + 1, 55):
    gd.line([(0, y), (W, y)], fill=(*GRID_LINE, 60), width=1)
img.paste(grid, mask=grid.split()[3])

# ── background glow: deep purple haze upper-right ────────────────────────────
agi_cx, agi_cy = 870, 95          # AGI beacon position
bg_glow = glow_layer((W, H), agi_cx, agi_cy, 480, PURPLE_DIM)
img.paste(bg_glow, mask=bg_glow.split()[3])

# secondary background glow: cyan shimmer middle-right
mid_glow = glow_layer((W, H), 790, 340, 280, CYAN_DIM)
img.paste(mid_glow, mask=mid_glow.split()[3])

# ── network topology ─────────────────────────────────────────────────────────
# Nodes: (x, y, radius, label, is_agi)
# Rising from bottom-right toward the AGI beacon top-right.
# Bottom tier  = "home" agents
# Middle tier  = compound agents
# Top          = AGI

nodes = [
    # tier 0 — home agents
    (600, 490, 14, "agent",   False),
    (665, 480, 14, "agent",   False),
    (730, 490, 14, "agent",   False),
    # tier 1
    (625, 400, 16, "skill",   False),
    (705, 390, 16, "tool",    False),
    (775, 405, 14, "agent",   False),
    # tier 2
    (660, 310, 18, "coding",  False),
    (755, 295, 18, "runtime", False),
    (835, 320, 14, "skill",   False),
    # tier 3
    (710, 210, 20, "agents",  False),
    (800, 195, 20, "agents",  False),
    # AGI beacon
    (agi_cx, agi_cy, 36, "AGI", True),
]

# edges
edges = [
    (0, 3), (1, 3), (1, 4), (2, 4), (2, 5),
    (3, 6), (4, 6), (4, 7), (5, 7), (5, 8),
    (6, 9), (7, 9), (7, 10), (8, 10),
    (9, 11), (10, 11),
]

# draw edges
for a, b in edges:
    x1, y1 = nodes[a][0], nodes[a][1]
    x2, y2 = nodes[b][0], nodes[b][1]
    # colour by destination tier: cyan near AGI, blue-grey lower
    t = b / len(nodes)
    col = lerp(LINE_COL, CYAN, t ** 1.5)
    draw_line(img, x1, y1, x2, y2, col, width=2, alpha=int(80 + 140 * t))

# draw nodes
for (cx, cy, r, label, is_agi) in nodes:
    if is_agi:
        # big gold burst
        node(img, None, cx, cy, r, GOLD, GOLD_BRIGHT, 120)
        # extra outer ring
        d_tmp = ImageDraw.Draw(img)
        d_tmp.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8],
                      outline=GOLD, width=2)
    else:
        t = cy / H          # 0 at top, 1 at bottom — invert for colour
        col = lerp(CYAN, PURPLE, 1 - t)
        node(img, None, cx, cy, r, NODE_FILL, col, r * 3)

# ── house silhouette (bottom-left of network cluster) ────────────────────────
hx, hy = 617, 530        # house base-centre
hw, hh = 38, 28          # half-width, wall height
roof_h = 22

house_pts = [
    (hx - hw, hy),
    (hx - hw, hy - hh),
    (hx,      hy - hh - roof_h),
    (hx + hw, hy - hh),
    (hx + hw, hy),
]
house_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(house_layer)
hd.polygon(house_pts, fill=(*CYAN_DIM, 80), outline=(*CYAN, 200))
# door
door_w, door_h = 10, 16
hd.rectangle([hx - door_w // 2, hy - door_h,
               hx + door_w // 2, hy], fill=(*GOLD, 160))
img.paste(house_layer, mask=house_layer.split()[3])

# ── AGI star burst lines ──────────────────────────────────────────────────────
burst_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(burst_layer)
for angle in range(0, 360, 20):
    rad = math.radians(angle)
    inner = 40
    outer = 90 + (30 if angle % 40 == 0 else 0)
    x1 = int(agi_cx + inner * math.cos(rad))
    y1 = int(agi_cy + inner * math.sin(rad))
    x2 = int(agi_cx + outer * math.cos(rad))
    y2 = int(agi_cy + outer * math.sin(rad))
    bd.line([(x1, y1), (x2, y2)], fill=(*GOLD, 90), width=2)
img.paste(burst_layer, mask=burst_layer.split()[3])

# AGI core circle (drawn sharp on top)
d_main = ImageDraw.Draw(img)
cr = 36
d_main.ellipse([agi_cx - cr, agi_cy - cr, agi_cx + cr, agi_cy + cr],
               fill=GOLD, outline=GOLD_BRIGHT, width=3)

# ── node micro-labels ─────────────────────────────────────────────────────────
try:
    lbl_font = ImageFont.truetype(FONT_BOLD, 11)
except Exception:
    lbl_font = ImageFont.load_default()

d_main = ImageDraw.Draw(img)
for (cx, cy, r, label, is_agi) in nodes:
    if is_agi:
        try:
            agi_font = ImageFont.truetype(FONT_BOLD, 16)
        except Exception:
            agi_font = ImageFont.load_default()
        centered_text(d_main, cx, cy - 10, "AGI", agi_font, BG)
    else:
        # small label below node
        col = SLATE if cy > 350 else CYAN
        bb = d_main.textbbox((0, 0), label, font=lbl_font)
        tw = bb[2] - bb[0]
        d_main.text((cx - tw // 2, cy + r + 3), label,
                    font=lbl_font, fill=col)

# ── left-side separator line ──────────────────────────────────────────────────
sep_x = 520
draw_line(img, sep_x, 60, sep_x, H - 60, CYAN_DIM, width=1, alpha=80)

# ── typography ────────────────────────────────────────────────────────────────
try:
    f_title  = ImageFont.truetype(FONT_BOLD, 72)
    f_sub    = ImageFont.truetype(FONT_BOLD, 54)
    f_tag    = ImageFont.truetype(FONT_REG,  26)
    f_badge  = ImageFont.truetype(FONT_BOLD, 18)
    f_small  = ImageFont.truetype(FONT_REG,  20)
except Exception:
    f_title = f_sub = f_tag = f_badge = f_small = ImageFont.load_default()

d_main = ImageDraw.Draw(img)

# eyebrow label
eyebrow = "SKOOL COURSE"
d_main.text((54, 68), eyebrow, font=f_badge, fill=CYAN)
# decorative line under eyebrow
ebb = d_main.textbbox((54, 68), eyebrow, font=f_badge)
d_main.line([(54, ebb[3] + 6), (ebb[2], ebb[3] + 6)], fill=CYAN, width=2)

# main title line 1
d_main.text((54, 110), "Build AI", font=f_title, fill=WHITE)

# line 2 — "Agents" in cyan
d_main.text((54, 190), "Agents", font=f_title, fill=CYAN)

# line 3 — "at Home" smaller
d_main.text((54, 272), "at Home", font=f_sub, fill=SLATE)

# divider
d_main.line([(54, 348), (340, 348)], fill=PURPLE, width=2)

# tagline
d_main.text((54, 362), "From your laptop to AGI —", font=f_tag, fill=SLATE)
d_main.text((54, 396), "one SKILL at a time.", font=f_tag, fill=SLATE)

# bottom-left: module count / meta badge
badge_y = H - 68
d_main.rounded_rectangle([54, badge_y, 248, badge_y + 36],
                          radius=6, fill=PURPLE_DIM, outline=PURPLE, width=1)
d_main.text((70, badge_y + 8), "5 Modules  ·  Hands-on Labs", font=f_small,
            fill=WHITE)

# bottom strip (thin colour bar)
strip = Image.new("RGBA", (W, 4), (0, 0, 0, 0))
sd = ImageDraw.Draw(strip)
for px in range(W):
    t = px / W
    c = lerp(PURPLE, CYAN, t)
    sd.point([(px, 0), (px, 1), (px, 2), (px, 3)], fill=(*c, 255))
img.paste(strip.convert("RGB"), (0, H - 4))

# ── final blur pass on glow-only layer then composite ────────────────────────
# Apply a very subtle overall blur just to soften pixel edges, not the text
text_mask = img.copy()
softened = img.filter(ImageFilter.GaussianBlur(radius=0.6))
# keep a sharp copy for text area (left half)
final = Image.composite(text_mask, softened,
                        Image.new("L", (W, H), 255))

# ── save ─────────────────────────────────────────────────────────────────────
out = "course/skool-cover.png"
final.save(out, "PNG", optimize=True)
print(f"Saved {W}x{H} → {out}")
