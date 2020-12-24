import tkinter as tk
from cProfile import label

import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

Writer = animation.writers['pillow']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

root = tk.Tk()
# Propriedades da simulaçãodims = 0
N = 1000
T = 1.0
dt0 = T / np.sqrt(N)
dt1 = float(T) / N
dt2 = T / (N - 1)
numPaths = 3
mu = 0.2
sigma = 0.3
legend = ['Browniano normal', 'Browniano geometrico', 'Browniano ponte']


def maior(lista):
    x = 0
    for i in lista:
        if x < i:
            x = i
    return x


def menor(lista):
    x = 0
    for i in lista:
        if x > i:
            x = i
    return x


def geracaoAleatoriadeGBM(dt):
    def Solucao():
        t = np.linspace(0, T, N)
        W = np.random.normal(size=N)
        A = np.cumsum(W) * np.sqrt(dt)*mu*t
        return np.exp((mu - 0.5 * sigma ** 2) * t + sigma  * A)

    lineData = np.vstack((Solucao(), Solucao(), Solucao()))

    return lineData


def geracaoAleatoriadeBB(dt):
    def Solucao():
        dt_sqrt = np.sqrt(dt)
        B = np.empty(N)
        B[0] = 0
        for n in range(0, N - 1, 1):
            t = np.random.uniform(-1, 1) * dt
            T = np.random.uniform(-1, 1) * dt_sqrt
            B[n + 1] = B[n] * (1 - t * dt / (1 - t)) + T
        return B

    lineData = np.vstack((Solucao(), Solucao(), Solucao()))
    return lineData


def geracaoAleatoriadeBN(dt):
    dX = np.sqrt(dt) * np.random.randn(1, N)
    X = np.cumsum(dX, axis=1)

    dY = np.sqrt(dt) * np.random.randn(1, N)
    Y = np.cumsum(dY, axis=1)

    dZ = np.sqrt(dt) * np.random.randn(1, N)
    Z = np.cumsum(dZ, axis=1)

    lineData = np.vstack((X, Y, Z))
    return lineData


def updateLinhas(num, dataLines, lines, dims):
    for u, v in zip(lines, dataLines):
        if dims == 2:
            u.set_data(v[0:2, :num])

        elif dims == 3:
            u.set_data(v[0:2, :num])
            u.set_3d_properties(v[2, :num])

    return lines


data = []
for index in range(numPaths):
    if index == 0:
        data.append(geracaoAleatoriadeBN(dt0))
    elif index == 1:
        data.append(geracaoAleatoriadeGBM(dt1))
    else:
        data.append(geracaoAleatoriadeBB(dt2))


def maior_entre_movimentos(valor1, valor2):
    if (valor1 > valor2):
        return valor1
    else:
        return valor2


def menor_entre_movimentos(valor1, valor2):
    if (valor1 < valor2):
        return valor1
    else:
        return valor2


def click2d():
    fig = plt.figure()
    fig.suptitle('2D Movimentos Brownianos', fontsize=14)

    ax = plt.axes(
        xlim=(menor_entre_movimentos(menor(data[0][0]), menor(data[1][0])) - 1,
              maior_entre_movimentos(maior(data[0][0]), maior(data[1][0])) + 1),
        ylim=(menor_entre_movimentos(menor(data[0][1]), menor(data[1][1])) - 1,
              maior_entre_movimentos(maior(data[0][1]), maior(data[1][1])) + 1))
    ax.set_xlabel('X(t)')
    ax.set_ylabel('Y(t)')

    lines = [ax.plot(dat[0, 0:1], dat[1, 0:1])[0] for dat in data]
    anim = animation.FuncAnimation(fig, updateLinhas, N + 1, fargs=(data, lines, 2),
                                   interval=30, repeat=False, blit=False)

    do_later()


def click3d():
    fig = plt.figure()
    fig.suptitle('3D Movimentos Brownianos', fontsize=14)
    ax = p3.Axes3D(fig)
    ax.set_xlim3d([menor_entre_movimentos(menor(data[0][0]), menor(data[1][0])) - 1,
                   maior_entre_movimentos(maior(data[0][0]), maior(data[1][0])) + 1])
    ax.set_xlabel('X(t)')

    ax.set_ylim3d([menor_entre_movimentos(menor(data[0][1]), menor(data[1][1])) - 1,
                   maior_entre_movimentos(maior(data[0][1]), maior(data[1][1])) + 1])
    ax.set_ylabel('Y(t)')

    ax.set_zlim3d([menor_entre_movimentos(menor(data[0][2]), menor(data[1][2])) - 1,
                   maior_entre_movimentos(maior(data[0][2]), maior(data[1][2])) + 1])
    ax.set_zlabel('Z(t)')


    lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]
    anim = animation.FuncAnimation(fig, updateLinhas, N + 1, fargs=(data, lines, 3),
                                   interval=30, repeat=False, blit=False)

    do_later()


btn2d = tk.Button(root, text='2D', command=click2d)
btn2d.pack()
btn3d = tk.Button(root, text='3D', command=click3d)
btn3d.pack()


def do_later():
    btn2d.destroy()
    btn3d.destroy()
    root.destroy()
    plt.legend(legend, loc=3)
    plt.tight_layout()
    plt.show()


root.mainloop()
