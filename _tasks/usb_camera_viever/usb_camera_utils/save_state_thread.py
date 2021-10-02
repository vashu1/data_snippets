import cv2
import datetime
import json
import logging
import multiprocessing
import os
import psutil 
import socket
import sys
import threading
import time

from . import avg_counter

# could be split to 2 separate threads for json and jpeg
# but then there will be a little more extra code in main
class SaveStateThread(threading.Thread):
    TERMINATION_TIMEOUT = 3

    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.queue = multiprocessing.Queue(maxsize=0)
        self.delay = delay
        self.last_save_timestamp = None
        self._host_ip = None
        self.saved_frames_count = 0
        self.cpu_loads = avg_counter.AvgPercentCounter()

    def terminate_thread(self):
        self.queue.put(None) # signal for run() to terminate
        self.join(self.TERMINATION_TIMEOUT)

    def run(self):
        while True:
            frame = self.queue.get() # will block if queue is empty
            if frame is None:
                break # finish thread
            timestamp = int(time.time())
            with open(f'{timestamp}.json', 'a') as file:
                metadata = self._get_metadata()
                file.write(json.dumps(metadata))
            cv2.imwrite(f'{timestamp}.jpg', frame)
            self.saved_frames_count += 1

    def final_report(self):
        self.terminate_thread()
        # print how many frames have been saved and
        # the avg cpu load between the first and the last frame saved
        result  = '\n'
        result += f'{self.saved_frames_count} frames have been saved\n'
        result += f'{round(self.cpu_loads.get_average(), 1)}% avg cpu' \
            f' load between the first and the last frame saved'
        return result

    def process_frame(self, frame):
        if not self.delay: # if delay is not set - do nothing
            return
        if not self.last_save_timestamp:
            self.last_save_timestamp = time.time()
        elif time.time() - self.last_save_timestamp > self.delay:
            while time.time() - self.last_save_timestamp > self.delay:
                self.last_save_timestamp += self.delay
        else: # "delay" seconds did not pass since last data save
            return 
        if not self.queue.empty():
            logging.warning('SaveStateThread can\'t keep up. Skipped saving some data!\n')
            while not self.queue.empty(): # to empty queue
                _ = self.queue.get()
        self.queue.put(frame)

    def _get_metadata(self):
        cpu_load = psutil.cpu_percent()
        self.cpu_loads.put_value(cpu_load)
        metadata = {
            'date': str(datetime.date.today()),
            'cpuload_percent': cpu_load,
            'freeram_bytes': psutil.virtual_memory().free,
            'freedisk_bytes': self._get_disk_space(),
            'ip': self._get_host_ip(),
        }
        return metadata

    def _get_disk_space(self):
        s = os.statvfs('./')
        return s.f_bavail * s.f_frsize

    def _get_host_ip(self): 
        # does not really work: return socket.gethostbyname(socket.gethostname()) 
        try:
            if self._host_ip is None: # ping only once, after that use cached value
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("8.8.8.8", 53))
                self._host_ip = str(s.getsockname()[0])
                s.close()
            return self._host_ip
        except:
            self._host_ip = 'none'