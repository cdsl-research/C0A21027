# ESP32でMicroPythonを用いて，KXM52-1050(加速度センサ)，L3GD20H(ジャイロセンサ)を利用する．
## ESP32_KXM52-1050_L3GD20H_micropython.py
### 概要
ESP32でMicroPythonを利用して加速度と角速度を得るために，加速度センサ(KXM52-1050)，ジャイロセンサ(L3GD20H)を利用します．
以下のモジュールをインポートしています．
from machine import ADC, PWM, Pin, I2C
impot time
Thoonyで開くことを前提にしており，Ctrl + Cでデータの取得を終了するようにしています．
### KXM52-1050とESP32の接続方法
* 1PIN ESP32の3.3V電源および，KXM52-1050の2PIN
* 2PIN KXM52-1050の1PIN
* 3PIN ESP32のGNDおよび，KXM52-1050の4PIN
* 4PIN KXM52-1050の3PIN
* 5PIN なし
* 6PIN ESP32の34PIN
* 7PIN ESP32の39PIN
* 8PIN ESP32の36PIN
### L3GD20HとESP32の接続方法
* 1PIN ESP32の3.3V電源および，10k抵抗を利用してL3GD20Hの5PIN
* 2PIN ESP32の22PIN
* 3PIN ESP32の21PIN
* 4PIN L3GD20Hの8PIN
* 5PIN 10k抵抗を利用してL3GD20Hの1PIN
* 6PIN なし
* 7PIN なし
* 8PIN ESP32のGDNおよび，L3GD20Hの4PIN
### 出力されるファイル
data.txtという名前のファイルが作成され，データが記述されます．
左から順に
* 計測開始からの経過時間 [ms]
* x軸加速度 [m/s^2]
* y軸加速度 [m/s^2]
* z軸加速度 [m/s^2]
* x軸角速度 [deg/s]
* y軸角速度 [deg/s]
* z軸角速度 [deg/s]  
というデータになっています．
