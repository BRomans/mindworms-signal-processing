import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y1_vals = []
y2_vals = []

index = count()

def animate(i):
    x_vals.append(next(index))
    y1_vals.append(random.randint(-3,2))
    y2_vals.append(random.randint(0,5))

    plt.cla() 
    
    plt.plot(x_vals, y1_vals, label="Channel 1")
    plt.plot(x_vals, y2_vals, label="Channel 2")

    plt.legend(loc='upper right')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(),animate,interval=1000)

plt.show()