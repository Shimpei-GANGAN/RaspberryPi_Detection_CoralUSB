#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   December  03  12:00, 2019 (Tue)
#------------------------------------------------------------
#
#   Raspberry Pi + Coral USB ACCELERATOR + Arduino
#       ・Coral USBを用いたリアルタイム顔検出
#       ・
#
#   本プログラムではcv2.VideoCapture()を使用
#------------------------------------------------------------

import argparse
import time
import sys
#  pip
import serial
import asyncio
import serial_asyncio

#  vision 
import cv2 
import numpy as np
import picamera
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from PIL import Image, ImageDraw, ImageFont


"""
    矩形の描画および表示
"""
def draw_image(image, results, labels, maxobjects):
    set_font = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"
    display_label = []
    
    for idx, obj in enumerate(results):
        #  Prepare image for drawing
        draw = ImageDraw.Draw(image)

        #  Prepare boundary box
        box = obj.bounding_box.flatten().tolist()

        #  Draw rectangle to desired thickness
        for x in range( 0, maxobjects ):
            draw.rectangle(box, outline=(0, 0, 255))

        #  Annotate image with label and confidence score
        if labels:
            display_str = labels[obj.label_id] + ": " + str(round(obj.score*100, 2)) + "%"
            draw.text((box[0], box[1]), display_str, font=ImageFont.truetype(set_font, 20))
            display_label.append([labels[obj.label_id], obj.score])
    #print(display_label)

    cv2.imshow("Coral Live Object Detection", np.asarray(image))
    #return display_label

"""
    Set up Arguments
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        help='Path of the detection model, it must be a SSD model with postprocessing operator.',
        required=True)
    parser.add_argument(
        "--label", help="Path of the labels file.")
    parser.add_argument(
        "--maxobjects", type=int, default=3, help="Maximum objects")
    parser.add_argument(
        "--threshold", type=float, default=0.05, help="Minimum threshold")
    parser.add_argument(
        "--picamera", action="store_true",
        help="Use PiCamera for image capture")
    parser.add_argument(
        '--keep_aspect_ratio',
        dest='keep_aspect_ratio',
        action='store_true',
        help=(
            'keep the image aspect ratio when down-sampling the image by adding '
            'black pixel padding (zeros) on bottom or right. '
            'By default the image is resized and reshaped without cropping. This '
            'option should be the same as what is applied on input images during '
            'model training. Otherwise the accuracy may be affected and the '
            'bounding box of detection result may be stretched.'))
    parser.set_defaults(keep_aspect_ratio=False)
    args = parser.parse_args()
    return args


"""
    Raspberry Pi to Arduino
"""
class Output(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self._transport = None

    #  Called when creating a connection
    def connection_made(self, transport):
        self._transport = transport
        print("--------------------------------")
        print("port opened\n", self._transport)
        print("--------------------------------")
        self._transport.serial.rts = False
        self._transport.write(b"1;")

    #  When data is received
    def data_received(self, data):
        print("--------------------------------")
        print("data received", data)
        print("--------------------------------")
        if b"\n" in data:
            self._transport.close()

    #  When a connection is lost
    def connection_lost(self, exc):
        print("port closed")
        self._transport.loop.stop()


"""
    メイン処理
"""
def Object_Detection(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(
        loop, Output, 
        "/dev/ttyACM0",
        baudrate=9600,
        write_timeout=0.1)

    #  Initialize args
    args = parse_args()

    #  Initialize video stream
    print("--------------------------------")
    #if not args.picamera:
        #  Set usb camera
    print("Use : usb camera")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("H", "2", "6", "4"))
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    
        #  Camera error handling
    if cap.isOpened() == False:
        print("Cannot open")
        sys.exit(1)
    """else:
        # Set picamera
        print("Use : picamera")
        cap = picamera.PiCamera()
        cap.resolution = (640, 480)
        cap.framerate = 30
    """
    print("--------------------------------")

    #  Initialize engine
    engine = DetectionEngine(args.model)
    labels = dataset_utils.read_label_file(args.label) if args.label else None

    #  Initialize serial
    print("Open Port")
    #ser = serial.Serial("/dev/ttyACM0", baudrate=9600, write_timeout=0.1)

    try:
        while True:
            #  Read frame from video
            _, img = cap.read()
            image = Image.fromarray(img)

            #  Perform inference
            results = engine.detect_with_image(
                image,
                threshold=args.threshold,
                keep_aspect_ratio=args.keep_aspect_ratio,
                relative_coord=False,
                top_k=args.maxobjects)
            if results:
                print(results)
                loop.run_until_complete(coro)
                print("Hello")
                #ser.write(b"1;")
            else:
                pass
                #ser.write(b"0;")

            #  draw image
            draw_image(image, results, labels, args.maxobjects)
                
            #  closing confition
            if cv2.waitKey(5) & 0xFF == ord("q"):
                #  ループを永遠に続けたい場合
                #loop.call_soon(Object_Detection, loop)
                #  ループを切るなら
                loop.stop()
                break
        
    except KeyboardInterrupt:
        print("Exit loop by Ctrl-c")

    print("FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)))
    cap.release()
    cv2.destroyAllWindows()
    print("Close Port")
    #ser.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_soon(Object_Detection, loop)
    loop.run_forever()
    loop.close()
