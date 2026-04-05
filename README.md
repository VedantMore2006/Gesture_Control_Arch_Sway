# 🧠 Gesture-Controlled Sway Interface (V3.0)

A modular, dual-hand, high-performance system to control the **Sway (Wayland)** compositor using hand gestures. Built with Python, OpenCV, and MediaPipe.

---

## 🧩 Architectural Overview (V3.0)

The system is built on a decoupled pipeline optimized for low-latency dual-hand tracking:

1.  **Camera Layer (`camera.py`)**: Captures video (default 640x480), flips it for mirror view, and feeds the detector.
2.  **Detection Layer (`detector.py`)**: Identifies up to **2 hands** simultaneously. Distinguishes between **Left** and **Right** hands.
3.  **Engine Layer (`engine.py`)**: Converts landmarks into semantic states. Supports: `FIST`, `PALM`, `PEACE`, `POINT`, `YO`, and `THUMBS_UP`.
    - **Sharp Detection (NEW)**: Uses a scale-based threshold (20% of hand size) to ensure gestures are intentional and "crisp".
4.  **State Manager (`manager.py`)**: Implements **Change-Only** triggers using a rolling buffer. Actions fire only when a gesture **transitions** (e.g., FIST -> NEUTRAL -> FIST).
5.  **Dispatcher Layer (`dispatcher.py`)**: Bridges gestures to the OS, executing `swaymsg`, shell commands, or keyboard emulation.
6.  **Visualizer (`visualizer.py`)**: Dual-hand HUD showing side-by-side status, FPS, and detection confidence.

---

## ✋ Gesture-to-Action Mappings

The current configuration uses independent controllers for each hand:

### 🖐️ Right Hand (Workspace & Navigation)
| Gesture | Logic | Default Action |
| :--- | :--- | :--- |
| ✊ **FIST** | All fingers folded | `swaymsg workspace 1` |
| ✋ **PALM** | All fingers extended | `swaymsg workspace 2` |
| ✌️ **PEACE** | Index + Middle up | `swaymsg workspace 3` |
| ☝️ **POINT** | Index up only | `swaymsg workspace next` |

### 🤚 Left Hand (System & Control)
| Gesture | Logic | Default Action |
| :--- | :--- | :--- |
| ✊ **FIST** | All fingers folded | `swaymsg kill` (Close Window) |
| ✋ **PALM** | All fingers extended | `swaymsg exec brave` |
| ✌️ **PEACE** | Index + Middle up | `swaymsg exec kitty` |
| ☝️ **POINT** | Index up only | `swaymsg floating toggle` |
| 🤘 **YO** | Thumb + Index + Pinky up | **Type "HI"** (using `wtype`) |

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.10+
- Sway / Wayland environment
- `wtype` (for keyboard emulation)
- `brave` and `kitty` (or edit `config.json` for your choices)

### Installation
```bash
conda activate gesture_control
pip install -r requirements.txt
```

### Running the App
```bash
python main.py
```

- **Q**: Quit the application.
- **R**: Reload `config.json` while running.

---

## 📁 File Structure
```text
.
├── camera.py        # OpenCV Capture
├── detector.py      # Dual-Hand Detection (V2+)
├── engine.py        # Gesture Classification (V3 Sharpness)
├── manager.py       # Change-Only State Logic
├── dispatcher.py    # OS/Sway Bridge
├── visualizer.py    # Side-by-Side HUD
├── main.py          # Dual-Hand Orchestrator (V3 Safe)
└── config.json      # Dual-Hand Settings
```

## ⚠️ Troubleshooting
- **Hand Mirroring**: Depending on your camera, "Left" might be detected as "Right". You can either swap the hand blocks in `config.json` or map important gestures to **both** hands.
- **No GUI**: If `imshow` fails, the system automatically falls back to **Headless Mode** for background control.
