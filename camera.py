import cv2
import logging

class Camera:
    def __init__(self, camera_id=0, resolution=(640, 480)):
        self.camera_id = camera_id
        self.resolution = resolution
        self.cap = None
        self._setup()

    def _setup(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            logging.error(f"Failed to open camera: {self.camera_id}")
            raise RuntimeError("Could not open webcam.")
        
        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        logging.info(f"Camera initialized with resolution {self.resolution}")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            logging.warning("Failed to read frame from camera.")
            return None
        # Flip frame horizontally for a more intuitive "mirror" feel
        return cv2.flip(frame, 1)

    def release(self):
        if self.cap:
            self.cap.release()
            logging.info("Camera released.")

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    cam = Camera()
    try:
        while True:
            frame = cam.get_frame()
            if frame is not None:
                cv2.imshow("Test Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()
