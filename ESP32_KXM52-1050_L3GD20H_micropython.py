# 必要なモジュールをインポートする
from machine import ADC, PWM, Pin, I2C
import time

# センサから取得したデータを加速度[m/s^2]に変換する
def kasoku(v):
    V = v * (3.55 / 65535)
    ag = (V - 1.65) / 660 * 1000
    a = ag * 9.8
    return a

###################################################################
#角速度変数

# データを取得するESP-32のピンを設定する
p21 = Pin(21, Pin.IN, Pin.PULL_UP)
p22 = Pin(22, Pin.IN, Pin.PULL_UP)

# I2C通信を行うピンの設定を行う
i2c = I2C(scl=Pin(22), sda=Pin(21))  # sclピンとsdaピンを使用

# デバイスのI2Cアドレス
device_address = 0x6A  # 書き込み先アドレスを指定する変数

# データを書き込む
data_to_write = b'\x0F'  # 書き込むデータをバイト列で指定
i2c.writeto_mem(device_address, 0x20, data_to_write)
data_to_write = b'\x20'
i2c.writeto_mem(device_address, 0x23, data_to_write)

# 読み込み先アドレスを格納する変数
ANGULAR_VELOCITY_REG = 0x28

####################################################################

# 経過時間を調べるためにデータ取得開始時間を取得する
first_time = time.ticks_ms()

# 取得データの書き込み先のファイルを開く
f = open('data_test.txt', 'w')

# Ctrl + Cで停止させた後に、ファイルに書き込むためにtry文でwhileを回す
try:
    while True:
        #########################################################################################
        #3軸それぞれの加速度データ受け取り
        z = ADC(Pin(36, Pin.IN), atten=ADC.ATTN_11DB)
        y = ADC(Pin(39, Pin.IN), atten=ADC.ATTN_11DB)
        x = ADC(Pin(34, Pin.IN), atten=ADC.ATTN_11DB)

        # 0-65535の範囲の整数を返す
        x_v = x.read_u16()
        y_v = y.read_u16()
        z_v = z.read_u16()
        nowtime = time.ticks_ms() - first_time
        
        # センサデータを加速度[m/s^2]へ変換する
        x_val = kasoku(x_v)
        y_val = kasoku(y_v)
        z_val = kasoku(z_v)
        #########################################################################################
        #角速度データ受け取り
        xl = i2c.readfrom_mem(device_address, 0x28, 1)
        xh = i2c.readfrom_mem(device_address, 0x29, 1)
        yl = i2c.readfrom_mem(device_address, 0x2A, 1)
        yh = i2c.readfrom_mem(device_address, 0x2B, 1)
        zl = i2c.readfrom_mem(device_address, 0x2C, 1)
        zh = i2c.readfrom_mem(device_address, 0x2D, 1)
        
        # センサデータを、合成する
        wx = xh[0] << 8 | xl[0]
        wy = yh[0] << 8 | yl[0]
        wz = zh[0] << 8 | zl[0]
        
        if wx >= 32768:
            wx = wx - 65536
        if wy >= 32768:
            wy = wy - 65536
        if wz >= 32768:
            wz = wz - 65536
        
        angular_velocity_x = wx * 0.07
        angular_velocity_y = wy * 0.07
        angular_velocity_z = wz * 0.07
        #########################################################################################
        
        f.write(str(nowtime) + ", " + str(x_val) + ", " + str(y_val) + ", " + str(z_val) + ", " + str(angular_velocity_x) + ", " + str(angular_velocity_y) + ", " + str(angular_velocity_z) + "\n")
        print(str(nowtime) + ", X: " + str(x_val) + ", Y: " + str(y_val) + ", Z:" + str(z_val))
        
        time.sleep(0.03)
finally:
    f.close()
