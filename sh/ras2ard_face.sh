#!/bin/sh

cd ~/edgetpu/

echo "Start Face Detection"
python3.5 ~/RaspberryPi_Detection_CoralUSB/py/ras2ard_face.py \
--model test_data/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite \
--keep_aspect_ratio
