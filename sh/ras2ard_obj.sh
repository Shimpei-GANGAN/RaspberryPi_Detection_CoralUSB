#!/bin/sh

cd ~/edgetpu/

echo "Start Object Detection"
python3.5 ~/RaspberryPi_Detection_CoralUSB/ras2ard.py \
--model test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
--label test_data/coco_labels.txt \
--keep_aspect_ratio
