import sys
import importlib
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import feedparser
import webbrowser
import json
import os
import time
from datetime import datetime, timedelta
import csv

# --- Dependency Installation ---
def install_and_import(package):
    import_name = package.split('.')[0]
    try:
        importlib.import_module(import_name)
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            messagebox.showerror("Installation Error", f"Failed to install {package}. Install manually.")
            return None
    finally:
        globals()[import_name] = importlib.import_module(import_name)

install_and_import('feedparser')
install_and_import('tkhtmlview')

# --- Theme ---
try:
    from win95_theme import (
        WIN95_GRAY, WIN95_BLUE, WIN95_FONT, WIN95_FONT_BOLD,
        WIN95_SYSTEM_FONT_BOLD, set_win95_style
    )
except ImportError:
    messagebox.showerror("Theme Error", "missing win95_theme.py")
    WIN95_GRAY = '#C0C0C0'
    WIN95_BLUE = '#000080'
    WIN95_FONT = ('Arial', 10)
    WIN95_FONT_BOLD = ('Arial', 10, 'bold')
    WIN95_SYSTEM_FONT_BOLD = ('System', 11, 'bold')
    def set_win95_style(): pass

# --- File Path ---
FEED_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "feeds.json")

# --- Persistence ---
def load_feeds():
    if os.path.exists(FEED_FILE):
        try:
            with open(FEED_FILE, "r") as file:
                data = json.load(file)
                if isinstance(data, dict) and "feeds" in data:
                    return data["feeds"]
                if isinstance(data, list):
                    return data
        except json.JSONDecodeError:
            return []
    return []

def save_feeds():
    with open(FEED_FILE, "w") as file:
        json.dump({"feeds": FEED_URLS}, file, indent=2)

