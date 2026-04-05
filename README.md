# 🧠 Gesture-Controlled Sway Interface (V2.0)

A modular, dual-hand, high-performance system to control the **Sway (Wayland)** compositor using hand gestures. Built with Python, OpenCV, and MediaPipe.

---

## 🧩 Architectural Overview (V2.0)

The system is built on a decoupled pipeline optimized for low-latency dual-hand tracking:

1.  **Camera Layer (`camera.py`)**: Captures video (default 640x480), flips it for mirror view, and feeds the detector.
2.  **Detection Layer (`detector.py`)**: Identifies up to **2 hands** and classifies them as **Left** or **Right**.
3.  **Engine Layer (`engine.py`)**: Converts landmarks into semantic states. Supports: `FIST`, `PALM`, `PEACE`, `POINT`, and `THUMBS_UP`.
4.  **State Manager (`manager.py`)**: Implements **Change-Only** triggers using a rolling buffer. An action fires only when a gesture **transitions** (e.g., FIST -> NEUTRAL -> FIST).
5.  **Dispatcher Layer (`dispatcher.py`)**: Bridges gestures to the OS, executing `swaymsg` and shell commands via `subprocess`.
6.  **Visualizer (`visualizer.py`)**: Dual-hand HUD showing side-by-side status, FPS, and detection confidence.

---

## ✋ Dual-Hand Gesture Mappings

V2 uses independent controllers for each hand, allowing for simultaneous actions:

### 🖐️ Right Hand (Workspace & Navigation)
| Gesture | Logic | Default Sway Action |
| :--- | :--- | :--- |
| ✊ **FIST** | All fingers folded | `swaymsg workspace 1` |
| ✋ **PALM** | All fingers extended | `swaymsg workspace 2` |
| ✌️ **PEACE** | Index + Middle up | `swaymsg workspace 3` |
| ☝️ **POINT** | Index up only | `swaymsg workspace next` |

### 🤚 Left Hand (System & Applications)
| Gesture | Logic | Default Sway Action |
| :--- | :--- | :--- |
| ✊ **FIST** | All fingers folded | `swaymsg kill` (Close Window) |
| ✋ **PALM** | All fingers extended | `swaymsg exec firefox` |
| ✌️ **PEACE** | Index + Middle up | `swaymsg exec foot` (Terminal) |
| ☝️ **POINT** | Index up only | `swaymsg floating toggle` |

---

## 🛠️ Performance & Stability

- **Change-Only Triggers**: Eliminates rapid-fire execution by requiring a gesture transition before re-triggering.
- **Dual-Hand Managers**: Independent state management for Left/Right hands prevents cross-hand interference.
- **Headless Fallback**: Automatically switches to background operation if GUI resources (X11/Wayland windows) are unavailable.

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.10+
- Sway / Wayland environment
- `foot` terminal (default in config) and `firefox`

### Quick Start
```bash
conda activate gesture_control
pip install -r requirements.txt
python main.py
```

- **Q**: Quit the application.
- **R**: Hot-reload `config.json`.

---

## 📁 File Structure
```text
.
├── camera.py        # OpenCV Capture
├── detector.py      # Dual-Hand Detection
├── engine.py        # Gesture Classification
├── manager.py       # Change-Only State Logic
├── dispatcher.py    # OS/Sway Bridge
├── visualizer.py    # Side-by-Side HUD
├── main.py          # Dual-Hand Orchestrator
├── config.json      # Dual-Hand Settings
└── requirements.txt # Version-pinned dependencies
```
