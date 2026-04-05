import subprocess
import logging

class ActionDispatcher:
    def __init__(self, gesture_map):
        self.gesture_map = gesture_map
        logging.info(f"ActionDispatcher initialized with {len(gesture_map)} mappings.")

    def run_command(self, gesture):
        if gesture in self.gesture_map:
            cmd = self.gesture_map[gesture]
            logging.info(f"Executing: {cmd} for gesture: {gesture}")
            
            try:
                # Use shell=True if the command is a string, otherwise use list
                if isinstance(cmd, list):
                    subprocess.run(cmd, check=True)
                else:
                    subprocess.run(cmd, shell=True, check=True)
                return True
            except subprocess.CalledProcessError as e:
                logging.error(f"Command failed: {e}")
            except Exception as e:
                logging.error(f"Error executing command: {e}")
        else:
            logging.warning(f"No command mapped for gesture: {gesture}")
        return False

if __name__ == "__main__":
    # Test dispatcher
    logging.basicConfig(level=logging.INFO)
    test_map = {
        "TEST": ["notify-send", "Gesture Control", "Test Action Executed"]
    }
    dispatcher = ActionDispatcher(test_map)
    dispatcher.run_command("TEST")
