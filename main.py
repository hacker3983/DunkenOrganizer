from organizer_core import *
from organizer_ui import *
import tkinter as tk
from tkinter import messagebox
import os
import platform

if platform.system() == "Windows":
    os.system("cls")

if __name__ == "__main__":
    if not categories:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Missing extensions.json", f"Could not find or parse {EXT_FILE}. Make sure it exists in the same folder as this script.")
        raise SystemExit(1)
    app = DunkenOrganizerApp()
    app.mainloop()
