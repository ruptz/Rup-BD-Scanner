import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import sv_ttk
import pywinstyles
import sys

# Define the keywords to search for
keywords = [
    "os.execute",
    "PerformHttpRequest",
    r"\\x[0-9A-Fa-f]{2}"  # Matches binary strings like \x50
]

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def scan_files():
    results = []
    line_info = []
    root_dir = folder_entry.get()
    
    if not os.path.exists(root_dir):
        messagebox.showerror("Error", "Folder path does not exist.")
        return
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".lua"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_number, line in enumerate(file, start=1):
                        for keyword in keywords:
                            if re.search(keyword, line):
                                results.append(f"Found '{keyword}' in '{file_path}' on line {line_number}")
                                line_info.append(f"{file_path} (Line {line_number}):\n{line.strip()}\n")  # Added new line for spacing

    # Display results
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, f"{len(results)} results found:\n\n")
    
    for result in results:
        results_text.insert(tk.END, result + "\n\n")  # Added spacing between results

    line_text.delete(1.0, tk.END)
    for info in line_info:
        line_text.insert(tk.END, info + "\n")  # Added spacing for line info

    if not results:
        results_text.insert(tk.END, "No suspicious activities found.\n")

def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

# Create the main window
root = tk.Tk()
root.title("Rup-Scripts Backdoor Scanner")
root.geometry("1200x700")  # Increased size for better visibility

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1200
window_height = 700
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Apply the Sun Valley theme
sv_ttk.set_theme("dark")

# Folder selection
folder_label = ttk.Label(root, text="Folder Path:", font=('Arial', 16, 'bold'))
folder_label.pack(pady=10)

folder_frame = ttk.Frame(root)
folder_frame.pack(pady=5)

folder_entry = ttk.Entry(folder_frame, width=60, font=('Arial', 12))
folder_entry.pack(side=tk.LEFT, padx=5, pady=5)

choose_button = ttk.Button(folder_frame, text="Choose Folder", command=choose_folder, style='Accent.TButton')
choose_button.pack(side=tk.LEFT, padx=5, pady=5)

scan_button = ttk.Button(root, text="Scan", command=scan_files, style='Accent.TButton', width=20)
scan_button.pack(pady=20)

# Results text area
results_label = ttk.Label(root, text="Scan Results:", font=('Arial', 16, 'bold'))
results_label.pack(pady=5)

results_frame = ttk.Frame(root)
results_frame.pack(pady=5)

# Darker background for results text area
results_text = scrolledtext.ScrolledText(results_frame, width=110, height=15, wrap=tk.WORD, font=('Arial', 12), bg='#111111', fg='white')
results_text.pack(padx=5, pady=5)

# Line info text area
line_label = ttk.Label(root, text="Line Info:", font=('Arial', 16, 'bold'))
line_label.pack(pady=5)

line_frame = ttk.Frame(root)
line_frame.pack(pady=5)

# Darker background for line info text area
line_text = scrolledtext.ScrolledText(line_frame, width=110, height=7, wrap=tk.WORD, font=('Arial', 12), bg='#111111', fg='white')
line_text.pack(padx=5, pady=5)

# Apply the theme to the title bar
apply_theme_to_titlebar(root)

# Run the application
root.mainloop()