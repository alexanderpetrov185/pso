from all_functions import *
from math import *
import random as rnd
import matplotlib.pyplot as plt
import imageio
import os


class Agent:
    def __init__(self, start, end, function, alpha, beta, gamma):
        # Параметры
        self.start = start
        self.end = end
        self.function = function
        self.alpha = alpha  # Вес собственного управления
        self.beta = beta    # Вес управления соседями
        self.gamma = gamma  # Вес целевой точки

        # Начальная позиция
        self.currentPos = self.getRandomPos()
        self.velocity = [0, 0]

        # Локальная и глобальная цели
        self.localGoal = self.currentPos[:]
        self.localScore = self.function(*self.localGoal)

    def getRandomPos(self):
        """ Метод для генерации случайной начальной позиции """
        return [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]

    def update(self, globalGoal, neighbors):
        """ Метод для обновления позиции агента """
        # Рассчитать вектор к глобальной цели
        goalVector = [globalGoal[0] - self.currentPos[0], globalGoal[1] - self.currentPos[1]]

        # Рассчитать вектор влияния соседей
        if neighbors:
            avgNeighborPos = [sum(n[0] for n in neighbors) / len(neighbors),
                              sum(n[1] for n in neighbors) / len(neighbors)]
            neighborVector = [avgNeighborPos[0] - self.currentPos[0], avgNeighborPos[1] - self.currentPos[1]]
        else:
            neighborVector = [0, 0]

        # Рассчитать новое управление
        self.velocity = [
            self.alpha * self.velocity[0] + self.beta * neighborVector[0] + self.gamma * goalVector[0],
            self.alpha * self.velocity[1] + self.beta * neighborVector[1] + self.gamma * goalVector[1]
        ]

        # Обновить позицию
        self.currentPos = [self.currentPos[0] + self.velocity[0], self.currentPos[1] + self.velocity[1]]

        # Обновить локальную цель
        score = self.function(*self.currentPos)
        if score < self.localScore:
            self.localGoal = self.currentPos[:]
            self.localScore = score


class DMPC:
    def __init__(self, size, function, start, end, alpha, beta, gamma, iterations):
        self.size = size
        self.function = function
        self.start = start
        self.end = end
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.iterations = iterations

        # Глобальная цель
        self.globalGoal = None
        self.globalScore = float('inf')

        # Создаём агентов
        self.agents = [Agent(start, end, function, alpha, beta, gamma) for _ in range(size)]

    def run(self):
        """ Запуск алгоритма """
        dataForGIF = []

        for _ in range(self.iterations):
            # Обновить глобальную цель
            for agent in self.agents:
                if agent.localScore < self.globalScore:
                    self.globalGoal = agent.localGoal
                    self.globalScore = agent.localScore

            # Обновить позиции агентов
            oneDataX, oneDataY = [], []
            for i, agent in enumerate(self.agents):
                # Соседи агента
                neighbors = [self.agents[j].currentPos for j in range(self.size) if j != i]
                agent.update(self.globalGoal, neighbors)
                oneDataX.append(agent.currentPos[0])
                oneDataY.append(agent.currentPos[1])

            dataForGIF.append([oneDataX, oneDataY])

        # Построить гифку
        self.createGIF(dataForGIF)

    def createGIF(self, dataForGIF):
        """ Создание гифки с результатами """
        fnames = []
        for i, (x, y) in enumerate(dataForGIF):
            fname = f"dmpc{i + 1}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Итерация: {i + 1}")

            # Без фиксированного масштаба
            ax1.plot(x, y, 'ro')
            ax1.set_title("Без фикс. масштаба")

            # С фиксированным масштабом
            ax2.plot(x, y, 'ro')
            ax2.set_xlim(self.start, self.end)
            ax2.set_ylim(self.start, self.end)
            ax2.set_title("С фикс. масштабом")

            fig.savefig(fname)
            plt.close()
            fnames.append(fname)

        with imageio.get_writer('dmpc.gif', mode='I') as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)


# Пример использования
dmpc = DMPC(size=50, function=Ackley, start=-5, end=5, alpha=0.5, beta=0.3, gamma=0.2, iterations=200)
dmpc.run()
print("РЕЗУЛЬТАТ:", dmpc.globalScore, "В ТОЧКЕ:", dmpc.globalGoal)
