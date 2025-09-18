import hebi
import numpy as np
from time import sleep
import os
import shutil
import scipy.io as sio
import csv
import uuid

freq = 10
lookup = hebi.Lookup()
sleep(2)
group = lookup.get_group_from_names("HEBI", "mobileIO")
group.feedback_frequency = freq
groupFeedback = hebi.GroupFeedback(group.size)

os.makedirs("logs", exist_ok=True)
os.makedirs("logs/cache", exist_ok=True)

logFile = group.start_log("logs", "currentLog.hebilog")

time, gyro, accelerometer = [], [], []

while True:
    fbk = group.get_next_feedback(reuse_fbk=None)
    if fbk is None:
        break

    t = fbk.receive_time[0]
    g = np.array(fbk.gyro[0]).flatten()
    a = np.array(fbk.accelerometer[0]).flatten()

    time.append(t)
    gyro.append(g)
    accelerometer.append(a)

    print("Data")
    print("Time:", t)
    print("Gyro:", g)
    print("Accelerometer:", a)
    print("")
    sleep(1/freq)

time = np.array(time)
gyro = np.vstack(gyro)
accelerometer = np.vstack(accelerometer)

mat_path = "logs/currentLog.mat"
sio.savemat(mat_path, {'time': time, 'gyro': gyro, 'accelerometer': accelerometer})

unique_id = str(uuid.uuid4())
cache_folder = f"logs/cache/{unique_id}"
os.makedirs(cache_folder, exist_ok=True)

csv_path = f"{cache_folder}/recording_{unique_id}.csv"
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time','Gyro X','Gyro Y','Gyro Z','Accel X','Accel Y','Accel Z'])
    for i in range(len(time)):
        writer.writerow([time[i], gyro[i,0], gyro[i,1], gyro[i,2], accelerometer[i,0], accelerometer[i,1], accelerometer[i,2]])

shutil.copy("logs/currentLog.mat", cache_folder)
shutil.copy("logs/currentLog.hebilog", cache_folder)

group.stop_log()
print(f"Saved logs/currentLog.mat, logs/currentLog.hebilog, and cache folder {cache_folder}")
print("DONE!")
