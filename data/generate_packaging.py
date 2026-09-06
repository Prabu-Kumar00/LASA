import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Add workspace directory to path to import medicine_catalog
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.medicine_catalog import CATALOG, Medicine

def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    font_names = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"] if bold else ["segoui.ttf", "arial.ttf", "calibri.ttf"]
    for name in font_names:
        try:
            path = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Fonts", name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        except Exception:
            continue
    try:
        # Pillow >= 10.1.0 supports size for load_default
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()

def draw_rectangular_carton(draw: ImageDraw.ImageDraw, med: Medicine, w: int, h: int):
    # Base carton background (medicine color)
    draw.rectangle([20, 20, w - 20, h - 20], fill=med.color, outline="#333333", width=3)
    
    # White label area for high contrast text
    draw.rectangle([35, 75, w - 35, h - 75], fill="#FFFFFF", outline="#DDDDDD", width=1)
    
    # Medicine Name (bold, dominant color)
    font_name = get_font(24, bold=True)
    draw.text((50, 90), med.name, fill=med.color, font=font_name)
    
    # Strength and Form
    font_sub = get_font(16, bold=False)
    draw.text((50, 130), f"{med.strength} | {med.form}", fill="#333333", font=font_sub)
    
    # Shelf Location
    font_shelf = get_font(12, bold=True)
    draw.rectangle([50, 170, 110, 195], fill="#E5E7EB", outline="#9CA3AF")
    draw.text((58, 175), f"Loc: {med.shelf}", fill="#1F2937", font=font_shelf)
    
    # Cold Chain Badge
    if med.cold_chain:
        draw.rectangle([w - 180, 170, w - 50, 195], fill="#DBEAFE", outline="#3B82F6")
        draw.text((w - 170, 175), "* 2-8°C REFRIGERATED", fill="#1E40AF", font=get_font(11, bold=True))

