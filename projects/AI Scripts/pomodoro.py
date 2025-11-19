import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import ctypes
import pygame

# -----------------------
# Windows API setup
# -----------------------
user32 = ctypes.windll.user32
SW_RESTORE = 9

def force_foreground(hwnd):
    try:
        user32.ShowWindow(hwnd, SW_RESTORE)
        user32.SetForegroundWindow(hwnd)
    except:
        pass

# -----------------------
# Audio setup
# -----------------------
pygame.mixer.init()

def play_audio_loop(file, volume=1.0):
    try:
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume)
        sound.play(loops=-1)
        return sound
    except:
        print(f"Error playing {file}")
        return None

def play_audio_once(file, volume=1.0):
    try:
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume)
        sound.play()
        return sound
    except:
        print(f"Error playing {file}")
        return None

def stop_audio(sound):
    if sound:
        sound.stop()

# -----------------------
# Progress Bar
# -----------------------
class Win95ProgressBar(tk.Canvas):
    def __init__(self, master, width=300, height=22, **kw):
        super().__init__(master, width=width, height=height, bg="#C0C0C0",
                         highlightthickness=2, highlightbackground="#808080", **kw)
        self.width = width
        self.height = height
        self.progress = 0.0

    def set(self, fraction):
        self.progress = max(0.0, min(1.0, fraction))
        self._draw()

    def _draw(self):
        self.delete("all")
        bar_w = int(self.width * self.progress)
        block_w = 12
        for x in range(0, bar_w, block_w):
            self.create_rectangle(x, 0, x + block_w - 2, self.height,
                                  fill="#0000A8", outline="#000080")

# -----------------------
# Timer logic
# -----------------------
def run_single_timer(ui, seconds, label_text):
    remaining = seconds
    ui.phase_label.config(text=label_text)

    # Start looping audios
    s1 = play_audio_loop(ui.audio1, ui.audio1_volume.get()/100) if ui.audio1 else None
    s2 = play_audio_loop(ui.audio2, ui.audio2_volume.get()/100) if ui.audio2 else None

    while remaining >= 0 and not ui.stop_flag:
        if s1:
            s1.set_volume(ui.audio1_volume.get()/100)
        if s2:
            s2.set_volume(ui.audio2_volume.get()/100)

        m = remaining // 60
        s = remaining % 60
        ui.time_label.config(text=f"{m:02d}:{s:02d}")
        fraction = 1 - (remaining / seconds)
        ui.bar.set(fraction)
        time.sleep(1)
        remaining -= 1

    stop_audio(s1)
    stop_audio(s2)

    # Only bring to front and play end audio if timer completed naturally
    if not ui.stop_flag:
        ui.bring_to_front()
        if ui.end_audio:
            play_audio_once(ui.end_audio, ui.end_audio_volume.get()/100)

def run_pomodoro_cycles(ui, work_min, break_min, cycles):
    ui.points = 0
    ui.points_label.config(text="Points: 0")
    for c in range(cycles):
        if ui.stop_flag:
            break
        run_single_timer(ui, work_min * 60, f"Work [{c+1}/{cycles}]")
        if ui.stop_flag:
            break
        run_single_timer(ui, break_min * 60, f"Break [{c+1}/{cycles}]")
        ui.points += 1
        ui.points_label.config(text=f"Points: {ui.points}")
    ui.phase_label.config(text="Stopped" if ui.stop_flag else "Done")

