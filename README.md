<!-- SORTITO README - Modern & Cool -->

<p align="center">
  <img src="logo.png" alt="SORTITO Logo" width="120" height="120" style="border-radius: 20px;">
</p>

<h1 align="center">SORTITO</h1>
<p align="center">
  <strong>Desktop File Organizer – Recursively sort videos & photos in one click.</strong>
</p>

<p align="center">
  <a href="https://github.com/GreyHatSonawane/SORTITO/releases/tag/v1.0">
    <img src="https://img.shields.io/badge/Download%20Latest-Exe-2ea44f?style=for-the-badge&logo=windows&logoColor=white" alt="Download for Windows">
  </a>
  <a href="https://github.com/GreyHatSonawane/SORTITO">
    <img src="https://img.shields.io/github/stars/GreyHatSonawane/SORTITO?style=for-the-badge&logo=github" alt="GitHub stars">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&logo=opensourceinitiative" alt="MIT License">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Tkinter-GUI-ff69b4?style=flat-square" alt="Tkinter">
  <img src="https://img.shields.io/badge/CustomTkinter-Modern-1f425f?style=flat-square" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/Pillow-Images-008cba?style=flat-square&logo=pillow" alt="Pillow">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Cross-platform">
</p>

---

## 📥 Download

> **Ready to use?** Grab the latest portable executable (no installation needed).

<p align="center">
  <a href="https://github.com/GreyHatSonawane/SORTITO/releases/tag/v1.0">
    <img src="https://img.shields.io/badge/⬇️%20Download%20SORTITO%20v1.0-2ea44f?style=for-the-badge&logo=windows&logoColor=white" alt="Download">
  </a>
</p>

---

## ✨ What is SORTITO?

**SORTITO** is a modern desktop application that **recursively scans any folder** (including all subfolders) and automatically sorts your **video** and **photo** files into dedicated `videos/` and `photos/` folders. No more manual dragging – just select a folder and click start.

### Key Features

| Feature | Description |
|---------|-------------|
| 🌀 **Recursive scan** | Goes through every subfolder, no limit on depth. |
| 📹 **Smart detection** | Recognises 30+ video & photo formats (easily extensible). |
| 🔄 **Copy / Move** | Choose to duplicate or relocate files. |
| 🏷️ **Duplicate handling** | Automatically renames conflicting files (`file_1.mp4`). |
| 📁 **“Others” folder** | Optionally collect all non‑media files. |
| 🌗 **Dark / Light theme** | Toggle instantly, follows system preference. |
| 📊 **Progress + ETA** | Real‑time percentage and estimated time remaining. |
| ⏹️ **Cancel anytime** | Safe stop – already processed files are kept. |
| 🪶 **Portable .exe** | Single file, no Python installation required. |

---

## 🖼️ Screenshots

<p align="center">
  <img src="screenshot-light.png" width="45%" alt="Light mode">
  &nbsp;&nbsp;
  <img src="screenshot-dark.png" width="45%" alt="Dark mode">
</p>

---

## 🧰 Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,py,git,github,windowsserver&theme=light" />
</p>

- **Python 3.8+** – Core logic and cross‑platform support.
- **CustomTkinter** – Modern, flat, rounded GUI.
- **Pillow (PIL)** – Image handling and icon processing.
- **PyInstaller** – Bundles everything into a single `.exe`.
- **Tkinter** – Native file dialogs and base windowing.

---

## 🚀 Quick Start

### Option 1: Run the executable (Windows)
1. Download `SORTITO.exe` from the [Releases](../../releases) page.
2. Double‑click to launch – no installation needed.
3. Select a source folder, choose options, and click **Start Sorting**.

### Option 2: Run from source (Python)
```bash
# Clone the repository
git clone https://github.com/GreyHatSonawane/SORTITO.git
cd SORTITO

# Install dependencies
pip install customtkinter pillow

# Run the app
python media_sorter_gui.py
