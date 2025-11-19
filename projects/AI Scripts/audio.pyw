import sys
import subprocess

# --- Dependency check before any other imports ---
required = ['pygame', 'tkinter']
missing = []

for module in required:
    try:
        __import__(module)
    except ImportError:
        missing.append(module)

# If dependencies missing, show a Tkinter dialog to offer install
if missing:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()  # Hide main window

    msg = "The following required modules are missing:\n\n"
    msg += "\n".join(missing)
    msg += "\n\nWould you like to install them now?"

    if messagebox.askyesno("Missing Dependencies", msg):
        for module in missing:
            try:
                print(f"Installing {module}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except Exception as e:
                messagebox.showerror("Installation Failed", f"Could not install {module}:\n{e}")
                sys.exit(1)

        messagebox.showinfo("Restart Required", "Dependencies installed successfully.\nRestarting...")
        root.destroy()
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)
    else:
        messagebox.showwarning("Missing Dependencies", "Cannot run without installing required modules.")
        sys.exit(1)

# --- Normal imports after dependency verification ---
import tkinter as tk
from tkinter import filedialog
import pygame

# Win95 theming
WIN95_GRAY = '#C0C0C0'
WIN95_FONT = ('Arial', 10)
WIN95_FONT_BOLD = ('Arial', 10, 'bold')

# Initialize Pygame mixer
try:
    pygame.mixer.init()
except Exception as e:
    import tkinter.messagebox as messagebox
    messagebox.showerror("Audio Initialization Failed", f"Error initializing pygame mixer:\n{e}")
    sys.exit(1)

# Globals
sound1 = None
sound2 = None
channel1 = None
channel2 = None

def load_file1():
    global sound1
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file:
        sound1 = pygame.mixer.Sound(file)
        if channel1 and channel1.get_busy():
            channel1.stop()
        status_label.config(text="File 1 loaded")

def load_file2():
    global sound2
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file:
        sound2 = pygame.mixer.Sound(file)
        if channel2 and channel2.get_busy():
            channel2.stop()
        status_label.config(text="File 2 loaded")

def play_audio():
    global channel1, channel2
    if sound1:
        sound1.set_volume(vol1_slider.get())
        channel1 = sound1.play(loops=-1)
    if sound2:
        sound2.set_volume(vol2_slider.get())
        channel2 = sound2.play(loops=-1)
    status_label.config(text="Playing both files")

def stop_audio():
    if channel1:
        channel1.stop()
    if channel2:
        channel2.stop()
    status_label.config(text="Stopped")

def update_volume1(val):
    if sound1:
        sound1.set_volume(float(val))

def update_volume2(val):
    if sound2:
        sound2.set_volume(float(val))

# GUI
root = tk.Tk()
root.title("Win95 Dual Audio Player with Sliders")
root.configure(bg=WIN95_GRAY)

def make_win95_button(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, font=WIN95_FONT_BOLD,
                    bg=WIN95_GRAY, relief="raised", bd=2, activebackground=WIN95_GRAY,
                    activeforeground="black", highlightthickness=0)
    btn.pack(pady=2, fill='x')
    return btn

main_frame = tk.Frame(root, bg=WIN95_GRAY, padx=10, pady=10)
main_frame.pack()

# Load buttons
load_button1 = make_win95_button(main_frame, "Load File 1", load_file1)
load_button2 = make_win95_button(main_frame, "Load File 2", load_file2)

# Play/Stop buttons
play_button = make_win95_button(main_frame, "Play Both", play_audio)
stop_button = make_win95_button(main_frame, "Stop", stop_audio)

# Frame for sound1 controls
frame1 = tk.Frame(root, bg=WIN95_GRAY)
frame1.pack(pady=10, fill='x')

tk.Label(frame1, text="Sound 1 Volume:", bg=WIN95_GRAY, font=WIN95_FONT).pack(anchor='w', pady=2)
vol1_slider = tk.Scale(frame1, from_=0, to=1, resolution=0.01,
                       orient='horizontal', length=200, command=update_volume1, bg=WIN95_GRAY)
vol1_slider.set(1.0)
vol1_slider.pack(fill='x', pady=2)

# Frame for sound2 controls
frame2 = tk.Frame(root, bg=WIN95_GRAY)
frame2.pack(pady=10, fill='x')

tk.Label(frame2, text="Sound 2 Volume:", bg=WIN95_GRAY, font=WIN95_FONT).pack(anchor='w', pady=2)
vol2_slider = tk.Scale(frame2, from_=0, to=1, resolution=0.01,
                       orient='horizontal', length=200, command=update_volume2, bg=WIN95_GRAY)
vol2_slider.set(1.0)
vol2_slider.pack(fill='x', pady=2)

# Status label
status_label = tk.Label(main_frame, text="No files loaded", bg=WIN95_GRAY,
                        font=WIN95_FONT, relief="sunken", bd=2, anchor='w')
status_label.pack(pady=5, fill='x')

root.mainloop()
