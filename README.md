# 🧠 Gesture-Controlled Sway Interface

A modular, high-performance system to control the **Sway (Wayland)** compositor using hand gestures. Built with Python, OpenCV, and MediaPipe.

---

## 🧩 Architectural Overview

The system follows a clean, decoupled pipeline to ensure low latency and high reliability:

1.  **Camera Layer (`camera.py`)**: Captures raw video at 640x480, flips it horizontally for intuitive "mirror" control, and passes frames to the detector.
2.  **Detection Layer (`detector.py`)**: Uses **MediaPipe Hands** (CPU-optimized) to identify 21 hand landmarks in real-time.
3.  **Engine Layer (`engine.py`)**: Converts raw coordinates into semantic finger states (Up/Down) to classify gestures like `FIST`, `PALM`, or `PEACE`.
4.  **State Manager (`manager.py`)**: Implements a rolling-buffer **debounce** (typically 5 frames) to filter out tracking noise and a temporal **cooldown** (1.0s) to prevent repeated triggers.
5.  **Dispatcher Layer (`dispatcher.py`)**: Bridges the logic to the OS by executing `swaymsg` commands via subprocess.
6.  **Visualizer (`visualizer.py`)**: Provides real-time feedback, showing FPS, current detection status, and stability confidence bars.

---

## ✋ Supported Gestures & Actions

The current MVP supports 3 primary gestures, mapped in `config.json`:

| Gesture | Logic (Finger States) | Default Sway Action |
| :--- | :--- | :--- |
| ✊ **FIST** | All fingers folded down. | `swaymsg workspace 1` |
| ✋ **PALM** | All fingers extended up. | `swaymsg workspace 2` |
| ✌️ **PEACE** | Index & Middle up; Others down. | `notify-send "System Ready"` |

---

## 🛠️ Performance & Tuning

- **Debouncing**: Instead of triggering on a single frame, the system requires a consistent gesture for **80% of the last 5 frames**. This eliminates "flicker" triggers.
- **Model Complexity**: Set to `0` in `config.json` for maximum speed on mobile CPUs.
- **Resolution**: 640x480 is the sweet spot for MediaPipe accuracy vs. processing overhead.

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.10+
- Sway/Wayland Environment
- An active Conda environment (e.g., `face_env`)

### Installation
```bash
pip install -r requirements.txt
```

### Running the App
```bash
python main.py
```

- **Q**: Quit the application.
- **R**: Reload `config.json` without restarting.

---

## 📁 File Structure Breakdown
```text
.
├── camera.py        # OpenCV Capture Wrapper
├── detector.py      # MediaPipe Hands Wrapper
├── engine.py        # Gesture Classification Logic
├── manager.py       # State, Debounce & Cooldown
├── dispatcher.py    # Subprocess & swaymsg bridge
├── visualizer.py    # HUD / Visualization Overlay
├── main.py          # Orchestrator Loop
└── config.json      # Settings & Mappings
```
