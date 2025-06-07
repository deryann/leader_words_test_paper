import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from run import _main

def run_gui():
    def generate_file(print_file=False):
        selected_folder = folder_var.get()
        if not selected_folder:
            messagebox.showerror("Error", "Please select a folder")
            return
        filepath, ans_filepath = _main(selected_folder)
        if print_file:
            os.startfile(filepath, "print")

    root = tk.Tk()
    root.title("Word Test Paper Generator")

    folder_var = tk.StringVar()
    folder_label = ttk.Label(root, text="Select Folder:")
    folder_label.pack(pady=5)
    folder_dropdown = ttk.Combobox(root, textvariable=folder_var)
    folder_dropdown.pack(pady=5)

    cfg_folder = os.path.join(os.getcwd(), "cfg")
    folders = [f for f in os.listdir(cfg_folder) if f.endswith(".json")]
    folder_dropdown["values"] = folders

    generate_button = ttk.Button(root, text="Generate File", command=lambda: generate_file(print_file=False))
    generate_button.pack(pady=5)

    generate_print_button = ttk.Button(root, text="Generate and Print", command=lambda: generate_file(print_file=True))
    generate_print_button.pack(pady=5)

    root.mainloop()
