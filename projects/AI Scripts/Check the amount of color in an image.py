import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
from PIL import Image, ImageTk
import numpy as np

# --- Utility Functions ---
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_mask_rgb(image, target_color, tolerance):
    img_array = np.array(image)
    r, g, b = hex_to_rgb(target_color)
    target_rgb = np.array([r, g, b])
    diff = np.linalg.norm(img_array - target_rgb, axis=-1)
    mask = diff <= tolerance
    return mask

def calculate_color_percentage(mask):
    return np.sum(mask) / mask.size * 100

def overlay_mask(image, mask):
    overlay = np.array(image).copy()
    overlay[mask] = [255, 0, 0]  # Highlight matching regions in red
    return Image.fromarray(overlay)

# --- Core Update Function ---
def update_images():
    if not img_path:
        return
    color = color_entry.get()
    tolerance = tolerance_scale.get()
    try:
        image = Image.open(img_path).convert('RGB')
        mask = calculate_mask_rgb(image, color, tolerance)
        percent = calculate_color_percentage(mask)
        overlay = overlay_mask(image, mask)

        # Resize for display
        display_img = image.copy()
        display_img.thumbnail((350, 350))
        overlay.thumbnail((350, 350))

        tk_img_orig = ImageTk.PhotoImage(display_img)
        tk_img_overlay = ImageTk.PhotoImage(overlay)

        img_label_orig.config(image=tk_img_orig)
        img_label_orig.image = tk_img_orig

        img_label_overlay.config(image=tk_img_overlay)
        img_label_overlay.image = tk_img_overlay

        result_label.config(text=f"Match: {percent:.2f}% within ±{tolerance}")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# --- File and Color Selection ---
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        global img_path
        img_path = file_path
        update_images()

def pick_color():
    color_code = colorchooser.askcolor(title="Choose target color")[1]
    if color_code:
        color_entry.delete(0, tk.END)
        color_entry.insert(0, color_code)
        update_images()

# --- GUI Setup ---
root = tk.Tk()
root.title("Accurate Color Coverage Visualizer (RGB Mode)")

img_path = None

frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)

# Buttons
ttk.Button(frame, text="Open Image", command=open_image).grid(row=0, column=0, sticky='w')
ttk.Button(frame, text="Pick Color", command=pick_color).grid(row=0, column=1, sticky='w')

# Color entry
ttk.Label(frame, text="Target Color (#HEX):").grid(row=1, column=0, sticky='w')
color_entry = ttk.Entry(frame)
color_entry.insert(0, "#ffffff")
color_entry.grid(row=1, column=1, sticky='ew')

# Tolerance slider
ttk.Label(frame, text="Tolerance:").grid(row=2, column=0, sticky='w')
tolerance_scale = tk.Scale(frame, from_=0, to=255, orient='horizontal', command=lambda _: update_images())
tolerance_scale.set(30)
tolerance_scale.grid(row=2, column=1, sticky='ew')

# Results
result_label = ttk.Label(frame, text="No image loaded yet.")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Image display
images_frame = ttk.Frame(frame)
images_frame.grid(row=4, column=0, columnspan=2, pady=5)

img_label_orig = ttk.Label(images_frame)
img_label_orig.grid(row=0, column=0, padx=5)

img_label_overlay = ttk.Label(images_frame)
img_label_overlay.grid(row=0, column=1, padx=5)

frame.columnconfigure(1, weight=1)

root.mainloop()
