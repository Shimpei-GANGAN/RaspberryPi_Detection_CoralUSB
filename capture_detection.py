
import cv2 
import numpy as np
import argparse, time, re

from edgetpu.detection.engine import DetectionEngine
from PIL import Image, ImageDraw, ImageFont

from imutils.video import FPS
from imutils.video import VideoStream


def ReadLabelFile(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret


def draw_image(image, results, labels):
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
            draw.text((box[0], box[1]), display_str, font=ImageFont.truetype("/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf", 20))

        displayImage = np.asarray(image)
        cv2.imshow("Coral Live Object Detection", displayImage)

def 



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", help="Path of the detection model.", required=True)
    parser.add_argument(
        "--label", help="Path of the labels file.")
    parser.add_argument(
        "--maxobjects", type=int, default=3, help="Maximum objects")
    parser.add_argument(
        "--threshold", type=float, default=0.3, help="Minimum threshold")
    parser.add_argument(
        "--picamera", action="store_true",
        help="Use PiCamera for image capture", default=False)
    args = parser.parse_args()

    #  Prepare labels.
    labels = ReadLabelFile(args.label) if args.label else None
    #  Initialize engine
    engine = DetectionEngine(args.model)

    #  Initialize video stream
    vs = VideoStream(usePiCamera=args.picamera, resolution=(640, 480)).start()
    time.sleep(1)

    fps = FPS().start()

    while True:
        try:
            #  Read frame from video
            screenshot = vs.read()
            image = Image.fromarray(screenshot)

            #  Perform inference
            results = engine.DetectWithImage(image, threshold=args.threshold,
                                             keep_aspect_ratio=True,
                                             relative_coord=False,
                                             top_k=args.maxobjects)

            #  draw image
            draw_image(image, results, labels)

            #  closing confition
            if cv2.waitKey(5) & 0xFF == ord("q"):
                fps.stop()
                break

            fps.update()
        except KeyboardInterrupt:
            fps.stop()
            break
    
    print("Elapsed time: {}".format(str(fps.elapsed())))
    print("Approx FPS: {}".format(str(fps.fps())))

    cv2.destroyAllWindows()
    vs.stop()
    time.sleep(2)

    
if __name__ == "__main__":
    main()
