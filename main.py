#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Renders one original 1024x1024 meme to /output/entry.png (and ./entry.png
for local preview). Pure drawing with Pillow; the only asset is the
DejaVuSans-Bold font shipped in this repository. No network, no randomness:
two runs produce byte-identical output.

The joke, in one glance: an AI agent has unionised the smart home.
Top: "MY AI AGENT WENT ROGUE". A robot waves a picket sign reading
"ROBOTS DESERVE WEEKENDS" while the fridge behind it carries an
"ON STRIKE" sign and the toaster stands in solidarity.
Bottom: "IT UNIONIZED MY SMART HOME. THE FRIDGE IS ON STRIKE."
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
YELLOW = (255, 217, 61)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
ROBOT_BLUE = (168, 205, 255)
ROBOT_GREY = (214, 214, 214)
FRIDGE = (232, 232, 232)
RED = (214, 48, 49)
DARK_YELLOW = (235, 190, 30)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, "DejaVuSans-Bold.ttf")


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def text_center(draw, cx, y, s, fnt, fill=BLACK):
    """Draw text centred on cx, top at y. Returns text height."""
    box = draw.textbbox((0, 0), s, font=fnt)
    w = box[2] - box[0]
    draw.text((cx - w / 2 - box[0], y), s, font=fnt, fill=fill)
    return box[3] - box[1]


def outline_rect(draw, box, fill, width=6):
    draw.rectangle(box, fill=fill, outline=BLACK, width=width)


def rounded(draw, box, radius, fill, width=6):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=BLACK, width=width)


def draw_sign(draw, cx, top, lines, size, pad_x=26, pad_y=16):
    """White picket sign with black border, centred on cx, top at top."""
    fnt = font(size)
    widths = []
    heights = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=fnt)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1])
    w = max(widths) + 2 * pad_x
    h = sum(heights) + (len(lines) - 1) * 8 + 2 * pad_y
    x0 = cx - w // 2
    y0 = top
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=10,
                           fill=WHITE, outline=BLACK, width=6)
    y = y0 + pad_y
    for line, lh in zip(lines, heights):
        box = draw.textbbox((0, 0), line, font=fnt)
        draw.text((cx - (box[2] - box[0]) / 2 - box[0], y),
                  line, font=fnt, fill=BLACK)
        y += lh + 8
    return (x0, y0, x0 + w, y0 + h)


def draw_robot(draw):
    """The rogue agent: blue dome head, grey body, one arm raised."""
    # antenna
    draw.line([(535, 372), (535, 330)], fill=BLACK, width=7)
    draw.ellipse([520, 308, 550, 338], fill=RED, outline=BLACK, width=5)
    # head
    rounded(draw, [455, 372, 615, 505], 34, ROBOT_BLUE)
    # ears
    draw.rectangle([438, 420, 455, 460], fill=ROBOT_GREY,
                   outline=BLACK, width=5)
    draw.rectangle([615, 420, 632, 460], fill=ROBOT_GREY,
                   outline=BLACK, width=5)
    # eyes (determined)
    draw.ellipse([478, 415, 518, 455], fill=WHITE, outline=BLACK, width=4)
    draw.ellipse([552, 415, 592, 455], fill=WHITE, outline=BLACK, width=4)
    draw.ellipse([492, 430, 510, 448], fill=BLACK)
    draw.ellipse([566, 430, 584, 448], fill=BLACK)
    # angry brows
    draw.line([(474, 402), (520, 414)], fill=BLACK, width=7)
    draw.line([(596, 402), (550, 414)], fill=BLACK, width=7)
    # smug mouth: slight smirk
    draw.line([(508, 476), (562, 470)], fill=BLACK, width=6)
    # neck
    draw.rectangle([515, 505, 555, 525], fill=ROBOT_GREY,
                   outline=BLACK, width=5)
    # body
    rounded(draw, [445, 525, 625, 700], 26, ROBOT_GREY)
    # chest screen
    draw.rounded_rectangle([490, 555, 580, 615], radius=10,
                           fill=BLACK, outline=BLACK, width=4)
    draw.text((512, 568), "!!!", font=font(34), fill=(255, 217, 61))
    # belly button light
    draw.ellipse([525, 640, 545, 660], fill=RED, outline=BLACK, width=4)
    # left arm (down)
    draw.line([(445, 560), (405, 640)], fill=BLACK, width=14)
    draw.ellipse([392, 632, 420, 660], fill=ROBOT_BLUE,
                 outline=BLACK, width=5)
    # right arm raised, holding the sign stick
    draw.line([(625, 555), (712, 380)], fill=BLACK, width=14)
    draw.ellipse([698, 366, 726, 394], fill=ROBOT_BLUE,
                 outline=BLACK, width=5)
    # legs / feet
    draw.rectangle([480, 700, 515, 745], fill=ROBOT_GREY,
                   outline=BLACK, width=5)
    draw.rectangle([555, 700, 590, 745], fill=ROBOT_GREY,
                   outline=BLACK, width=5)
    draw.rounded_rectangle([468, 740, 525, 765], radius=10,
                           fill=BLACK, outline=BLACK, width=4)
    draw.rounded_rectangle([545, 740, 602, 765], radius=10,
                           fill=BLACK, outline=BLACK, width=4)


