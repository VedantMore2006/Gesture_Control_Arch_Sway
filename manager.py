import time
from collections import deque, Counter

class StateManager:
    def __init__(self, debounce_frames=5, cooldown_seconds=3.0):
        self.debounce_frames = debounce_frames
        self.cooldown_seconds = cooldown_seconds
        self.gesture_buffer = deque(maxlen=debounce_frames)
        self.last_action_time = 0
        self.current_gesture = None
        self.stable_gesture = None

    def update(self, detected_gesture):
        # Add current detection to buffer (can be None)
        self.gesture_buffer.append(detected_gesture)
        
        # Determine the most common gesture in the buffer
        if len(self.gesture_buffer) < self.debounce_frames:
            return None, 0.0

        counts = Counter(self.gesture_buffer)
        most_common, count = counts.most_common(1)[0]
        confidence = count / self.debounce_frames

        # Only update if the gesture is dominant and not None
        if confidence >= 0.8 and most_common is not None:
             self.stable_gesture = most_common
        else:
             self.stable_gesture = None

        return self.stable_gesture, confidence

    def can_trigger(self):
        curr_time = time.time()
        if curr_time - self.last_action_time >= self.cooldown_seconds:
            return True
        return False

    def trigger_success(self):
        self.last_action_time = time.time()
        # Clear buffer to prevent immediate re-triggering?
        # Actually, cooldown handles it, but clearing can help
        self.gesture_buffer.clear()

if __name__ == "__main__":
    # Test manager logic
    mgr = StateManager(debounce_frames=3, cooldown_seconds=2.0)
    
    # Simulate a series of frames
    frames = ["FIST", "FIST", "FIST", "PALM", "PALM", "PALM"]
    for f in frames:
        stable, conf = mgr.update(f)
        print(f"Input: {f} | Stable: {stable} | Confidence: {conf:.2f}")
        if stable and mgr.can_trigger():
            print(">>> ACTION TRIGGERED!")
            mgr.trigger_success()
        time.sleep(0.1)
