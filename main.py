import cv2
import json
import logging
import time

from camera import Camera
from detector import HandDetector
from engine import GestureEngine
from manager import StateManager
from dispatcher import ActionDispatcher
from visualizer import Visualizer

class GestureControlApp:
    def __init__(self, config_path="config.json"):
        self.load_config(config_path)
        
        # Init hardware
        self.camera = Camera(
            camera_id=self.config['settings']['camera_id'],
            resolution=tuple(self.config['settings']['resolution'])
        )
        
        # Init detection (2 hands)
        self.detector = HandDetector(
            max_hands=2,
            complexity=self.config['settings']['model_complexity'],
            detection_con=self.config['settings']['min_detection_confidence'],
            track_con=self.config['settings']['min_tracking_confidence']
        )
        
        self.engine = GestureEngine()
        
        # Two managers (one per hand)
        self.managers = {
            "Right": StateManager(
                debounce_frames=self.config['settings']['debounce_frames'],
                cooldown_seconds=self.config['settings']['cooldown_seconds']
            ),
            "Left": StateManager(
                debounce_frames=self.config['settings']['debounce_frames'],
                cooldown_seconds=self.config['settings']['cooldown_seconds']
            )
        }
        
        # Dispatchers per hand
        self.dispatchers = {
            "Right": ActionDispatcher(self.config['gestures'].get('Right', {})),
            "Left": ActionDispatcher(self.config['gestures'].get('Left', {}))
        }
        
        self.visualizer = Visualizer()
        
        self.skip_frames = self.config['settings'].get('skip_frames', 0)
        self.headless = self.config['settings'].get('headless', False)
        self.frame_count = 0
        self.running = False
        
        if self.headless:
            logging.info("GestureControlApp running in HEADLESS mode.")
        
        logging.info("GestureControlApp V2 initialized.")

    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise

    def run(self):
        self.running = True
        logging.info("Starting V2 main loop...")
        
        try:
            while self.running:
                frame = self.camera.get_frame()
                if frame is None:
                    break
                
                self.frame_count += 1
                
                # 1. Detection
                self.detector.find_hands(frame)
                all_hand_data = self.detector.get_landmarks(frame)
                
                # Active hands in this frame
                active_labels = []
                
                # 2. Recognition & Dispatch for each hand found
                for hand in all_hand_data:
                    label = hand['label'] # "Left" or "Right"
                    landmarks = hand['landmarks']
                    active_labels.append(label)
                    
                    if landmarks:
                        # a) Classify gesture
                        finger_states = self.engine.get_finger_states(landmarks)
                        gesture = self.engine.classify_gesture(finger_states)
                        
                        # b) Update manager for THIS hand
                        stable_gesture, confidence = self.managers[label].update(gesture)
                        
                        # c) Dispatch if stable and NEW (change-only trigger)
                        if stable_gesture and self.managers[label].can_trigger():
                            success = self.dispatchers[label].run_command(stable_gesture)
                            if success:
                                self.managers[label].trigger_success()
                        
                        # d) Visualize this hand
                        if not self.headless:
                            try:
                                frame = self.visualizer.draw_status(frame, label, stable_gesture, 
                                                                   stable=(stable_gesture is not None), 
                                                                   confidence=confidence)
                            except Exception as e:
                                logging.warning(f"GUI Error: {e}. Switching to headless.")
                                self.headless = True
                
                # Update managers for hands NOT seen in this frame (to reset buffers)
                for label, mgr in self.managers.items():
                    if label not in active_labels:
                        mgr.update(None)

                # 3. HUD Overlay
                if not self.headless:
                    try:
                        frame = self.detector.draw_landmarks(frame)
                        frame = self.visualizer.draw_fps(frame)
                        cv2.imshow("Gesture Control V2 (Sway)", frame)
                    except Exception as e:
                        logging.warning(f"GUI Error: {e}. Switching to headless.")
                        self.headless = True
                
                # Exit keys
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.running = False
                elif key == ord('r'):
                    self.load_config("config.json")
                    self.dispatchers["Right"].gesture_map = self.config['gestures'].get('Right', {})
                    self.dispatchers["Left"].gesture_map = self.config['gestures'].get('Left', {})
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
