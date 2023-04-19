import threading
import time

class ProxyListener(threading.Thread):
    def __init__(self, browser_proxy, callback):
        threading.Thread.__init__(self)
        self.browser_proxy = browser_proxy
        self.callback = callback
        self.last_index = 0
        self.stopped = False

    def run(self):
        while not self.stopped:
            entries = self.browser_proxy.get_entries()
            new_entries = entries[self.last_index:]
            self.last_index = len(entries)
            for entry in new_entries:
                self.callback(entry)
            time.sleep(1)

    def stop(self):
        self.stopped = True
