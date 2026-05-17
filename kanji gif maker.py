import requests
import numpy as np
from svgpathtools import parse_path
from PIL import Image, ImageDraw
from xml.dom import minidom
import os

def generate_guided_smooth_kanji_gif(kanji_char, output_path):
    # 1. Fetch SVG
    hex_code = hex(ord(kanji_char))[2:].zfill(5)
    url = f"https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/{hex_code}.svg"
    response = requests.get(url)
    if response.status_code != 200:
        return print(f"Kanji {kanji_char} not found.")

    # 2. Parse Paths
    doc = minidom.parseString(response.content)
    path_strings = [p.getAttribute('d') for p in doc.getElementsByTagName('path')]
    doc.unlink()

    # --- ANIMATION SETTINGS (Tweaked for the Dot) ---
    STEPS_PER_STROKE = 12  # Increased to make the dot movement smoother
    FRAME_DURATION = 35    # Speeds up slightly because there are more frames
    PAUSE_AT_END = 2000    # Pause for 2 seconds on finished Kanji
    # ------------------------------------------------

    frames = []
    scale = 4 
    img_size = (109 * scale, 109 * scale)
    finished_strokes = []

    # COLORS (RGBA)
    COL_WHITE = (255, 255, 255, 255)
    COL_RED = (255, 0, 0, 255) # Guiding dot color
    COL_CLEAR = (0, 0, 0, 0)

    # 3. Incremental Drawing Loop
    for d in path_strings:
        path = parse_path(d)
        
        # Calculate all points for the total stroke once
        total_points_to_draw = []
        for segment in path:
            segment_points = [segment.point(t) for t in np.linspace(0, 1, 10)]
            total_points_to_draw.extend(segment_points)

        # Draw the current stroke incrementally
        for step in range(1, STEPS_PER_STROKE + 1):
            img = Image.new('RGBA', img_size, COL_CLEAR)
            draw = ImageDraw.Draw(img)
            
            # A. Draw all previously finished strokes (Background)
            for prev_d in finished_strokes:
                prev_path = parse_path(prev_d)
                for segment in prev_path:
                    # Drawing slightly faster points for finished strokes is okay
                    points = [segment.point(t) for t in np.linspace(0, 1, 6)]
                    coords = [(p.real * scale, p.imag * scale) for p in points]
                    draw.line(coords, fill=COL_WHITE, width=3*scale, joint='curve')

            # B. Draw current active stroke percentage
            current_progress = step / STEPS_PER_STROKE
            slice_idx = int(len(total_points_to_draw) * current_progress)
            active_points = total_points_to_draw[:max(2, slice_idx)]
            
            if len(active_points) >= 2:
                coords = [(p.real * scale, p.imag * scale) for p in active_points]
                draw.line(coords, fill=COL_WHITE, width=3*scale, joint='curve')

            # C. *** NEW: Calculate and Draw Guiding Red Dot ***
            if len(total_points_to_draw) > 0:
                # Find the 'pen tip' at this specific step
                idx = min(max(0, slice_idx - 1), len(total_points_to_draw) - 1)
                pen_tip = total_points_to_draw[idx]

                # Convert to canvas coordinates
                dot_x = pen_tip.real * scale
                dot_y = pen_tip.imag * scale
                
                # Dot size (adjust to taste)
                # Setting radius slightly larger than half stroke_width makes it visible
                dot_radius = 2.5 * scale 

                # Draw the ellipse centered on (dot_x, dot_y)
                draw.ellipse(
                    [
                        dot_x - dot_radius, dot_y - dot_radius,
                        dot_x + dot_radius, dot_y + dot_radius
                    ],
                    fill=COL_RED, # Interior color
                    outline=COL_RED # Exterior border
                )

            # D. Convert to Palette for Transparency
            alpha = img.split()[-1]
            img_p = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            img_p.paste(255, mask)
            frames.append(img_p)
            
        # Add current stroke to finished
        finished_strokes.append(d)

    # 4. Final Pause (The red dot is hidden here since the pen is 'lifted')
    # Create one final frame WITHOUT the dot
    img = Image.new('RGBA', img_size, COL_CLEAR)
    draw = ImageDraw.Draw(img)
    for fin_d in finished_strokes:
        fin_path = parse_path(fin_d)
        for segment in fin_path:
            points = [segment.point(t) for t in np.linspace(0, 1, 10)]
            coords = [(p.real * scale, p.imag * scale) for p in points]
            draw.line(coords, fill=COL_WHITE, width=3*scale, joint='curve')
    
    alpha = img.split()[-1]
    img_p = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    img_p.paste(255, mask)
    final_frame = img_p

    # Add the pause
    num_pause_frames = PAUSE_AT_END // FRAME_DURATION
    for _ in range(num_pause_frames):
        frames.append(final_frame)

    # 5. Save
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        transparency=255,
        disposal=2 
    )
    print(f"Success! Guided Transparent GIF created: {output_path}")

# --- CONFIG ---
TARGET_KANJI = "歩"
SAVE_DIRECTORY = r"C:\Users\Eshaan\OneDrive\Desktop\kanji_gif"
FILE_NAME = f"Day_111_{TARGET_KANJI}.gif"
FULL_SAVE_PATH = os.path.join(SAVE_DIRECTORY, FILE_NAME)

generate_guided_smooth_kanji_gif(TARGET_KANJI, FULL_SAVE_PATH)