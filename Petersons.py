import threading
import time

class PetersonMutex:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.flags = [False] * num_processes
        self.turn = 0

    def lock(self, process_id):
        other = 1 - process_id
        self.flags[process_id] = True
        self.turn = process_id
        while self.flags[other] and self.turn == process_id:
            pass

    def unlock(self, process_id):
        self.flags[process_id] = False

stop_threads = False

def process(process_id, mutex, folders, response_times):
    while not stop_threads:
        folder_name = folders[process_id]
        print(f"Process {process_id} is not in the critical section.")
        time.sleep(1)

        start_time = time.time()

        mutex.lock(process_id)
        print(f"Process {process_id} is accessing folder '{folder_name}'.")
        time.sleep(2)  # Simulate work inside the folder
        mutex.unlock(process_id)

        end_time = time.time()

        response_times[process_id].append(end_time - start_time)

if __name__ == "__main__":
    num_processes = 3
    mutex = PetersonMutex(num_processes)
    
    folders = ["a", "b", "c"]
    response_times = [[] for _ in range(num_processes)]

    threads = []
    for i in range(num_processes):
        t = threading.Thread(target=process, args=(i, mutex, folders, response_times))
        threads.append(t)
        t.start()

    try:
        time.sleep(5)  # Run for 10 seconds, you can adjust this value as needed
        stop_threads = True  # Set the flag to stop threads
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass

    for i, times in enumerate(response_times):
        if len(times) > 0:
            avg_response_time = sum(times) / len(times)
            print(f"Process {i} - Average Response Time: {avg_response_time} seconds")
