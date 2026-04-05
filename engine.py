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

        # Hand Scale (Distance from wrist to middle finger base)
        # Used to normalize the "sharpness" threshold based on distance from camera
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        scale = math.sqrt((wrist[1]-middle_mcp[1])**2 + (wrist[2]-middle_mcp[2])**2)
        
        # Sharpness Threshold (e.g., tip must be 20% of hand scale above joint)
        threshold = scale * 0.2

        fingers = []

        # Thumb logic (horizontal extension)
        # Thumb is "up" if its tip is significantly outside its MCP/IP joint
        if abs(landmarks[self.thumb_tip][1] - landmarks[self.thumb_ip][1]) > threshold:
            fingers.append(True)
        else:
            fingers.append(False)

        # 4 Fingers logic (vertical comparison + sharpness threshold)
        for i in range(len(self.tip_ids)):
            # diff = pip.y - tip.y
            diff = landmarks[self.pip_ids[i]][2] - landmarks[self.tip_ids[i]][2]
            
            if diff > threshold:
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

        # YO: [True, True, False, False, True] (Thumb, Index, Pinky)
        if finger_states[0] and finger_states[1] and finger_states[4] and not finger_states[2] and not finger_states[3]:
            return "YO"

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
