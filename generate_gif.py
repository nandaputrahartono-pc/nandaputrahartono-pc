import PIL.Image
import PIL.ImageDraw

# Image dimensions
pixel_size = 8
w, h = 32, 32

# Colors
TRANSPARENT = (0, 0, 0, 0)
SKIN = (255, 204, 153, 255)
HAIR = (50, 30, 20, 255)
SHIRT = (41, 128, 185, 255)  # blue
PANTS = (44, 62, 80, 255)    # dark blue/gray
SHOES = (20, 20, 20, 255)
GLASSES = (200, 200, 200, 255)

frames = []

for frame_index in range(4):
    img = PIL.Image.new("RGBA", (w, h), TRANSPARENT)
    draw = PIL.ImageDraw.Draw(img)
    
    # Calculate head bobbing
    bob = 1 if frame_index % 2 != 0 else 0
    
    # --- HEAD ---
    # Face
    draw.rectangle([12, 4 + bob, 18, 11 + bob], fill=SKIN)
    # Hair
    draw.rectangle([11, 3 + bob, 19, 5 + bob], fill=HAIR)
    draw.rectangle([11, 5 + bob, 13, 7 + bob], fill=HAIR)
    draw.rectangle([18, 5 + bob, 19, 8 + bob], fill=HAIR)
    # Glasses
    draw.point([15, 7 + bob], fill=GLASSES)
    draw.point([17, 7 + bob], fill=GLASSES)
    draw.line([15, 7 + bob, 17, 7 + bob], fill=GLASSES)
    
    # --- BODY ---
    # Torso
    draw.rectangle([13, 12 + bob, 17, 19 + bob], fill=SHIRT)
    
    # --- ARMS ---
    if frame_index == 0: # Standing
        # Right arm (back)
        draw.rectangle([11, 13 + bob, 12, 17 + bob], fill=SHIRT)
        draw.rectangle([11, 18 + bob, 12, 18 + bob], fill=SKIN)
        # Left arm (front)
        draw.rectangle([18, 13 + bob, 19, 17 + bob], fill=SHIRT)
        draw.rectangle([18, 18 + bob, 19, 18 + bob], fill=SKIN)
    elif frame_index == 1: # Step right
        # Right arm swings forward
        draw.rectangle([18, 13 + bob, 20, 15 + bob], fill=SHIRT)
        draw.rectangle([20, 16 + bob, 21, 17 + bob], fill=SHIRT)
        draw.rectangle([21, 17 + bob, 21, 18 + bob], fill=SKIN)
        # Left arm swings back
        draw.rectangle([10, 13 + bob, 12, 15 + bob], fill=SHIRT)
        draw.rectangle([9, 15 + bob, 10, 16 + bob], fill=SHIRT)
        draw.rectangle([9, 17 + bob, 9, 17 + bob], fill=SKIN)
    elif frame_index == 2: # Standing
        # Right arm
        draw.rectangle([11, 13 + bob, 12, 17 + bob], fill=SHIRT)
        draw.rectangle([11, 18 + bob, 12, 18 + bob], fill=SKIN)
        # Left arm
        draw.rectangle([18, 13 + bob, 19, 17 + bob], fill=SHIRT)
        draw.rectangle([18, 18 + bob, 19, 18 + bob], fill=SKIN)
    elif frame_index == 3: # Step left
        # Right arm swings back
        draw.rectangle([10, 13 + bob, 12, 15 + bob], fill=SHIRT)
        draw.rectangle([9, 15 + bob, 10, 16 + bob], fill=SHIRT)
        draw.rectangle([9, 17 + bob, 9, 17 + bob], fill=SKIN)
        # Left arm swings forward
        draw.rectangle([18, 13 + bob, 20, 15 + bob], fill=SHIRT)
        draw.rectangle([20, 16 + bob, 21, 17 + bob], fill=SHIRT)
        draw.rectangle([21, 17 + bob, 21, 18 + bob], fill=SKIN)
        
    # --- LEGS ---
    if frame_index == 0:
        # Stand
        draw.rectangle([13, 20 + bob, 14, 25], fill=PANTS)
        draw.rectangle([16, 20 + bob, 17, 25], fill=PANTS)
        draw.rectangle([12, 25, 14, 26], fill=SHOES)
        draw.rectangle([16, 25, 18, 26], fill=SHOES)
    elif frame_index == 1:
        # Right leg up, left leg straight
        draw.rectangle([13, 20 + bob, 14, 24], fill=PANTS)
        draw.rectangle([13, 24, 15, 25], fill=SHOES)
        
        draw.rectangle([16, 20 + bob, 17, 22], fill=PANTS)
        draw.rectangle([17, 22, 18, 23], fill=SHOES)
    elif frame_index == 2:
        # Stand
        draw.rectangle([13, 20 + bob, 14, 25], fill=PANTS)
        draw.rectangle([16, 20 + bob, 17, 25], fill=PANTS)
        draw.rectangle([13, 25, 15, 26], fill=SHOES)
        draw.rectangle([16, 25, 18, 26], fill=SHOES)
    elif frame_index == 3:
        # Left leg up, right leg straight
        draw.rectangle([16, 20 + bob, 17, 24], fill=PANTS)
        draw.rectangle([16, 24, 18, 25], fill=SHOES)
        
        draw.rectangle([13, 20 + bob, 14, 22], fill=PANTS)
        draw.rectangle([12, 22, 13, 23], fill=SHOES)

    # Scale up using nearest neighbor for crisp pixel look
    img = img.resize((w * pixel_size, h * pixel_size), PIL.Image.NEAREST)
    frames.append(img)

# Save the GIF
frames[0].save(
    "walking-character.gif",
    save_all=True,
    append_images=frames[1:],
    duration=250, # ms per frame
    loop=0,
    transparency=0,
    disposal=2
)
print("Generated walking-character.gif successfully!")
