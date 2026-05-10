import PIL.Image
import PIL.ImageDraw
import random

W, H = 256, 80
scale = 3
N = 256 # 256 frames for very long loop to space out events

# Colors
SKY = (15, 15, 35, 255)
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
    
    # Mountain BG (Speed 0.5 -> Dist 128)
    offset_bg = int(fi * 0.5) % 128
    for i in range(-1, W//32 + 5):
        bx = i * 32 - offset_bg
        draw.polygon([(bx, 50), (bx+16, 25), (bx+32, 50)], fill=MTN_BG)

    # Mountain FG (Speed 1 -> Dist 256)
    offset_fg = (fi * 1) % 256
    for i in range(-1, W//64 + 5):
        bx = i * 64 - offset_fg
        draw.polygon([(bx, 55), (bx+32, 30), (bx+64, 55)], fill=MTN_FG)
        
    # Ground
    draw.rectangle([0, 50, W, H], fill=GROUND)
    
    # Trees & Random Ground Objects (Speed 2 -> Dist 512)
    offset_ground = (fi * 2) % 512
    for i in range(-1, W//512 + 2):
        bx = i * 512 - offset_ground
        
        # --- Trees ---
        for t_off in [30, 150, 280, 400]:
            tx, ty = bx + t_off, 52
            draw.rectangle([tx-2, ty-5, tx+2, ty], fill=TREE_TRUNK)
            draw.polygon([(tx, ty-25), (tx-8, ty-10), (tx+8, ty-10)], fill=TREE_LEAVES)
            draw.polygon([(tx, ty-15), (tx-10, ty), (tx+10, ty)], fill=TREE_LEAVES)
            
        # --- Camping Tent ---
        tx = bx + 80
        ty = 53
        draw.polygon([(tx, ty), (tx-10, ty+7), (tx+10, ty+7)], fill=(200, 50, 50, 255)) # tent body
        draw.polygon([(tx, ty), (tx-4, ty+7), (tx+4, ty+7)], fill=(150, 30, 30, 255)) # tent door
        # Campfire
        draw.polygon([(tx+15, ty+7), (tx+12, ty+4), (tx+18, ty+4)], fill=(255, 100, 0, 255))
        if fi % 4 < 2:
            draw.point([tx+15, ty+3], fill=(255, 200, 0, 255))
            
        # --- Broken Car (on the grass/shoulder) ---
        cx = bx + 250
        cy = 53
        draw.rectangle([cx, cy, cx+20, cy+6], fill=(50, 100, 200, 255)) # body
        draw.rectangle([cx+4, cy-4, cx+16, cy], fill=(50, 100, 200, 255)) # top
        draw.rectangle([cx+5, cy-3, cx+9, cy], fill=(150, 200, 255, 255)) # windows
        draw.rectangle([cx+11, cy-3, cx+15, cy], fill=(150, 200, 255, 255))
        draw.rectangle([cx+3, cy+5, cx+6, cy+8], fill=(20, 20, 20, 255)) # wheels
        draw.rectangle([cx+14, cy+5, cx+17, cy+8], fill=(20, 20, 20, 255))
        if fi % 2 == 0:
            draw.ellipse([cx-4, cy-4, cx, cy], fill=(150, 150, 150, 150))
            draw.ellipse([cx-8, cy-8, cx-2, cy-2], fill=(100, 100, 100, 100))
            
        # --- Sleeping Tiger ---
        tx_cat = bx + 420
        ty_cat = 57
        draw.rectangle([tx_cat, ty_cat, tx_cat+8, ty_cat+3], fill=(230, 120, 0, 255)) # body
        draw.rectangle([tx_cat+7, ty_cat+1, tx_cat+10, ty_cat+3], fill=(230, 120, 0, 255)) # head
        draw.line([tx_cat+1, ty_cat, tx_cat+1, ty_cat+2], fill=(0, 0, 0, 255)) # stripes
        draw.line([tx_cat+4, ty_cat, tx_cat+4, ty_cat+2], fill=(0, 0, 0, 255))
        if fi % 16 < 8:
            draw.point([tx_cat+11, ty_cat-2], fill=(255, 255, 255, 255))
            draw.point([tx_cat+12, ty_cat-3], fill=(255, 255, 255, 255))
            draw.point([tx_cat+13, ty_cat-4], fill=(255, 255, 255, 255))

    # --- Ghost ---
    # Floating around. Speed 3 -> Dist 768
    offset_ghost = (fi * 3) % 768
    for i in range(-1, W//768 + 2):
        gx = i * 768 + 500 - offset_ghost
        # Float up and down
        gy = 25 + int(3 * __import__('math').sin(fi * 0.2))
        
        # Draw ghost
        draw.ellipse([gx, gy, gx+10, gy+10], fill=(255, 255, 255, 200))
        draw.rectangle([gx, gy+5, gx+10, gy+12], fill=(255, 255, 255, 200))
        # Tail
        draw.polygon([(gx, gy+12), (gx+2, gy+10), (gx+4, gy+12)], fill=(255, 255, 255, 200))
        draw.polygon([(gx+3, gy+12), (gx+5, gy+10), (gx+7, gy+12)], fill=(255, 255, 255, 200))
        draw.polygon([(gx+6, gy+12), (gx+8, gy+10), (gx+10, gy+12)], fill=(255, 255, 255, 200))
        # Eyes
        draw.point([gx+2, gy+4], fill=(0, 0, 0, 255))
        draw.point([gx+6, gy+4], fill=(0, 0, 0, 255))
        
    # Road
    draw.rectangle([0, 60, W, 76], fill=ROAD)
    
    # Road markings (Speed 4 -> Dist 1024)
    offset_road = (fi * 4) % 1024
    for i in range(-1, W//1024 + 2):
        bx = i * 1024 - offset_road
        
        # Road lines
        for l in range(0, 1024, 64):
            draw.rectangle([bx+l, 67, bx+l+24, 69], fill=ROAD_LINE)
            
        # --- Mice Chasing ---
        mx1 = bx + 600
        my = 72
        mx2 = mx1 + 12 
        
        # Mouse 1
        draw.rectangle([mx1, my, mx1+4, my+2], fill=(150, 150, 150, 255))
        draw.point([mx1-1, my+1], fill=(150, 150, 150, 255)) 
        draw.line([mx1+4, my, mx1+6, my-1], fill=(150, 150, 150, 255)) 
        # Mouse 2
        draw.rectangle([mx2, my, mx2+4, my+2], fill=(100, 100, 100, 255))
        draw.point([mx2-1, my+1], fill=(100, 100, 100, 255))
        draw.line([mx2+4, my, mx2+6, my-1], fill=(100, 100, 100, 255))
        
        # animate legs
        if fi % 4 < 2:
            my -= 1
            
    # --- Birds ---
    # Speed 3 -> Dist 768
    offset_bird = (fi * 3) % 768
    for i in range(-1, W//768 + 2):
        bx = i * 768 + 300 - offset_bird
        by = 15 + int(4 * __import__('math').sin(fi * 0.1))
        
        # draw a flock of 3 birds
        for flock_off_x, flock_off_y in [(0, 0), (12, -4), (16, 6)]:
            bird_x = bx + flock_off_x
            bird_y = by + flock_off_y
            
            # Wing flapping
            if fi % 4 < 2:
                # wings up
                draw.polygon([(bird_x, bird_y), (bird_x+2, bird_y+1), (bird_x+4, bird_y)], fill=(0, 0, 0, 255))
                draw.point([bird_x+1, bird_y-1], fill=(0, 0, 0, 255))
                draw.point([bird_x+3, bird_y-1], fill=(0, 0, 0, 255))
            else:
                # wings down
                draw.polygon([(bird_x, bird_y), (bird_x+2, bird_y-1), (bird_x+4, bird_y)], fill=(0, 0, 0, 255))
                draw.point([bird_x+1, bird_y+1], fill=(0, 0, 0, 255))
                draw.point([bird_x+3, bird_y+1], fill=(0, 0, 0, 255))
        
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