# --- Export CSV ---
def export_feeds_as_csv():
    if not FEED_URLS:
        messagebox.showinfo("No Feeds", "No feeds to export.")
        return
    csv_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "feeds.csv")
    try:
        with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Feed URL"])
            for feed in FEED_URLS:
                writer.writerow([feed])
        messagebox.showinfo("Export Successful", f"Exported to:\n{csv_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"{e}")

# --- Import CSV ---
def import_feeds_from_csv():
    try:
        csv_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not csv_path:
            return

        imported = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                url = row[0].strip()
                if url and url not in FEED_URLS:
                    imported.append(url)

        if imported:
            FEED_URLS.extend(imported)
            save_feeds()
            update_feed_list()
            messagebox.showinfo("Import Complete", f"Imported {len(imported)} feeds.")
        else:
            messagebox.showinfo("No New Feeds", "No new URLs found.")

    except Exception as e:
        messagebox.showerror("Import Error", f"{e}")

# --- Globals ---
FEED_URLS = load_feeds()

# --- Core Functions ---
def open_link(url):
    webbrowser.open_new(url)

def open_content_window(content):
    content_window = tk.Toplevel(root)
    content_window.title("Feed Content")
    content_window.geometry("800x600")
    content_window.state('zoomed')

    html_frame = tkhtmlview.HTMLScrolledText(content_window, background="white")
    html_frame.pack(pady=10, padx=10, fill="both", expand=True)

    html_with_meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">' + content
    html_frame.set_html(html_with_meta)

def fetch_feeds():
    for widget in feed_frame.winfo_children():
        widget.destroy()

    all_entries = []
    one_month_ago = time.mktime((datetime.now() - timedelta(days=30)).timetuple())

    for url in FEED_URLS:
        feed = feedparser.parse(url)
        source = feed.feed.get("title", "Unknown Source")
        entries = feed.entries[:3]
        for entry in entries:
            entry_time = entry.get("published_parsed")
            if entry_time and time.mktime(entry_time) < one_month_ago:
                continue
            all_entries.append((entry, source, url))

    all_entries.sort(key=lambda x: x[0].get("published_parsed", ()), reverse=True)
    all_entries = all_entries[:50]

    for entry, source, feed_url in all_entries:
        entry_frame = tk.Frame(feed_frame, bd=2, relief=tk.GROOVE, bg=WIN95_GRAY)
        entry_frame.pack(fill="x", pady=5, padx=5)

        entry_title = entry.get("title", "No title")
        title_label = tk.Label(entry_frame, text=f"{source}: {entry_title}",
                               font=("Arial", 12, "bold"),
                               fg="black", bg=WIN95_GRAY,
                               anchor="w", justify="left", wraplength=1000)
        title_label.pack(fill="x", padx=5, pady=(5, 0))

        date_str = entry.get('published', 'No date')
        date_label = tk.Label(entry_frame, text=f"Published: {date_str}",
                              font=("Arial", 10, "italic"),
                              anchor="w", bg=WIN95_GRAY)
        date_label.pack(fill="x", padx=5)

        btn_frame = tk.Frame(entry_frame, bg=WIN95_GRAY)
        btn_frame.pack(fill="x", pady=5, padx=5)

        link_button = tk.Button(btn_frame, text="View Online",
                                 command=lambda url=entry.link: open_link(url),
                                 bg=WIN95_GRAY, fg="black", relief=tk.RAISED, bd=3,
                                 font=WIN95_FONT)
        link_button.pack(side="left", padx=(0, 5))

        def copy_to_clipboard(url=entry.link):
            root.clipboard_clear()
            root.clipboard_append(url)
            messagebox.showinfo("Copied", f"Copied:\n{url}")

        copy_button = tk.Button(btn_frame, text="Copy Link",
                                 command=copy_to_clipboard,
                                 bg=WIN95_GRAY, fg="black", relief=tk.RAISED, bd=3,
                                 font=WIN95_FONT)
        copy_button.pack(side="left", padx=(0, 5))

        content = entry.get('summary', entry.get('description', 'No content'))
        read_button = tk.Button(btn_frame, text="Read Here",
                                 command=lambda c=content: open_content_window(c),
                                 bg=WIN95_GRAY, fg="black", relief=tk.RAISED, bd=3,
                                 font=WIN95_FONT)
        read_button.pack(side="left", padx=(0, 5))

        def remove_this_feed(url=feed_url):
            if url in FEED_URLS:
                FEED_URLS.remove(url)
                save_feeds()
                fetch_feeds()
                update_feed_list()

        remove_button = tk.Button(btn_frame, text="Remove Feed",
                                   command=remove_this_feed,
                                   fg="red", bg=WIN95_GRAY,
                                   relief=tk.RAISED, bd=3, font=WIN95_FONT)
        remove_button.pack(side="left")

def add_feed():
    url = url_entry.get().strip()
    if url:
        if url not in FEED_URLS:
            FEED_URLS.append(url)
            save_feeds()
            update_feed_list()
            url_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Info", "Already exists.")
    else:
        messagebox.showerror("Input Error", "Enter a valid URL.")

def add_youtube_channel_feed():
    channel_id = url_entry.get().strip()
    if channel_id:
        full_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        if full_url not in FEED_URLS:
            FEED_URLS.append(full_url)
            save_feeds()
            update_feed_list()
            url_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Info", "Already exists.")
    else:
        messagebox.showerror("Input Error", "Enter a valid channel ID.")

def remove_feed():
    selection = feed_listbox.curselection()
    if selection:
        index = selection[0]
        del FEED_URLS[index]
        save_feeds()
        update_feed_list()

def update_feed_list():
    feed_listbox.delete(0, tk.END)
    for feed_url in FEED_URLS:
        feed_listbox.insert(tk.END, feed_url)

def auto_refresh():
    fetch_feeds()
    root.after(900000, auto_refresh)

def on_close():
    root.destroy()

# --- GUI ---
root = tk.Tk()
root.title("Integrated RSS Reader")
root.geometry("900x700")
root.protocol("WM_DELETE_WINDOW", on_close)

set_win95_style()
root.config(bg=WIN95_GRAY)

# --- Notebook ---
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=5, pady=5)

