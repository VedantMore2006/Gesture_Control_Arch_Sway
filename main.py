import cv2
import json
import logging
import time
import os

os.environ["QT_QPA_PLATFORM"] = "xcb"

from camera import Camera
from detector import HandDetector
from engine import GestureEngine
from manager import StateManager
from dispatcher import ActionDispatcher
from visualizer import Visualizer

class GestureControlApp:
    def __init__(self, config_path="config.json"):
        self.load_config(config_path)
        
        # Init modules
        self.camera = Camera(
            camera_id=self.config['settings']['camera_id'],
            resolution=tuple(self.config['settings']['resolution'])
        )
        
        self.detector = HandDetector(
            complexity=self.config['settings']['model_complexity'],
            detection_con=self.config['settings']['min_detection_confidence'],
            track_con=self.config['settings']['min_tracking_confidence']
        )
        
        self.engine = GestureEngine()
        
        self.manager = StateManager(
            debounce_frames=self.config['settings']['debounce_frames'],
            cooldown_seconds=self.config['settings']['cooldown_seconds']
        )
        
        self.dispatcher = ActionDispatcher(self.config['gestures'])
        self.visualizer = Visualizer()
        
        self.skip_frames = self.config['settings'].get('skip_frames', 0)
        self.headless = self.config['settings'].get('headless', False)
        self.frame_count = 0
        self.running = False
        
        if self.headless:
            logging.info("GestureControlApp running in HEADLESS mode.")
        
        logging.info("GestureControlApp initialized.")

    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise

    def run(self):
        self.running = True
        logging.info("Starting main loop...")
        
        try:
            while self.running:
                frame = self.camera.get_frame()
                if frame is None:
                    break
                
                self.frame_count += 1
                if self.skip_frames > 0 and self.frame_count % (self.skip_frames + 1) != 0:
                    # Logic for skipping frames if CPU is high
                    # We still want to show the feed if possible
                    # Or just continue
                    pass

                # 1. Detection
                self.detector.find_hands(frame)
                landmarks = self.detector.get_landmarks(frame)
                
                # 2. Recognition
                gesture = None
                if landmarks:
                    finger_states = self.engine.get_finger_states(landmarks)
                    gesture = self.engine.classify_gesture(finger_states)
                
                # 3. State Management (Debounce)
                stable_gesture, confidence = self.manager.update(gesture)
                
                # 4. Dispatching
                if stable_gesture and self.manager.can_trigger():
                    # Only trigger if gesture has changed or cooldown passed?
                    # The manager.can_trigger() handles cooldown.
                    success = self.dispatcher.run_command(stable_gesture)
                    if success:
                        self.manager.trigger_success()
                
                # 5. Visualization (Optional - can be disabled for headless)
                if not self.headless:
                    try:
                        frame = self.detector.draw_landmarks(frame)
                        frame = self.visualizer.draw_fps(frame)
                        frame = self.visualizer.draw_status(frame, stable_gesture, stable=(stable_gesture is not None), confidence=confidence)
                        
                        cv2.imshow("Gesture Control (Sway)", frame)
                    except Exception as e:
                        logging.warning(f"GUI Error: {e}. Switching to headless mode.")
                        self.headless = True
                
                # Exit keys
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.running = False
                elif key == ord('r'):
                    self.load_config("config.json")
                    self.dispatcher.gesture_map = self.config['gestures']
                    logging.info("Config reloaded.")

        finally:
            self.camera.release()
            try:
                cv2.destroyAllWindows()
            except:
                pass
            logging.info("App shutdown.")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    app = GestureControlApp()
    app.run()
