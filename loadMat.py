import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

mat_path = "logs/currentLog.mat"
data = sio.loadmat(mat_path)

time = np.array(data['time']).flatten()
gyro = np.array(data['gyro'])
accelerometer = np.array(data['accelerometer'])

axis_labels = ['X', 'Y', 'Z']
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8), sharex=True)

lines_gyro = []
for i in range(3):
    line, = ax1.plot(time, gyro[:, i], label=axis_labels[i])
    lines_gyro.append(line)
ax1.set_ylabel('Gyro (rad/s)')
ax1.set_title('Gyroscope Data')
ax1.grid(True)
leg1 = ax1.legend(loc='upper right', fancybox=True, shadow=True)

lines_accel = []
for i in range(3):
    line, = ax2.plot(time, accelerometer[:, i], label=axis_labels[i])
    lines_accel.append(line)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Acceleration (m/s²)')
ax2.set_title('Accelerometer Data')
ax2.grid(True)
leg2 = ax2.legend(loc='upper right', fancybox=True, shadow=True)

def make_legend_interactive(fig, legend, lines):
    lined = dict()
    for legline, origline in zip(legend.get_lines(), lines):
        legline.set_picker(5)
        lined[legline] = origline
    def on_pick(event):
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()
    fig.canvas.mpl_connect('pick_event', on_pick)

make_legend_interactive(fig, leg1, lines_gyro)
make_legend_interactive(fig, leg2, lines_accel)

plt.tight_layout()
plt.show()
