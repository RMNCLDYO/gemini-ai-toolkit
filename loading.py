import sys
import time
import threading

class Loading:
    def __init__(self):
        self.spinner = '|/-\\'
        self.spinner_index = 0
        self.running = False
        self.thread = None

    def hide_cursor(self):
        try:
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()
        except Exception as e:
            print(f"[ WARNING ]: Failed to hide cursor: {str(e)}")

    def show_cursor(self):
        try:
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()
        except Exception as e:
            print(f"[ WARNING ]: Failed to show cursor: {str(e)}")

    def clear_line(self):
        try:
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
        except Exception as e:
            print(f"[ WARNING ]: Failed to clear line: {str(e)}")

    def update(self):
        while self.running:
            try:
                sys.stdout.write('\rWaiting for assistant response... ' + self.spinner[self.spinner_index])
                sys.stdout.flush()
                self.spinner_index = (self.spinner_index + 1) % len(self.spinner)
                time.sleep(0.1)
            except Exception as e:
                print(f"[ WARNING ]: Error updating spinner: {str(e)}")
                break
        self.clear_line()
        self.show_cursor()

    def start(self):
        if not self.running:
            try:
                self.running = True
                self.hide_cursor()
                self.thread = threading.Thread(target=self.update)
                self.thread.start()
            except Exception as e:
                print(f"[ ERROR ]: Failed to start loading animation: {str(e)}")
                self.running = False
                self.show_cursor()

    def stop(self):
        if self.running:
            try:
                self.running = False
                if self.thread:
                    self.thread.join(timeout=1)  # Wait for up to 1 second for the thread to finish
                    if self.thread.is_alive():
                        print("[ WARNING ]: Loading animation thread did not terminate as expected.")
            except Exception as e:
                print(f"[ ERROR ]: Failed to stop loading animation: {str(e)}")
            finally:
                self.show_cursor()
                self.clear_line()