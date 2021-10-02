"""
Tool implementing following features:

1. if a USB video device with the provided VID and PID is found, open the video 
stream and show it upscaled (or downscaled) to 640x480. A proper error must be shown otherwise

2. while the video stream is being shown, every d (delay) seconds:
    a) save a frame using the timestamp as filename and a format of your choice(png,
bmp, jpeg, etc...)
    b) save the following metadata in a json:date, cpuload, freeram, freedisk, wlan/ip
address if present

3. on CTRL+C:
    a) wait for any pending operation to be completed
    b) close the usb stream
    c) print how many frames have been saved and the avg cpu load between the first and
the last frame saved d) exit
"""

import argparse
import cv2 # opencv-python
import logging
import signal
import sys
import uvclite # wrapper for libuvc

from usb_camera_utils.frame_format import select_frame_format
from usb_camera_utils.args_checks import CheckPositiveAction, Check2ByteHexAction
from usb_camera_utils.save_state_thread import SaveStateThread

DEFAULT_SCREEN_SIZE = (640, 480)

# parse arguments
parser = argparse.ArgumentParser(description = __doc__)
parser.add_argument('-v', '--vid', metavar = '', action = Check2ByteHexAction,
    type = str, required = True, help = 'Vendor ID')
parser.add_argument('-p', '--pid', metavar = '', action = Check2ByteHexAction,
    type = str, required = True, help = 'Product ID')
parser.add_argument('-d', '--delay', metavar = '',
    action = CheckPositiveAction,type = int, required = True,
    help = 'Delay in seconds between saves of frames and metadata.')

args = parser.parse_args()

def loop(device, save_state_thread):
    try:
        while True: # main loop
            frame = device.get_frame_bgr() # OpenCV uses BGR
            frame = cv2.resize(frame, DEFAULT_SCREEN_SIZE)
            save_state_thread.process_frame(frame)
            cv2.imshow('frame', frame) 
            cv2.waitKey(1)
            if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
                break # hack for closing window with X button
    except KeyboardInterrupt: # Ctrl-C
        pass

try:
    save_state_thread = SaveStateThread(args.delay)
    save_state_thread.start()

    with uvclite.UVCContext() as context:
        device = context.find_device(vendor_id=args.vid, product_id=args.pid)
        device.open()
        frame_format = select_frame_format(
            device.get_list_of_formats(), DEFAULT_SCREEN_SIZE)
        # HACK - my camera returns UYVY but works only with YUYV/ANY :-((
        frame_format['frame_format'] = uvclite.UVCFrameFormat.UVC_FRAME_FORMAT_ANY
        device.set_stream_format(**frame_format)
        device.start_streaming()
        loop(device, save_state_thread)
        device.stop_streaming()
        device.close()
        print(save_state_thread.final_report()) # print saved frame count and avg cpu
except Exception as e:
    logging.error(e)
finally: # clean up
    cv2.destroyAllWindows()
    save_state_thread.terminate_thread()