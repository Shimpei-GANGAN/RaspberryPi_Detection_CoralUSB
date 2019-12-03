#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   December  04  08:00, 2019 (Wed)
#------------------------------------------------------------
#
#   Raspberry Pi + Coral USB ACCELERATOR + Arduino
#       ・Coral USBを用いたリアルタイム顔検出
#
#   本プログラムではcv2.VideoCapture()を使用
#------------------------------------------------------------

#  default
import argparse
import time
import sys
from multiprocessing import Process
from multiprocessing import Queue

#  pip
import serial, serial.tools.list_ports
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
        print("ffafafafafafaafa")

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

def ard_reset(q):
    print("ard reset function")

    #  Initialize serial
    #print("Open port")
    with serial.Serial("/dev/ttyACM0", 9600) as ser:
        for _ in range(10):
            ser.write(b"q;")
            time.sleep(1)


def ard(q):
    print("ard function")
    if q.get():
        send_str = q.get()
    """  理想の形
    if q.get() and q.get() == "H":
        send_str = "1;"
    else:
        send_str = "0;" if q.get() == "L" else "q;"
    """

    #  Automatic detection of connection port
    def _search_com_port():
        coms = serial.tools.list_ports.comports()
        comlist = []
        for _ in coms:
            comlist.append(_.device)
        #print(comlist)
        return comlist[0]
    use_port = _search_com_port()

    #  Initialize serial
    print("Open port")
    with serial.Serial(use_port, 9600) as ser:
        """
            1回じゃ送信を受け取って反映出来なかった
            Arduinoからの通信が帰ってくるまでは送信続けるとかのがええ
        """
        for _ in range(10):
            if send_str == "H":
                ser.write(b"1;")
                time.sleep(1)
            elif send_str == "L":
                ser.write(b"0;")
                time.sleep(1)
            elif send_str == "Q":
                ser.write(b"q;")
                time.sleep(1)        
    print("Close port")
    
"""
    メイン処理
"""
#if __name__ == "__main__":
def Object_Detection(loop):
    queue = Queue()
    qqqqq = Queue()
    p = Process(target=ard, args=(queue,))
    p2 = Process(target=ard_reset, args=(qqqqq,))
    p.start()
    p2.start()
    qqqqq.put("Q")

    """
    if loop is None:
        loop = asyncio.get_event_loop()
    loop2 = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(
        loop2, Output, 
        "/dev/ttyACM0",
        baudrate=9600,
        write_timeout=0.1)
    """

    #  Initialize args
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
    args = parse_args()

    #  Initialize video stream
    print("--------------------------------")
    #if not args.picamera:
    #  Set usb camera
    print("Use : usb camera")
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("H", "2", "6", "4"))
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    
    #  Camera error handling => 将来的にaseertに変更
    if cap.isOpened() == False:
        print("Cannot open")
        sys.exit(1)
    print("--------------------------------")

    #  Initialize engine
    engine = DetectionEngine(args.model)
    labels = dataset_utils.read_label_file(args.label) if args.label else None

    #  Start Capture
    print("Start Capture")
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

            if len(results) == 1:
                print(results)
                queue.put("H")
                #loop2.run_until_complete(coro)
            elif len(results) > 1:
                print(results)
                queue.put("L")
            else:
                pass
            """
                矩形の描画および表示
            """
            #  draw image
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
                
                cv2.imshow("Coral Live Object Detection", np.asarray(image))
                #return display_label
            draw_image(image, results, labels, args.maxobjects)
                
            #  closing confition
            if cv2.waitKey(5) & 0xFF == ord("q"):
                #  ループを永遠に続けたい場合
                loop.call_soon(Object_Detection, loop)
                #  ループを切るなら
                #loop.stop()
                break
        
    except KeyboardInterrupt:
        print("Exit loop by Ctrl-c")
        loop.stop()

    print("FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)))
    cap.release()
    cv2.destroyAllWindows()
    print("Stop Capture")
    #ser.close()
    #p.join()

if __name__ == "__main__":   
    loop = asyncio.get_event_loop()
    loop.call_soon(Object_Detection, loop)
    loop.run_forever()
    loop.close()
