import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2, 2, figsize=(5, 5))

data0 = np.linspace(0, 1, 100)
data1 = np.linspace(1, 2, 100)
data2 = np.linspace(2, 3, 100)
data3 = np.linspace(3, 4, 100)

func0 = 1 / 6 * data0 ** 3
func1 = 1 / 6 * (1 + 3 * (data1 - 1) + 3 * (data1 - 1) ** 2 - 3 * (data1 - 1) ** 3)
func2 = 1 / 6 * (4 - 6 * (data2 - 2) ** 2 + 3 * (data2 - 2) ** 3)
func3 = 1 / 6 * (1 - 3 * (data3 - 3) + 3 * (data3 - 3) ** 2 - (data3 - 3) ** 3)

axs[0, 0].plot(data0, func0, 'C3')
axs[0, 1].plot(data1, func1, 'C2')
axs[1, 0].plot(data2, func2, 'C1')
axs[1, 1].plot(data3, func3, 'C4')

axs[0, 0].set_title("p1(t)")
axs[0, 1].set_title("p2(t)")
axs[1, 0].set_title("p3(t)")
axs[1, 1].set_title("p4(t)")

plt.show()
