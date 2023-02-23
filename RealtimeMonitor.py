import queue
import threading
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

sensorDataQueue = queue.Queue()

# 센서 값 읽기 쓰래드 함수
def serialSensorRead():
    while True:
        serialData = ser.readline().decode()

        accelX, accelY, accelZ, gyroX, gyroY, gyroZ, magX, magY, magZ = serialData.split(',')

        accelX = float(accelX)
        accelY = float(accelY)
        accelZ = float(accelZ)

        gyroX = float(gyroX)
        gyroY = float(gyroY)
        gyroZ = float(gyroZ)

        magX = float(magX)
        magY = float(magY)
        magZ = float(magZ)

        sensorDataQueue.put((float(accelX), float(accelY), float(accelZ), float(gyroX), float(gyroY), float(gyroZ), float(magX), float(magY), float(magZ)))

# 시리얼 통신 포트와 속도 설정
ser = serial.Serial("/dev/cu.usbmodem1103", 115200) 
max_points = 100

# 그래프 설정
fig = plt.figure()
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.5)

accelAxes = fig.add_subplot(3, 1, 1, xlim=(0, max_points), ylim=(-3.0, 3.0))
gyroAxes = fig.add_subplot(3, 1, 2, xlim=(0, max_points), ylim=(-300.0, 300.0))
magAxes = fig.add_subplot(3, 1, 3, xlim=(0, max_points), ylim=(-200.0, 200.0))

accelAxes.set_title('Accelation')
accelLineX, = accelAxes.plot([], [], lw=2)
accelLineX, = accelAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='red', label='x')
accelLineY, = accelAxes.plot([], [], lw=2)
accelLineY, = accelAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='green', label='y')
accelLineZ, = accelAxes.plot([], [], lw=2)
accelLineZ, = accelAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='blue', label='z')
accelAxes.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

gyroAxes.set_title('Gyroscope')
gyroLineX, = gyroAxes.plot([], [], lw=2)
gyroLineX, = gyroAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='red', label='x')
gyroLineY, = gyroAxes.plot([], [], lw=2)
gyroLineY, = gyroAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='green', label='y')
gyroLineZ, = gyroAxes.plot([], [], lw=2)
gyroLineZ, = gyroAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='blue', label='z')
gyroAxes.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

magAxes.set_title('Magnet')
magLineX, = magAxes.plot([], [], lw=2)
magLineX, = magAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='red', label='x')
magLineY, = magAxes.plot([], [], lw=2)
magLineY, = magAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='green', label='y')
magLineZ, = magAxes.plot([], [], lw=2)
magLineZ, = magAxes.plot(np.arange(max_points), np.ones(max_points, dtype=np.float64)*np.nan, lw=2, color='blue', label='z')
magAxes.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

def init():
    return accelLineX, accelLineY, accelLineZ, gyroLineX, gyroLineY, gyroLineZ, magLineX, magLineY, magLineZ

# 큐에 쌓인 데이터 통합하여 반환. 그래프에 한번에 적용하여 속도 증대.
def getAllSensorDataOnQueue():
    accelXBunch = []
    accelYBunch = []
    accelZBunch = []
    gyroXBunch = []
    gyroYBunch = []
    gyroZBunch = []
    magXBunch = []
    magYBunch = []
    magZBunch = []
    while not sensorDataQueue.empty():
        accelX, accelY, accelZ, gyroX, gyroY, gyroZ, magX, magY, magZ = sensorDataQueue.get_nowait()
        accelXBunch.append(accelX)
        accelYBunch.append(accelY)
        accelZBunch.append(accelZ)
        gyroXBunch.append(gyroX)
        gyroYBunch.append(gyroY)
        gyroZBunch.append(gyroZ)
        magXBunch.append(magX)
        magYBunch.append(magY)
        magZBunch.append(magZ)
    return tuple(accelXBunch), tuple(accelYBunch), tuple(accelZBunch), tuple(gyroXBunch), tuple(gyroYBunch), tuple(gyroZBunch), tuple(magXBunch), tuple(magYBunch), tuple(magZBunch)

# 그래프 업데이트 함수
def animate(i):
    accelX, accelY, accelZ, gyroX, gyroY, gyroZ, magX, magY, magZ = getAllSensorDataOnQueue()
    if (accelX.count == 0):
        return

    # accel
    oldAccelX = accelLineX.get_ydata()
    newAccelX = np.r_[oldAccelX[1:], accelX]
    accelLineX.set_ydata(newAccelX)

    oldAccelY = accelLineY.get_ydata()
    newAccelY = np.r_[oldAccelY[1:], accelY]
    accelLineY.set_ydata(newAccelY)

    oldAccelZ = accelLineZ.get_ydata()
    newAccelZ = np.r_[oldAccelZ[1:], accelZ]
    accelLineZ.set_ydata(newAccelZ)

    # gyro
    oldGyroX = gyroLineX.get_ydata()
    newGyroX = np.r_[oldGyroX[1:], gyroX]
    gyroLineX.set_ydata(newGyroX)

    oldGyroY = gyroLineY.get_ydata()
    newGyroY = np.r_[oldGyroY[1:], gyroY]
    gyroLineY.set_ydata(newGyroY)

    oldGyroZ = gyroLineZ.get_ydata()
    newGyroZ = np.r_[oldGyroZ[1:], gyroZ]
    gyroLineZ.set_ydata(newGyroZ)

    # mag
    oldMagX = magLineX.get_ydata()
    newMagX = np.r_[oldMagX[1:], magX]
    magLineX.set_ydata(newMagX)

    oldMagY = magLineY.get_ydata()
    newMagY = np.r_[oldMagY[1:], magY]
    magLineY.set_ydata(newMagY)

    oldMagZ = magLineZ.get_ydata()
    newMagZ = np.r_[oldMagZ[1:], magZ]
    magLineZ.set_ydata(newMagZ)

    return accelLineX, accelLineY, accelLineZ, gyroLineX, gyroLineY, gyroLineZ, magLineX, magLineY, magLineZ

# 시리얼 통신 센서값 읽기 함수 쓰래드 등록 및 시작
serialSensorReadThread = threading.Thread(target=serialSensorRead, daemon=True)
serialSensorReadThread.start()

# 그래프 업데이트 등록 및 시작
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=False)
plt.show()