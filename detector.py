import mediapipe as mp
import logging
import cv2

class HandDetector:
    def __init__(self, mode=False, max_hands=1, complexity=0, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.detection_con = detection_con
        self.track_con = track_con

        # Init MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            model_complexity=self.complexity,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        logging.info(f"HandDetector initialized (max_hands={max_hands}, complexity={complexity})")

    def find_hands(self, frame):
        # Convert to RGB as MediaPipe requires it
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        # We can also return the frame with landmarks drawn if needed
        return self.results

    def get_landmarks(self, frame):
        landmarks = []
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append([id, cx, cy, lm.z])
        return landmarks

    def draw_landmarks(self, frame):
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return frame

if __name__ == "__main__":
    import cv2
    from camera import Camera
    logging.basicConfig(level=logging.INFO)
    
    cam = Camera()
    detector = HandDetector()
    
    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                break
            
            results = detector.find_hands(frame)
            frame = detector.draw_landmarks(frame)
            
            cv2.imshow("Hand Detection Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()
