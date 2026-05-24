# Features & Uses – SORTITO

## 🔧 Detailed Features

### 1. Recursive Scanning
Walks through every subfolder inside the chosen source directory – no limit on depth.

### 2. Smart Media Detection
Distinguishes videos from photos using a built‑in extensible set of file extensions.  
*(You can easily add or remove extensions in the source code.)*

### 3. Copy / Move Modes
- **Move mode** – files are relocated to the new folders (original locations cleared).  
- **Copy mode** – files are duplicated; originals remain untouched.  
Ideal for backing up media before reorganising.

### 4. Duplicate Filename Handling
If a file with the same name already exists in the destination folder, SORTITO appends `_1`, `_2`, etc. before the extension.  
Example: `video.mp4` becomes `video_1.mp4`, `video_2.mp4`, …

### 5. “Others” Folder (Optional)
When enabled, every file that is neither a video nor a photo is moved/copied into an `others/` folder.  
When disabled, non‑media files are skipped entirely.

### 6. Real‑time Progress & ETA
A progress bar shows the percentage completed.  
The status bar displays a dynamic estimate of remaining time (e.g., `Processing... 45.2% | ETA: 2m 12s`).

### 7. Dark / Light Theme
Switch between modern light and dark modes. The app follows your system preference by default.

### 8. Cancellable Operation
Click the **Cancel** button (same button changes from “Start Sorting” to “Cancel”) to safely stop the process at any point.

### 9. Clean Activity Log
Every file action (move/copy/skip) is logged in a scrollable text area, with errors highlighted.

### 10. Portable Executable
The Windows `.exe` is self‑contained – no Python, no dependencies to install. Just download and run.

## 📖 Typical Use Cases

| Use Case | How SORTITO Helps |
|----------|--------------------|
| **Clean up Downloads folder** | Move all downloaded videos and photos into dedicated folders instantly. |
| **Organise a camera SD card** | Extract only the media files (ignore system folders). |
| **Prepare media for backup** | Copy videos and photos to separate folders before backing up. |
| **Find all media on an old hard drive** | Recursively scan a whole drive, gather media in one place. |
| **Separate work files from personal media** | Run on a shared drive, then only share the `videos/` and `photos/` folders. |
| **Batch rename and sort by type** | Combine with other tools after sorting. |
| **Before deleting a messy folder** | First copy media out, then safely delete the rest. |

## 🎯 Tips & Tricks

- **Use copy mode** when experimenting – your original files stay safe.
- **Enable “others” folder** if you want to keep a complete archive of everything (not just media).
- **Run on a small test folder** first to understand the behaviour.
- **Dark mode** is easier on the eyes during long sorting jobs.
- **Cancel anytime** – the tool finishes the current file then stops cleanly.

## 🧩 Extensibility

Developers can easily:
- Add new video/photo extensions in the `VIDEO_EXTENSIONS` / `PHOTO_EXTENSIONS` sets.
- Change the destination folder names (`videos`, `photos`, `others`).
- Modify the GUI layout using CustomTkinter widgets.
- Integrate the core sorting logic into other Python projects.

---

**SORTITO turns minutes into seconds – sort your media the smart way.**