feed_tab = ttk.Frame(notebook)
settings_tab = ttk.Frame(notebook)
import_tab = ttk.Frame(notebook)

notebook.add(feed_tab, text="Feeds")
notebook.add(settings_tab, text="Settings")
notebook.add(import_tab, text="Import / Export")

# --- Feeds Tab ---
main_controls_frame = ttk.Frame(feed_tab)
main_controls_frame.pack(fill='x', pady=5)

fetch_button = ttk.Button(main_controls_frame, text="Refresh Feeds", command=fetch_feeds)
fetch_button.pack()

feed_canvas_frame = ttk.Frame(feed_tab)
feed_canvas_frame.pack(fill="both", expand=True)

feed_canvas = tk.Canvas(feed_canvas_frame, bg=WIN95_GRAY)
feed_scrollbar = ttk.Scrollbar(feed_canvas_frame, orient="vertical", command=feed_canvas.yview)
feed_canvas.configure(yscrollcommand=feed_scrollbar.set)

feed_scrollbar.pack(side="right", fill="y")
feed_canvas.pack(side="left", fill="both", expand=True)

feed_frame = ttk.Frame(feed_canvas)
feed_frame_id = feed_canvas.create_window((0, 0), window=feed_frame, anchor="nw")

def resize_feed_frame(event):
    canvas_width = event.width
    feed_canvas.itemconfig(feed_frame_id, width=canvas_width)

def update_scrollregion(event):
    feed_canvas.configure(scrollregion=feed_canvas.bbox("all"))

feed_frame.bind("<Configure>", update_scrollregion)
feed_canvas.bind("<Configure>", resize_feed_frame)

def _on_mousewheel(event):
    if sys.platform == "win32":
        feed_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    else:
        feed_canvas.yview_scroll(int(event.delta), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)

# --- Settings Tab ---
settings_frame = ttk.Frame(settings_tab, padding="10")
settings_frame.pack(fill="both", expand=True)

url_label = ttk.Label(settings_frame, text="Enter RSS Feed URL or YouTube Channel ID:")
url_label.pack(pady=(0, 5))

url_entry = ttk.Entry(settings_frame, width=80)
url_entry.pack(fill='x', expand=True, pady=5)

button_frame = ttk.Frame(settings_frame)
button_frame.pack(fill='x', pady=5)

add_button = ttk.Button(button_frame, text="Add RSS Feed", command=add_feed)
add_button.pack(side="left", padx=(0, 5))

youtube_button = ttk.Button(button_frame, text="Add YouTube Feed", command=add_youtube_channel_feed)
youtube_button.pack(side="left")

list_frame = ttk.Frame(settings_frame)
list_frame.pack(fill='both', expand=True, pady=10)

listbox_border_frame = tk.Frame(list_frame, bg='black', relief=tk.SUNKEN, bd=2)
listbox_border_frame.pack(side="left", fill='both', expand=True)

feed_listbox = tk.Listbox(listbox_border_frame, height=15, bd=0, font=WIN95_FONT)
feed_listbox.pack(side="left", fill='both', expand=True, padx=1, pady=1)

list_scrollbar = ttk.Scrollbar(listbox_border_frame, orient="vertical", command=feed_listbox.yview)
list_scrollbar.pack(side="right", fill="y")
feed_listbox.config(yscrollcommand=list_scrollbar.set)

remove_button = ttk.Button(settings_frame, text="Remove Selected Feed", command=remove_feed)
remove_button.pack(pady=5)

# --- Import / Export Tab ---
import_export_frame = ttk.Frame(import_tab, padding="10")
import_export_frame.pack(fill="both", expand=True)

import_button = ttk.Button(import_export_frame, text="Import Feeds from CSV", command=import_feeds_from_csv)
import_button.pack(pady=10)

export_button = ttk.Button(import_export_frame, text="Export Feeds as CSV", command=export_feeds_as_csv)
export_button.pack(pady=10)

# --- Init ---
update_feed_list()
fetch_feeds()
auto_refresh()

root.mainloop()
