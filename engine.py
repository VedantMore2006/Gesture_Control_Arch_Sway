import math

class GestureEngine:
    def __init__(self):
        # MediaPipe Landmark IDs for tips and PIP joints
        self.tip_ids = [8, 12, 16, 20] # Index, Middle, Ring, Pinky
        self.pip_ids = [6, 10, 14, 18] # Respective PIP joints
        self.thumb_tip = 4
        self.thumb_ip = 2

    def get_finger_states(self, landmarks):
        """
        Returns a list of booleans: [Thumb, Index, Middle, Ring, Pinky]
        True = Extended (Up), False = Folded (Down)
        """
        if not landmarks:
            return None

        # Landmarks format: [id, x, y, z]
        # Coordinates are screen-space (pixels) from HandDetector
        fingers = []

        # Thumb logic (horizontal extension for right/left hand)
        # Using simple x comparison for now, but y can be used if hand is vertical
        # In a mirror view, if thumb_tip.x > thumb_base.x, thumb is likely out
        if landmarks[self.thumb_tip][1] > landmarks[self.thumb_ip][1]:
            fingers.append(True)
        else:
            fingers.append(False)

        # 4 Fingers logic (vertical comparison)
        for i in range(len(self.tip_ids)):
            # If tip y is higher (smaller value) than PIP y, finger is UP
            if landmarks[self.tip_ids[i]][2] < landmarks[self.pip_ids[i]][2]:
                fingers.append(True)
            else:
                fingers.append(False)

        return fingers

    def classify_gesture(self, finger_states):
        if not finger_states:
            return None

        # [Thumb, Index, Middle, Ring, Pinky]
        
        # FIST: [False, False, False, False, False]
        if all(not s for s in finger_states[1:]): # Ignore thumb for basic fist
            return "FIST"

        # PALM: [True, True, True, True, True]
        if all(finger_states[1:]):
            return "PALM"

        # PEACE: [False, True, True, False, False]
        if finger_states[1] and finger_states[2] and not finger_states[3] and not finger_states[4]:
            return "PEACE"
            
        # POINT: [False, True, False, False, False]
        if finger_states[1] and all(not s for s in finger_states[2:]):
            return "POINT"

        # THUMBS_UP: [True, False, False, False, False]
        if finger_states[0] and all(not s for s in finger_states[1:]):
            return "THUMBS_UP"

        return None

if __name__ == "__main__":
    # Test simple logic
    engine = GestureEngine()
    print(f"Fist Test: {engine.classify_gesture([False, False, False, False, False])}")
    print(f"Palm Test: {engine.classify_gesture([True, True, True, True, True])}")
    print(f"Peace Test: {engine.classify_gesture([False, True, True, False, False])}")
