# RaspberryPi_Detection_CoralUSB
Raspberry Pi 3 Model B+でCoral USB アクセラレータを使用したリアルタイム物体検出・顔検出を実行する。


## ソース詳細
### capute_detection.py

Coral USB アクセラレータを使用したリアルタイム物体検出・リアルタイム顔検出用。入力モデルを指定することで物体検出と顔検出をスイッチング可能。
imutis.video.VideoStreamを使用。

### Example (Running under edgetpu repo's root directory):
    # Face Detection
    python3 ~/RaspberryPi_Detection_CoralUSB/capture_detection.py \
    --model test_data/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite \
    --keep_aspect_ratio

    # Object Detection(Coco)
    python3 ~/RaspberryPi_Detection_CoralUSB/capture_detection.py \
    --model test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
    --label coco_labels.txt \
    --keep_aspect_ratio

*** 

### capute_detection_cv2.py

Coral USB アクセラレータを使用したリアルタイム物体検出・リアルタイム顔検出用。入力モデルを指定することで物体検出と顔検出をスイッチング可能。
cv2.VideoCaptureを使用。

### Example (Running under edgetpu repo's root directory):
    # Face Detection
    python3 ~/RaspberryPi_Detection_CoralUSB/capture_detection_cv2.py \
    --model test_data/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite \
    --keep_aspect_ratio

    # Object Detection(Coco)
    python3 ~/RaspberryPi_Detection_CoralUSB/capture_detection_cv2.py \
    --model test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
    --label coco_labels.txt \
    --keep_aspect_ratio

***
## デモ等に関する公開記事はこちらより
- https://gangannikki.hatenadiary.jp/entry/2019/07/20/230000

- https://gangannikki.hatenadiary.jp/entry/2019/07/24/190000

