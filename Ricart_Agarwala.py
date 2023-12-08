import random
import threading
import time
import pickle

class RicartAgrawalaMutex:
    def __init__(self, num_processes, process_id):
        self.num_processes = num_processes
        self.process_id = process_id
        self.request_time = [0] * num_processes
        self.reply_count = 0
        self.want_to_enter = False
        self.in_critical_section = False
        self.lock = threading.Lock()

    def request(self):
        with self.lock:
            self.want_to_enter = True
            self.request_time[self.process_id] = time.time()
            self.reply_count = 0
            for i in range(self.num_processes):
                if i == self.process_id:
                    continue
                while self.reply_count < self.num_processes - 1 and self.request_time[i] != 0 and (
                        self.request_time[i] < self.request_time[self.process_id] or
                        (self.request_time[i] == self.request_time[self.process_id] and i < self.process_id)):
                    pass

    def release(self):
        with self.lock:
            self.want_to_enter = False
            self.request_time[self.process_id] = 0

    def receive_request(self, requesting_process):
        with self.lock:
            if self.want_to_enter and (self.request_time[requesting_process] < self.request_time[self.process_id] or
                    (self.request_time[requesting_process] == self.request_time[self.process_id] and requesting_process < self.process_id)):
                pass
            else:
                self.request_time[requesting_process] = 0

    def receive_reply(self, replying_process):
        with self.lock:
            self.reply_count += 1

    def enter_critical_section(self):
        with self.lock:
            self.in_critical_section = True

    def exit_critical_section(self):
        with self.lock:
            self.in_critical_section = False
            self.release()

    def request_cs(self):
        self.request()
        self.enter_critical_section()

    def release_cs(self):
        self.exit_critical_section()

# Usage Example
def process(process_id, mutex, folders):
    while True:
        folder_name = folders[process_id]
        print(f"Process {process_id} is not in the critical section.")
        time.sleep(1)

        mutex.request_cs()
        print(f"Process {process_id} is accessing folder '{folder_name}'.")
        time.sleep(2)  # Simulate work inside the folder
        mutex.release_cs()

if __name__ == "__main__":
    num_processes = 3
    mutex = RicartAgrawalaMutex(num_processes, 0)
    
    # Folders as nodes in the distributed system
    folders = ["a", "b", "c"]

    # Shuffle the order of folders randomly
    random.shuffle(folders)

    # Start multiple threads representing processes
    threads = []
    for i in range(num_processes):
        t = threading.Thread(target=process, args=(i, mutex, folders))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
