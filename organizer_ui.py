from organizer_core import organize_folder, remove_ansii, categories
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading

class DunkenOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dunken Organizer")
        self.resizable(False, False)
        self.configure(bg="#1e1e1f")
        self.geometry(self._center_geometry(640, 380))

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._setup_styles()
        self.selected_folder = tk.StringVar(value="No folder selected")
        self._build_ui()

    def _center_geometry(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        return f"{w}x{h}+{x}+{y}"

    def _setup_styles(self):
        bg = "#1e1e1f"
        panel = "#26229"
        accent = "#00c2ff"
        btn_bg = "#2b2b2e"
        btn_fg = "#e6e6e6"
        text_fg = "#d9d9d9"

        self.style.configure("TFrame", background=panel)
        self.style.configure("TLabel", background=panel, foreground=text_fg, font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=accent)
        self.style.configure("TButton", background=btn_bg, foreground=btn_fg, relief="flat")
        self.style.map("TButton",
                       background=[("active", "#333336")])

        self.style.configure("Primary.TButton", background=accent, foreground="#0b0b0b", font=("Segoe UI", 10, "bold"))
        self.style.map("Primary.TButton", background=[("active", "#00b8f0")])
    def _build_ui(self):
        padding = 12
        main = ttk.Frame(self, padding=padding)
        main.pack(fill="both", expand=True)

        # Title
        ttk.Label(main, text="Dunken Organizer", style="Title.TLabel").pack(anchor="w", pady=(0,8))

        # folder select row
        row = ttk.Frame(main)
        row.pack(fill="x", pady=(0,10))

        self.folder_label = ttk.Label(row, textvariable=self.selected_folder, width=58)
        self.folder_label.pack(side="left", padx=(0,8))

        select_btn = ttk.Button(row, text="Select Folder", command=self.select_folder)
        select_btn.pack(side="left")

        # organize button
        self.organize_btn = ttk.Button(main, text="Organize Files", style="Primary.TButton", command=self.organize_clicked, state="disabled")
        self.organize_btn.pack(fill="x", pady=(6,10))

        # status / log box
        ttk.Label(main, text="Status / Log:").pack(anchor="w")
        self.log = scrolledtext.ScrolledText(main, height=10, bg="#171718", fg="#e6e6e6", insertbackground="#e6e6e6")
        self.log.pack(fill="both", expand=True, pady=(6,0))

        # footer
        footer = ttk.Frame(main)
        footer.pack(fill="x", pady=(8,0))
        ttk.Label(footer, text="Tip: Files are organized only in the selected folder (non-recursive).").pack(side="left")
        ttk.Label(footer, text=" ").pack(side="right")

        # initial message
        self.log_insert("Welcome to Dunken Organizer — select a folder to begin.\n")

    def log_insert(self, msg: str):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to organize")
        if folder:
            self.selected_folder.set(folder)
            self.organize_btn.config(state="normal")
            self.log_insert(f"Folder selected: {folder}")

    def organize_clicked(self):
        folder = self.selected_folder.get()
        if not folder or folder == "No folder selected":
            messagebox.showwarning("No folder", "Please select a folder first.")
            return
        # disable buttons while working
        self.organize_btn.config(state="disabled")
        self.log_insert("Organizing... please wait.")
        # run in background thread
        thread = threading.Thread(target=self._run_organize_thread, args=(folder,), daemon=True)
        thread.start()

    def _run_organize_thread(self, folder):
        def logger(msg):
            msg = remove_ansii(msg)
            # schedule UI updates on main thread
            self.after(0, lambda m=msg: self.log_insert(m))
        organize_folder(folder, logger)
        # re-enable button on main thread
        self.after(0, lambda: self.organize_btn.config(state="normal"))

