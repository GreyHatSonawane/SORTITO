#!/usr/bin/env python3
"""
SORTITO - Desktop File Organizer
Taskbar icon fixed - uses .ico for Windows, .png for others.
"""

import os
import sys
import shutil
import threading
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk

# ==================== File Type Definitions ====================
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v',
    '.mpg', '.mpeg', '.3gp', '.mts', '.m2ts', '.vob', '.ogv', '.ogg', '.ts'
}

PHOTO_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
    '.heic', '.heif', '.raw', '.cr2', '.nef', '.arw', '.dng', '.orf', '.rw2'
}

class SORTITOApp:
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("SORTITO - Media Sorter")
        self.root.geometry("920x700")
        self.root.minsize(800, 600)

        # Set taskbar / window icon (no corner image)
        self._set_icons()

        self.source_dir = ""
        self.copy_mode = False
        self.include_others = True
        self.is_running = False
        self.start_time = 0
        self.processed_count = 0
        self.total_files = 0

        self._create_widgets()
        self._center_window()

    def _set_icons(self):
        """Set icons for title bar and Windows taskbar."""
        # Determine base path (when frozen or running from source)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        # 1. Use iconphoto with PNG (works on title bar on all platforms)
        png_path = os.path.join(base_path, "logo.png")
        if os.path.exists(png_path):
            try:
                img = Image.open(png_path)
                img.thumbnail((64, 64), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, photo)
                self._icon_ref = photo  # prevent garbage collection
            except Exception as e:
                print(f"iconphoto error: {e}")

        # 2. For Windows taskbar, use iconbitmap with .ico (requires .ico file)
        if sys.platform == "win32":
            ico_path = os.path.join(base_path, "logo.ico")
            if os.path.exists(ico_path):
                try:
                    self.root.iconbitmap(ico_path)
                except Exception as e:
                    print(f"iconbitmap error: {e}")

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # Header (text only, no logo image)
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(title_box, text="SORTITO", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Desktop File Organizer", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w")

        self.theme_switch = ctk.CTkSwitch(header_frame, text="Dark Mode", command=self._toggle_theme, progress_color="blue")
        self.theme_switch.pack(side="right")
        self._update_theme_switch()

        ctk.CTkLabel(main_frame, text="Recursively organise videos and photos", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 20))

        # Folder selection card
        folder_card = ctk.CTkFrame(main_frame, corner_radius=12)
        folder_card.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(folder_card, text="Source Folder", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        folder_select = ctk.CTkFrame(folder_card, fg_color="transparent")
        folder_select.pack(fill="x", padx=15, pady=(0,10))
        self.folder_entry = ctk.CTkEntry(folder_select, placeholder_text="No folder selected", state="readonly", height=40)
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.browse_btn = ctk.CTkButton(folder_select, text="Browse", width=100, height=40, command=self._browse_folder)
        self.browse_btn.pack(side="right")

        # Options card
        options_card = ctk.CTkFrame(main_frame, corner_radius=12)
        options_card.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(options_card, text="Options", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        options_inner = ctk.CTkFrame(options_card, fg_color="transparent")
        options_inner.pack(fill="x", padx=15, pady=(0,10))
        self.copy_check = ctk.CTkCheckBox(options_inner, text="Copy files instead of moving (preserve originals)", command=self._set_copy_mode)
        self.copy_check.pack(anchor="w", pady=4)
        self.others_check = ctk.CTkCheckBox(options_inner, text="Create 'others' folder for non‑media files", command=self._set_include_others)
        self.others_check.select()
        self.others_check.pack(anchor="w", pady=4)

        # Action area
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0,15))
        self.start_btn = ctk.CTkButton(action_frame, text="Start Sorting", height=45, font=ctk.CTkFont(size=14, weight="bold"), command=self._start_sorting)
        self.start_btn.pack(side="left", padx=(0,15))
        self.progress = ctk.CTkProgressBar(action_frame, width=300, height=15)
        self.progress.set(0)
        self.progress.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.progress_label = ctk.CTkLabel(action_frame, text="0%", width=50)
        self.progress_label.pack(side="right")

        # Log card
        log_card = ctk.CTkFrame(main_frame, corner_radius=12)
        log_card.pack(fill="both", expand=True)
        ctk.CTkLabel(log_card, text="Activity Log", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        self.log_text = ctk.CTkTextbox(log_card, wrap="word", font=ctk.CTkFont(family="Consolas", size=10))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0,15))

        # Status bar
        self.status_var = ctk.StringVar(value="Ready")
        status_bar = ctk.CTkLabel(main_frame, textvariable=self.status_var, font=ctk.CTkFont(size=11), anchor="w")
        status_bar.pack(fill="x", pady=(10,0))

    # ------------------ Theme and Options ------------------
    def _toggle_theme(self):
        current = ctk.get_appearance_mode()
        new = "Dark" if current == "Light" else "Light"
        ctk.set_appearance_mode(new)
        self._update_theme_switch()

    def _update_theme_switch(self):
        is_dark = (ctk.get_appearance_mode() == "Dark")
        self.theme_switch.select() if is_dark else self.theme_switch.deselect()
        self.theme_switch.configure(text="Dark Mode" if not is_dark else "Light Mode")

    def _set_copy_mode(self):
        self.copy_mode = self.copy_check.get()

    def _set_include_others(self):
        self.include_others = self.others_check.get()

    def _browse_folder(self):
        if self.is_running:
            return
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_dir = folder
            self.folder_entry.configure(state="normal")
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.folder_entry.configure(state="readonly")

    def _log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update_idletasks()

    # ------------------ File Processing ------------------
    def _get_category(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix in VIDEO_EXTENSIONS:
            return 'video'
        elif suffix in PHOTO_EXTENSIONS:
            return 'photo'
        else:
            return 'other'

    def _get_unique_destination(self, dest_dir: Path, filename: str) -> Path:
        dest_path = dest_dir / filename
        if not dest_path.exists():
            return dest_path
        stem = dest_path.stem
        suffix = dest_path.suffix
        counter = 1
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = dest_dir / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def _move_file(self, file_path: Path, dest_dir: Path) -> bool:
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = self._get_unique_destination(dest_dir, file_path.name)
            if self.copy_mode:
                shutil.copy2(file_path, dest_path)
                op = "Copied"
            else:
                shutil.move(str(file_path), str(dest_path))
                op = "Moved"
            self._log(f"  {op}: {file_path.name} → {dest_dir.name}/")
            return True
        except Exception as e:
            self._log(f"  ERROR: {file_path.name} - {e}")
            return False

    def _is_within_dest_folders(self, file_path: Path, dest_folders: set) -> bool:
        for folder in dest_folders:
            if folder in file_path.parents:
                return True
        return False

    def _count_total_files(self, source_dir: Path, dest_folders: set) -> int:
        total = 0
        for file_path in source_dir.rglob('*'):
            if not file_path.is_file():
                continue
            if self._is_within_dest_folders(file_path, dest_folders):
                continue
            total += 1
        return total

    def _sort_media(self, source_dir: Path):
        videos_dir = source_dir / "videos"
        photos_dir = source_dir / "photos"
        others_dir = source_dir / "others" if self.include_others else None
        dest_folders = {videos_dir, photos_dir}
        if others_dir:
            dest_folders.add(others_dir)

        self.total_files = self._count_total_files(source_dir, dest_folders)
        if self.total_files == 0:
            self._log("No files to process (all files already sorted or empty folder).")
            return

        self._log(f"Found {self.total_files} files to process.")
        self._log("-" * 50)

        stats = {'video': 0, 'photo': 0, 'other': 0}
        self.processed_count = 0
        self.start_time = time.time()

        for file_path in source_dir.rglob('*'):
            if not self.is_running:
                self._log("\nOperation cancelled by user.")
                break
            if not file_path.is_file():
                continue
            if self._is_within_dest_folders(file_path, dest_folders):
                continue

            category = self._get_category(file_path)
            if category == 'video':
                if self._move_file(file_path, videos_dir):
                    stats['video'] += 1
            elif category == 'photo':
                if self._move_file(file_path, photos_dir):
                    stats['photo'] += 1
            elif self.include_others:
                if self._move_file(file_path, others_dir):
                    stats['other'] += 1
            else:
                self._log(f"  Skipped (other): {file_path.name}")

            self.processed_count += 1
            percent = (self.processed_count / self.total_files) * 100
            self.root.after(0, self._update_progress, percent)

            elapsed = time.time() - self.start_time
            if self.processed_count > 0:
                rate = self.processed_count / elapsed
                remaining_files = self.total_files - self.processed_count
                eta_seconds = remaining_files / rate if rate > 0 else 0
                eta_str = self._format_time(eta_seconds)
                status_msg = f"Processing... {percent:.1f}% | ETA: {eta_str}"
                self.root.after(0, lambda msg=status_msg: self.status_var.set(msg))

        self._log("-" * 50)
        self._log("Summary:")
        self._log(f"  Videos {'copied' if self.copy_mode else 'moved'}: {stats['video']}")
        self._log(f"  Photos {'copied' if self.copy_mode else 'moved'}: {stats['photo']}")
        if self.include_others:
            self._log(f"  Other files {'copied' if self.copy_mode else 'moved'}: {stats['other']}")
        self._log(f"  Total files processed: {self.processed_count}")
        self._log(f"\nOutput folders created in: {source_dir}")
        self._log("  - videos/")
        self._log("  - photos/")
        if self.include_others:
            self._log("  - others/")

    def _update_progress(self, percent):
        self.progress.set(percent / 100)
        self.progress_label.configure(text=f"{percent:.1f}%")

    def _format_time(self, seconds):
        if seconds < 0:
            return "0s"
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"

    def _sort_thread(self, source_dir: Path):
        try:
            self._sort_media(source_dir)
            if self.is_running:
                self.status_var.set("Completed successfully")
                messagebox.showinfo("Done", "Media sorting completed!")
            else:
                self.status_var.set("Cancelled")
        except Exception as e:
            self._log(f"Fatal error: {e}")
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            self.is_running = False
            self.start_btn.configure(state="normal", text="Start Sorting", command=self._start_sorting)
            self.browse_btn.configure(state="normal")
            self.progress.set(0)
            self.progress_label.configure(text="0%")
            if not self.is_running:
                self.status_var.set("Ready")

    def _start_sorting(self):
        if not self.source_dir:
            messagebox.showwarning("No Folder", "Please select a source folder first.")
            return
        source_path = Path(self.source_dir).resolve()
        if not source_path.exists() or not source_path.is_dir():
            messagebox.showerror("Invalid Folder", "The selected folder does not exist.")
            return

        self.log_text.delete("1.0", "end")
        self.is_running = True
        self.start_btn.configure(state="disabled", text="Cancel", command=self._cancel_sorting)
        self.browse_btn.configure(state="disabled")
        self.progress.set(0)
        self.progress_label.configure(text="0%")
        self.status_var.set("Counting files...")

        thread = threading.Thread(target=self._sort_thread, args=(source_path,), daemon=True)
        thread.start()

    def _cancel_sorting(self):
        if self.is_running:
            self.is_running = False
            self._log("\nCancelling... please wait.")
            self.start_btn.configure(state="disabled")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SORTITOApp()
    app.run()