# -----------------------
# UI
# -----------------------
class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro Audio Timer")
        self.root.configure(bg="#C0C0C0")
        self.hwnd = self.root.winfo_id()
        self.points = 0
        self.stop_flag = False

        self.audio1 = None
        self.audio2 = None
        self.end_audio = None
        self.audio1_volume = tk.IntVar(value=100)
        self.audio2_volume = tk.IntVar(value=100)
        self.end_audio_volume = tk.IntVar(value=100)

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(expand=True, fill="both")

        # Timer tab
        self.tab_timer = tk.Frame(self.nb, bg="#C0C0C0")
        self.nb.add(self.tab_timer, text="Timer")
        self.build_timer_tab(self.tab_timer)

        # Audio tab
        self.tab_audio = tk.Frame(self.nb, bg="#C0C0C0")
        self.nb.add(self.tab_audio, text="Audio")
        self.build_audio_tab(self.tab_audio)

    def bring_to_front(self):
        force_foreground(self.hwnd)

    def build_timer_tab(self, frame):
        self.phase_label = tk.Label(frame, text="Idle", font=("Arial", 12, "bold"), bg="#C0C0C0")
        self.phase_label.pack(pady=5)

        self.points_label = tk.Label(frame, text="Points: 0", font=("Arial", 12, "bold"), bg="#C0C0C0")
        self.points_label.pack(pady=5)

        # Work input
        row = tk.Frame(frame, bg="#C0C0C0"); row.pack(pady=2)
        tk.Label(row, text="Work (min):", bg="#C0C0C0").pack(side="left")
        self.work_entry = tk.Entry(row, width=5)
        self.work_entry.insert(0, "25")
        self.work_entry.pack(side="left")

        # Break input
        row2 = tk.Frame(frame, bg="#C0C0C0"); row2.pack(pady=2)
        tk.Label(row2, text="Break (min):", bg="#C0C0C0").pack(side="left")
        self.break_entry = tk.Entry(row2, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.pack(side="left")

        # Cycles input
        row3 = tk.Frame(frame, bg="#C0C0C0"); row3.pack(pady=2)
        tk.Label(row3, text="Cycles:", bg="#C0C0C0").pack(side="left")
        self.cycle_entry = tk.Entry(row3, width=5)
        self.cycle_entry.insert(0, "1")
        self.cycle_entry.pack(side="left")

        # Time display
        self.time_label = tk.Label(frame, text="00:00", font=("Arial", 20, "bold"), bg="#C0C0C0")
        self.time_label.pack(pady=10)

        # Progress bar
        self.bar = Win95ProgressBar(frame)
        self.bar.pack(pady=10)

        # Start and Stop buttons
        button_row = tk.Frame(frame, bg="#C0C0C0"); button_row.pack(pady=5)
        tk.Button(button_row, text="Start", command=self.start, bg="#C0C0C0").pack(side="left", padx=5)
        tk.Button(button_row, text="Stop", command=self.stop, bg="#C0C0C0").pack(side="left", padx=5)

    def build_audio_tab(self, frame):
        # Audio 1
        tk.Button(frame, text="Select Audio 1", command=self.select_audio1, bg="#C0C0C0").pack(pady=2)
        tk.Label(frame, text="Volume 1", bg="#C0C0C0").pack()
        tk.Scale(frame, variable=self.audio1_volume, from_=0, to=100, orient="horizontal", bg="#C0C0C0").pack(pady=2)

        # Audio 2
        tk.Button(frame, text="Select Audio 2", command=self.select_audio2, bg="#C0C0C0").pack(pady=2)
        tk.Label(frame, text="Volume 2", bg="#C0C0C0").pack()
        tk.Scale(frame, variable=self.audio2_volume, from_=0, to=100, orient="horizontal", bg="#C0C0C0").pack(pady=2)

        # End audio
        tk.Button(frame, text="Select End Audio", command=self.select_end_audio, bg="#C0C0C0").pack(pady=2)
        tk.Label(frame, text="End Volume", bg="#C0C0C0").pack()
        tk.Scale(frame, variable=self.end_audio_volume, from_=0, to=100, orient="horizontal", bg="#C0C0C0").pack(pady=2)

    def select_audio1(self):
        self.audio1 = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])

    def select_audio2(self):
        self.audio2 = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])

    def select_end_audio(self):
        self.end_audio = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])

    def start(self):
        try:
            w = int(self.work_entry.get())
            b = int(self.break_entry.get())
            c = int(self.cycle_entry.get())
        except:
            self.phase_label.config(text="Invalid Input")
            return
        self.stop_flag = False
        t = threading.Thread(target=run_pomodoro_cycles, args=(self, w, b, c))
        t.daemon = True
        t.start()

    def stop(self):
        self.stop_flag = True

def main():
    ui = UI()
    ui.root.mainloop()

if __name__ == "__main__":
    main()
