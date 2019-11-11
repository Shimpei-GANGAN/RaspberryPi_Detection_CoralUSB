#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   November  11  21:00, 2019 (Mon)
#------------------------------------------------------------
#
#   Raspberry Pi + Coral USB ACCELERATOR
#   Coral USBを用いたリアルタイム物体検出・顔検出
#
#   本プログラムではcv2.VideoCapture()を使用
#------------------------------------------------------------

import cv2 
import numpy as np
import argparse
import time
import sys
import serial

from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from PIL import Image, ImageDraw, ImageFont

"""
    矩形の描画および表示
"""
def draw_image(image, results, labels):
    set_font = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"
    result_size = len(results)

    for idx, obj in enumerate(results):
        #  Prepare image for drawing
        draw = ImageDraw.Draw(image)

        #  Prepare boundary box
        box = obj.bounding_box.flatten().tolist()

        #  Draw rectangle to desired thickness
        for x in range( 0, 4 ):
            draw.rectangle(box, outline=(0, 0, 255))

        #  Annotate image with label and confidence score
        if labels:
            display_str = labels[obj.label_id] + ": " + str(round(obj.score*100, 2)) + "%"
            draw.text((box[0], box[1]), display_str, font=ImageFont.truetype(set_font, 20))

    displayImage = np.asarray(image)
    cv2.imshow("Coral Live Object Detection", displayImage)


"""
    Argumentsの設定
"""
def setting_argument():
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
        help="Use PiCamera for image capture", default=False)
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
    メイン処理
"""
def main():
    #  Set up args
    args = setting_argument()

    #  Initialize engine
    engine = DetectionEngine(args.model)
    labels = dataset_utils.read_label_file(args.label) if args.label else None

    #  Initialize video stream
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("H", "2", "6", "4"))
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

    #  Camera error handling
    if cap.isOpened() == False:
        print("Cannot open")
        sys.exit(1)

    #  Initialize Serial
    ser = serial.Serial("/dev/ttyACM0", 115200)

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

            #  draw image
            draw_image(image, results, labels)

            #  closing confition
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Exit loop by Ctrl-c")
    
    print("FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)))
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
