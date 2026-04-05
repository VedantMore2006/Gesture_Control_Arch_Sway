import cv2
import time

class Visualizer:
    def __init__(self, font_scale=0.8, thickness=2):
        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.font_scale = font_scale
        self.thickness = thickness
        self.prev_time = 0

    def draw_fps(self, frame):
        curr_time = time.time()
        fps = 1 / (curr_time - self.prev_time)
        self.prev_time = curr_time
        
        # Display FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                    self.font, self.font_scale, (0, 255, 0), self.thickness)
        return frame

    def draw_status(self, frame, label, gesture, stable=False, confidence=0.0):
        # Determine color
        color = (0, 255, 0) if (stable and gesture) else (0, 0, 255)
        
        # Determine position based on label
        # Right hand on the right side, Left hand on the left
        if label == "Right":
            x, y = frame.shape[1] - 250, 70
        else:
            x, y = 10, 70
            
        text = f"{label}: {gesture}" if gesture else f"{label}: --"
        
        cv2.putText(frame, text, (x, y), 
                    self.font, self.font_scale, color, self.thickness)
        
        # Progress bar
        if gesture:
            cv2.rectangle(frame, (x, y + 15), (x + 200, y + 30), (50, 50, 50), -1)
            filled_w = int(200 * confidence)
            cv2.rectangle(frame, (x, y + 15), (x + filled_w, y + 30), color, -1)
        
        return frame

    def draw_hand_status(self, frame, hand_exists=False):
        color = (0, 255, 0) if hand_exists else (0, 0, 255)
        status = "HAND TRACKED" if hand_exists else "SEARCHING..."
        cv2.circle(frame, (frame.shape[1]-20, 20), 10, color, -1)
        # Use simple text
        return frame

if __name__ == "__main__":
    # Test visualization
    cam = cv2.VideoCapture(0)
    viz = Visualizer()
    while True:
        ret, frame = cam.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        viz.draw_fps(frame)
        viz.draw_status(frame, "FIST", stable=True, confidence=0.8)
        viz.draw_hand_status(frame, True)
        
        cv2.imshow("Viz Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cam.release()
    cv2.destroyAllWindows()