def draw_vial(draw: ImageDraw.ImageDraw, med: Medicine, w: int, h: int):
    # Silver cap
    draw.rectangle([w//2 - 50, 20, w//2 + 50, 45], fill="#9CA3AF", outline="#4B5563", width=2)
    draw.rectangle([w//2 - 40, 45, w//2 + 40, 75], fill="#D1D5DB", outline="#4B5563", width=2)
    
    # Glass vial body (translucent grey/amber look)
    draw.rectangle([w//2 - 80, 75, w//2 + 80, h - 35], fill="#F3F4F6", outline="#4B5563", width=3)
    # Bottom curvature
    draw.chord([w//2 - 80, h - 55, w//2 + 80, h - 15], 0, 180, fill="#E5E7EB", outline="#4B5563", width=3)
    
    # Fluid representation (half full, in medicine color)
    draw.rectangle([w//2 - 77, 180, w//2 + 77, h - 35], fill=med.color)
    draw.chord([w//2 - 77, h - 55, w//2 + 77, h - 18], 0, 180, fill=med.color)
    
    # Vial Label
    label_top = 95
    label_bottom = 175
    draw.rectangle([w//2 - 77, label_top, w//2 + 77, label_bottom], fill="#FFFFFF", outline="#CCCCCC", width=1)
    
    # Brand line on label in medicine color
    draw.rectangle([w//2 - 77, label_top, w//2 + 77, label_top + 10], fill=med.color)
    
    # Texts on label
    draw.text((w//2 - 70, label_top + 15), med.name, fill="#111827", font=get_font(16, bold=True))
    draw.text((w//2 - 70, label_top + 38), med.strength, fill="#4B5563", font=get_font(13, bold=True))
    draw.text((w//2 - 70, label_top + 55), med.form, fill="#6B7280", font=get_font(11, bold=False))
    
    # Shelf Location
    draw.rectangle([w//2 - 70, label_bottom - 20, w//2 - 20, label_bottom - 5], fill="#F3F4F6")
    draw.text((w//2 - 68, label_bottom - 18), med.shelf, fill="#374151", font=get_font(10, bold=True))
    
    # Cold Chain badge on label
    if med.cold_chain:
        draw.rectangle([w//2 - 10, label_bottom - 20, w//2 + 70, label_bottom - 5], fill="#DBEAFE")
        draw.text((w//2 - 6, label_bottom - 18), "2-8°C COLD", fill="#1D4ED8", font=get_font(9, bold=True))

def draw_pen_carton(draw: ImageDraw.ImageDraw, med: Medicine, w: int, h: int):
    # Slim pen-carton layout (long and slender)
    draw.rectangle([20, 60, w - 20, h - 60], fill=med.color, outline="#333333", width=3)
    
    # Decorative stripes / modern medical pattern on the left
    draw.polygon([(20, 60), (80, 60), (50, h - 60), (20, h - 60)], fill="#FFFFFF")
    draw.polygon([(85, 60), (120, 60), (90, h - 60), (55, h - 60)], fill="#D1D5DB")
    
    # White background panel for text on the right
    draw.rectangle([135, 75, w - 35, h - 75], fill="#FFFFFF", outline="#E5E7EB", width=1)
    
    # Texts
    draw.text((150, 85), med.name, fill=med.color, font=get_font(20, bold=True))
    draw.text((150, 115), f"{med.strength} | {med.form}", fill="#374151", font=get_font(14, bold=True))
    
    # Shelf & Cold Chain
    draw.text((150, 140), f"Loc: {med.shelf}", fill="#6B7280", font=get_font(11, bold=True))
    if med.cold_chain:
        draw.rectangle([w - 140, 137, w - 45, 155], fill="#EFF6FF", outline="#3B82F6")
        draw.text((w - 132, 140), "COLD: 2-8°C", fill="#1D4ED8", font=get_font(9, bold=True))

def draw_blister(draw: ImageDraw.ImageDraw, med: Medicine, w: int, h: int):
    # Blister card background (metallic light grey)
    draw.rectangle([20, 20, w - 20, h - 20], fill="#E5E7EB", outline="#9CA3AF", width=3)
    
    # Draw a grid of 6 rounded foil pill cavities (bubbles)
    cols, rows = 3, 2
    cavity_w, cavity_h = 70, 45
    start_x, start_y = 40, 130
    
    for r in range(rows):
        for c in range(cols):
            x1 = start_x + c * (cavity_w + 30)
            y1 = start_y + r * (cavity_h + 15)
            # Oval pocket
            draw.ellipse([x1, y1, x1 + cavity_w, y1 + cavity_h], fill="#D1D5DB", outline="#9CA3AF", width=2)
            # Highlight to make it look 3D
            draw.ellipse([x1 + 5, y1 + 5, x1 + cavity_w - 20, y1 + cavity_h - 15], fill="#F3F4F6")
            
    # Text Banner on top (representing colored printing on foil)
    draw.rectangle([20, 20, w - 20, 110], fill=med.color)
    
    # Print on foil
    draw.text((40, 32), med.name, fill="#FFFFFF", font=get_font(22, bold=True))
    draw.text((40, 68), f"{med.strength} | {med.form}", fill="#F3F4F6", font=get_font(14, bold=False))
    
    # Location
    draw.rectangle([w - 110, 65, w - 40, 85], fill="#FFFFFF", outline="#CCCCCC")
    draw.text((w - 100, 68), f"Loc: {med.shelf}", fill="#374151", font=get_font(10, bold=True))
    
    # Blisters are non-refrigerated in our dataset, but draw cold chain if it were true
    if med.cold_chain:
        draw.rectangle([w - 110, 32, w - 40, 52], fill="#DBEAFE")
        draw.text((w - 104, 36), "COLD 2-8°", fill="#1E40AF", font=get_font(9, bold=True))

def generate_packaging_image(med: Medicine, output_path: str):
    # Canvas Size
    w, h = 400, 300
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.ImageDraw(img)
    
    # Draw packaging shape
    if med.pack_shape == "rectangular carton":
        draw_rectangular_carton(draw, med, w, h)
    elif med.pack_shape == "vial":
        draw_vial(draw, med, w, h)
    elif med.pack_shape == "pen carton":
        draw_pen_carton(draw, med, w, h)
    elif med.pack_shape == "blister":
        draw_blister(draw, med, w, h)
    else:
        # Default fallback rectangular carton
        draw_rectangular_carton(draw, med, w, h)
        
    # Draw SKU and NDC simulation at the bottom of the canvas
    # Background strip for details
    draw.rectangle([20, h - 25, w - 20, h - 5], fill="#1F2937")
    
    font_bot = get_font(10, bold=False)
    # Monospaced SKU / Barcode text
    details_str = f"SKU: {med.sku}     NDC (Bar): [{med.ndc_sim}]"
    draw.text((30, h - 22), details_str, fill="#F9FAFB", font=font_bot)
    
    # Save Image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated packaging image for {med.sku} at {output_path}")

def main():
    # Targets app/static/packaging
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "app", "static", "packaging")
    
    print("Generating synthetic packaging images...")
    for med in CATALOG:
        output_path = os.path.join(target_dir, f"{med.sku}.png")
        generate_packaging_image(med, output_path)
    print("All packaging images generated successfully!")

if __name__ == "__main__":
    main()
