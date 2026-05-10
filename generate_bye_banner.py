import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import random
import math

W, H = 128, 64
scale = 6
N = 32

SKY = (15, 10, 30, 255)

# Char Colors
SKIN = (255, 204, 153, 255)
HAIR = (50, 30, 20, 255)
SHIRT = (41, 128, 185, 255)
PANTS = (44, 62, 80, 255)
SHOES = (20, 20, 20, 255)
GLASSES = (200, 200, 200, 255)
BUBBLE = (255, 255, 255, 255)
TEXT = (0, 0, 0, 255)

random.seed(42)
fireworks = []
for _ in range(15):
    fx = random.randint(10, W-10)
    fy = random.randint(5, 30)
    color = (random.randint(150, 255), random.randint(100, 255), random.randint(150, 255), 255)
    start_time = random.randint(0, N-1)
    duration = random.randint(10, 20)
    fireworks.append({
        'x': fx, 'y': fy, 'color': color,
        'start': start_time, 'duration': duration,
        'type': random.choice([0, 1])
    })

frames = []

try:
    font = PIL.ImageFont.load_default()
except:
    font = None

for fi in range(N):
    img = PIL.Image.new("RGBA", (W, H), SKY)
    draw = PIL.ImageDraw.Draw(img)
    
    # City silhouette
    draw.rectangle([0, H-12, W, H], fill=(5, 5, 10, 255))
    for bx in range(0, W, 15):
        bh = random.Random(bx).randint(10, 25)
        draw.rectangle([bx, H-bh, bx+12, H], fill=(10, 10, 15, 255))
        
        # Add a few random lit windows
        if bh > 15:
            wx = bx + 2
            wy = H - bh + 4
            if random.Random(bx+fi//8).random() > 0.5: # twinkling lights
                draw.rectangle([wx, wy, wx+2, wy+2], fill=(200, 200, 100, 255))
    
    # Fireworks
    for fw in fireworks:
        age = (fi - fw['start']) % N
        if age < fw['duration']:
            progress = age / fw['duration']
            radius = progress * 15
            num_particles = 8 if fw['type'] == 0 else 12
            
            # Simple alpha blending manually to avoid PIL issues
            alpha = 1.0 - progress
            # Mix firework color with sky color based on alpha
            r = int(fw['color'][0] * alpha + SKY[0] * (1-alpha))
            g = int(fw['color'][1] * alpha + SKY[1] * (1-alpha))
            b = int(fw['color'][2] * alpha + SKY[2] * (1-alpha))
            c = (r, g, b, 255)
            
            for i in range(num_particles):
                angle = i * (2 * math.pi / num_particles)
                px = fw['x'] + math.cos(angle) * radius
                py = fw['y'] + math.sin(angle) * radius
                py += progress * 8 # gravity
                
                if 0 <= px < W and 0 <= py < H:
                    draw.point([px, py], fill=c)
                    if fw['type'] == 1 and progress < 0.5:
                        draw.point([px+1, py], fill=c)
                        draw.point([px, py+1], fill=c)

    cx = W // 2 - 16
    cy = H - 28 
    
    # Head
    draw.rectangle([cx+12, cy+4, cx+18, cy+11], fill=SKIN)
    draw.rectangle([cx+11, cy+3, cx+19, cy+5], fill=HAIR)
    draw.rectangle([cx+11, cy+5, cx+13, cy+7], fill=HAIR)
    draw.rectangle([cx+18, cy+5, cx+19, cy+8], fill=HAIR)
    draw.point([cx+15, cy+7], fill=GLASSES)
    draw.point([cx+17, cy+7], fill=GLASSES)
    draw.line([cx+15, cy+7, cx+17, cy+7], fill=GLASSES)
    
    # Body
    draw.rectangle([cx+13, cy+12, cx+17, cy+19], fill=SHIRT)
    
    # Left Arm
    draw.rectangle([cx+11, cy+13, cx+12, cy+17], fill=SHIRT)
    draw.rectangle([cx+11, cy+18, cx+12, cy+18], fill=SKIN)
    
    # Waving Right Arm
    wave_frame = (fi // 2) % 4 
    if wave_frame == 0:
        draw.rectangle([cx+18, cy+12, cx+19, cy+14], fill=SHIRT)
        draw.rectangle([cx+20, cy+10, cx+21, cy+12], fill=SHIRT)
        draw.rectangle([cx+22, cy+8, cx+23, cy+9], fill=SKIN)
    elif wave_frame == 1:
        draw.rectangle([cx+18, cy+12, cx+19, cy+14], fill=SHIRT)
        draw.rectangle([cx+19, cy+9, cx+20, cy+11], fill=SHIRT)
        draw.rectangle([cx+20, cy+7, cx+21, cy+8], fill=SKIN)
    elif wave_frame == 2:
        draw.rectangle([cx+18, cy+12, cx+19, cy+14], fill=SHIRT)
        draw.rectangle([cx+18, cy+9, cx+19, cy+11], fill=SHIRT)
        draw.rectangle([cx+17, cy+7, cx+18, cy+8], fill=SKIN)
    elif wave_frame == 3:
        draw.rectangle([cx+18, cy+12, cx+19, cy+14], fill=SHIRT)
        draw.rectangle([cx+19, cy+9, cx+20, cy+11], fill=SHIRT)
        draw.rectangle([cx+20, cy+7, cx+21, cy+8], fill=SKIN)

    # Legs
    draw.rectangle([cx+13, cy+20, cx+14, cy+25], fill=PANTS)
    draw.rectangle([cx+16, cy+20, cx+17, cy+25], fill=PANTS)
    draw.rectangle([cx+12, cy+25, cx+14, cy+26], fill=SHOES)
    draw.rectangle([cx+16, cy+25, cx+18, cy+26], fill=SHOES)
    
    # Speech Bubble
    bubble_y = cy - 14 if (fi // 4) % 2 == 0 else cy - 13
    
    draw.rectangle([cx-6, bubble_y, cx+42, bubble_y+13], fill=BUBBLE, outline=TEXT)
    
    draw.polygon([(cx+14, bubble_y+13), (cx+18, bubble_y+13), (cx+16, bubble_y+17)], fill=BUBBLE)
    draw.line([(cx+14, bubble_y+13), (cx+16, bubble_y+17)], fill=TEXT)
    draw.line([(cx+16, bubble_y+17), (cx+18, bubble_y+13)], fill=TEXT)
    draw.line([(cx+15, bubble_y+13), (cx+17, bubble_y+13)], fill=BUBBLE)
    
    if font:
        draw.text((cx-1, bubble_y+1), "Bye bye!", font=font, fill=TEXT)
    else:
        draw.text((cx-1, bubble_y+1), "Bye bye!", fill=TEXT)

    img = img.resize((W * scale, H * scale), PIL.Image.NEAREST)
    frames.append(img)

frames[0].save(
    "bye-bye-banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    transparency=0,
    disposal=2
)
print("Generated bye-bye-banner.gif successfully!")
