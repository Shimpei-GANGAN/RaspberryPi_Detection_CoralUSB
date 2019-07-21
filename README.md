# RaspberryPi_Detection_CoralUSB
Raspberry Pi 3 Model B+でCoral USB アクセラレータを使用したリアルタイム物体検出・顔検出を実行する。

## ソース詳細
- <b>capute_detection.py</b>

Coral USB アクセラレータを使用したリアルタイム物体検出・リアルタイム顔検出用。入力モデルで物体検出と顔検出をスイッチング。

- <b>capute_detection_pyserial.py</b>

Coral USB アクセラレータを使用したリアルタイム物体検出・リアルタイム顔検出用。入力モデルで物体検出と顔検出をスイッチング。
検出結果はPyserialを用いてArduinoに送信し、結果に合わせて処理を行う。

## デモ等に関する公開記事はこちらより
- https://gangannikki.hatenadiary.jp/entry/2019/07/20/230000

-  