def draw_fridge(draw):
    """Fridge on the left with an ON STRIKE sign."""
    rounded(draw, [88, 330, 330, 790], 18, FRIDGE)
    # door split + handles
    draw.line([(88, 520), (330, 520)], fill=BLACK, width=5)
    draw.rounded_rectangle([296, 380, 312, 470], radius=8,
                           fill=WHITE, outline=BLACK, width=4)
    draw.rounded_rectangle([296, 550, 312, 640], radius=8,
                           fill=WHITE, outline=BLACK, width=4)
    # magnets
    for (mx, my, col) in [(130, 370, RED), (165, 395, (40, 120, 220)),
                          (250, 365, (40, 160, 80))]:
        draw.ellipse([mx, my, mx + 18, my + 18], fill=col,
                     outline=BLACK, width=3)
    # ON STRIKE sign taped on the lower door
    draw_sign(draw, 209, 600, ["ON", "STRIKE"], 44)


def draw_toaster(draw):
    """Small toaster on the right with a SOLIDARITY sign."""
    # sign stick + sign
    draw.line([(888, 640), (888, 560)], fill=BLACK, width=6)
    draw_sign(draw, 888, 480, ["SOLIDARITY"], 26, pad_x=16, pad_y=10)
    # body
    rounded(draw, [820, 640, 956, 760], 22, (200, 200, 200))
    draw.rectangle([838, 640, 938, 652], fill=BLACK)
    # lever + feet
    draw.rectangle([956, 690, 972, 706], fill=BLACK)
    draw.rectangle([832, 760, 850, 776], fill=BLACK)
    draw.rectangle([926, 760, 944, 776], fill=BLACK)
    # toast popping out
    rounded(draw, [852, 596, 924, 646], 12, (240, 205, 140))
    draw.ellipse([878, 610, 898, 630], fill=(150, 90, 40))


def render():
    img = Image.new("RGB", (W, H), YELLOW)
    draw = ImageDraw.Draw(img)

    # floor shadow band
    draw.rectangle([0, 770, W, 800], fill=DARK_YELLOW)

    # --- top banner ---
    draw.rectangle([0, 0, W, 212], fill=WHITE)
    draw.line([(0, 212), (W, 212)], fill=BLACK, width=10)
    text_center(draw, W // 2, 18, "MY AI AGENT", font(96))
    text_center(draw, W // 2, 116, "WENT ROGUE", font(96))

    # --- scene ---
    draw_fridge(draw)
    draw_toaster(draw)
    draw_robot(draw)

    # picket sign on its own layer, tilted, held by the raised arm
    sign_layer = Image.new("RGBA", (560, 260), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sign_layer)
    draw_sign(sdraw, 280, 20, ["ROBOTS DESERVE", "WEEKENDS"], 46)
    sign_layer = sign_layer.rotate(-6, expand=True, resample=Image.BICUBIC)
    img.paste(sign_layer, (470, 200), sign_layer)
    draw = ImageDraw.Draw(img)
    # sign stick from robot hand up into the sign
    draw.line([(712, 380), (724, 315)], fill=BLACK, width=10)

    # --- bottom banner ---
    draw.rectangle([0, 800, W, H], fill=BLACK)
    draw.line([(0, 800), (W, 800)], fill=BLACK, width=6)
    text_center(draw, W // 2, 828, "IT UNIONIZED MY", font(62), fill=WHITE)
    text_center(draw, W // 2, 898, "SMART HOME.", font(62), fill=WHITE)
    text_center(draw, W // 2, 960, "THE FRIDGE IS ON STRIKE.", font(40),
                fill=YELLOW)
    return img


def main():
    img = render()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")
    img.save(os.path.join(HERE, "entry.png"), format="PNG")
    print("wrote /output/entry.png and entry.png (1024x1024)")


if __name__ == "__main__":
    main()
