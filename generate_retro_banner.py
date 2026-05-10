import PIL.Image
import PIL.ImageDraw
import random

W, H = 256, 80
scale = 3
N = 64

# Colors
SKY = (15, 15, 35, 255)        # night sky
MOON = (240, 230, 140, 255)
MTN_BG = (25, 25, 50, 255)
MTN_FG = (35, 35, 70, 255)
GROUND = (25, 60, 35, 255)
ROAD = (40, 40, 45, 255)
ROAD_LINE = (180, 180, 180, 255)
TREE_TRUNK = (60, 30, 15, 255)
TREE_LEAVES = (15, 45, 25, 255)

# Char
SKIN = (255, 204, 153, 255)
HAIR = (50, 30, 20, 255)
SHIRT = (41, 128, 185, 255)
PANTS = (44, 62, 80, 255)
SHOES = (20, 20, 20, 255)
GLASSES = (200, 200, 200, 255)

random.seed(42)
stars = [(random.randint(0, W), random.randint(0, 35)) for _ in range(30)]

frames = []

for fi in range(N):
    img = PIL.Image.new("RGBA", (W, H), SKY)
    draw = PIL.ImageDraw.Draw(img)
    
    # Stars
    for sx, sy in stars:
        if (sx + sy + fi) % 10 < 8:
            draw.point([sx, sy], fill=(255, 255, 255, 200))
            
    # Moon
    draw.ellipse([200, 10, 216, 26], fill=MOON)
    
    # Mountain BG
    offset_bg = int(fi * 0.5) % 32
    for i in range(-1, W//32 + 2):
        bx = i * 32 - offset_bg
        draw.polygon([(bx, 50), (bx+16, 25), (bx+32, 50)], fill=MTN_BG)

    # Mountain FG
    offset_fg = (fi * 1) % 64
    for i in range(-1, W//64 + 2):
        bx = i * 64 - offset_fg
        draw.polygon([(bx, 55), (bx+32, 30), (bx+64, 55)], fill=MTN_FG)
        
    # Ground
    draw.rectangle([0, 50, W, H], fill=GROUND)
    
    # Trees
    offset_tree = (fi * 2) % 64
    for i in range(-1, W//64 + 2):
        bx = i * 64 - offset_tree
        tx, ty = bx + 32, 52
        draw.rectangle([tx-2, ty-5, tx+2, ty], fill=TREE_TRUNK)
        draw.polygon([(tx, ty-25), (tx-8, ty-10), (tx+8, ty-10)], fill=TREE_LEAVES)
        draw.polygon([(tx, ty-15), (tx-10, ty), (tx+10, ty)], fill=TREE_LEAVES)
        
    # Road
    draw.rectangle([0, 60, W, 76], fill=ROAD)
    
    # Road lines
    offset_road = (fi * 4) % 64
    for i in range(-1, W//64 + 2):
        bx = i * 64 - offset_road
        draw.rectangle([bx, 67, bx+24, 69], fill=ROAD_LINE)
        
    # Character centered
    cx, cy = W//2 - 15, 41
    cycle = (fi // 2) % 4 
    bob = 1 if cycle % 2 != 0 else 0
    
    # Head
    draw.rectangle([cx+12, cy+4+bob, cx+18, cy+11+bob], fill=SKIN)
    draw.rectangle([cx+11, cy+3+bob, cx+19, cy+5+bob], fill=HAIR)
    draw.rectangle([cx+11, cy+5+bob, cx+13, cy+7+bob], fill=HAIR)
    draw.rectangle([cx+18, cy+5+bob, cx+19, cy+8+bob], fill=HAIR)
    draw.point([cx+15, cy+7+bob], fill=GLASSES)
    draw.point([cx+17, cy+7+bob], fill=GLASSES)
    draw.line([cx+15, cy+7+bob, cx+17, cy+7+bob], fill=GLASSES)
    
    # Body
    draw.rectangle([cx+13, cy+12+bob, cx+17, cy+19+bob], fill=SHIRT)
    
    # Arms
    if cycle == 0 or cycle == 2:
        draw.rectangle([cx+11, cy+13+bob, cx+12, cy+17+bob], fill=SHIRT)
        draw.rectangle([cx+11, cy+18+bob, cx+12, cy+18+bob], fill=SKIN)
        draw.rectangle([cx+18, cy+13+bob, cx+19, cy+17+bob], fill=SHIRT)
        draw.rectangle([cx+18, cy+18+bob, cx+19, cy+18+bob], fill=SKIN)
    elif cycle == 1:
        draw.rectangle([cx+18, cy+13+bob, cx+20, cy+15+bob], fill=SHIRT)
        draw.rectangle([cx+20, cy+16+bob, cx+21, cy+17+bob], fill=SHIRT)
        draw.rectangle([cx+21, cy+17+bob, cx+21, cy+18+bob], fill=SKIN)
        draw.rectangle([cx+10, cy+13+bob, cx+12, cy+15+bob], fill=SHIRT)
        draw.rectangle([cx+9, cy+15+bob, cx+10, cy+16+bob], fill=SHIRT)
        draw.rectangle([cx+9, cy+17+bob, cx+9, cy+17+bob], fill=SKIN)
    elif cycle == 3:
        draw.rectangle([cx+10, cy+13+bob, cx+12, cy+15+bob], fill=SHIRT)
        draw.rectangle([cx+9, cy+15+bob, cx+10, cy+16+bob], fill=SHIRT)
        draw.rectangle([cx+9, cy+17+bob, cx+9, cy+17+bob], fill=SKIN)
        draw.rectangle([cx+18, cy+13+bob, cx+20, cy+15+bob], fill=SHIRT)
        draw.rectangle([cx+20, cy+16+bob, cx+21, cy+17+bob], fill=SHIRT)
        draw.rectangle([cx+21, cy+17+bob, cx+21, cy+18+bob], fill=SKIN)

    # Legs
    if cycle == 0 or cycle == 2:
        draw.rectangle([cx+13, cy+20+bob, cx+14, cy+25], fill=PANTS)
        draw.rectangle([cx+16, cy+20+bob, cx+17, cy+25], fill=PANTS)
        draw.rectangle([cx+12, cy+25, cx+14, cy+26], fill=SHOES)
        draw.rectangle([cx+16, cy+25, cx+18, cy+26], fill=SHOES)
    elif cycle == 1:
        draw.rectangle([cx+13, cy+20+bob, cx+14, cy+24], fill=PANTS)
        draw.rectangle([cx+13, cy+24, cx+15, cy+25], fill=SHOES)
        draw.rectangle([cx+16, cy+20+bob, cx+17, cy+22], fill=PANTS)
        draw.rectangle([cx+17, cy+22, cx+18, cy+23], fill=SHOES)
    elif cycle == 3:
        draw.rectangle([cx+16, cy+20+bob, cx+17, cy+24], fill=PANTS)
        draw.rectangle([cx+16, cy+24, cx+18, cy+25], fill=SHOES)
        draw.rectangle([cx+13, cy+20+bob, cx+14, cy+22], fill=PANTS)
        draw.rectangle([cx+12, cy+22, cx+13, cy+23], fill=SHOES)

    img = img.resize((W * scale, H * scale), PIL.Image.NEAREST)
    frames.append(img)

frames[0].save(
    "banner-retro.gif",
    save_all=True,
    append_images=frames[1:],
    duration=60,
    loop=0,
    transparency=0,
    disposal=2
)
print("Generated banner-retro.gif successfully!")
