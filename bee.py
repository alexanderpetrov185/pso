from all_functions import *
import random as rnd
import matplotlib.pyplot as plt
import imageio
import os

class Bee:
    def __init__(self, start, end, function):
        self.start = start
        self.end = end
        self.function = function
        self.position = self.get_initial_position()
        self.score = self.function(*self.position)
        self.best_position = self.position[:]
        self.best_score = self.score

    def get_initial_position(self):
        """ Метод для получения начальной позиции"""
        return [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]

    def explore(self):
        """ Метод для исследования новой позиции"""
        new_pos = [self.position[0] + rnd.uniform(-0.1, 0.1), self.position[1] + rnd.uniform(-0.1, 0.1)]
        new_score = self.function(*new_pos)
        if new_score < self.score:
            self.position = new_pos
            self.score = new_score
            if new_score < self.best_score:
                self.best_position = self.position[:]
                self.best_score = new_score

class BeeColony:
    def __init__(self, num_bees, elite_bees, iterations, function, start, end):
        self.num_bees = num_bees
        self.elite_bees = elite_bees
        self.iterations = iterations
        self.function = function
        self.start = start
        self.end = end
        self.bees = [Bee(start, end, function) for _ in range(self.num_bees)]
        self.global_best_score = float('inf')
        self.global_best_position = []

    def start_optimization(self):
        """ Запуск алгоритма пчел"""
        data_for_gif = []
        for _ in range(self.iterations):
            one_data_x = []
            one_data_y = []
            for bee in self.bees:
                bee.explore()
                one_data_x.append(bee.position[0])
                one_data_y.append(bee.position[1])
                if bee.score < self.global_best_score:
                    self.global_best_score = bee.score
                    self.global_best_position = bee.best_position[:]
            data_for_gif.append([one_data_x, one_data_y])

        # рисуем gif
        fnames = []
        i = 0
        for x, y in data_for_gif:
            i += 1
            fname = f"g{i}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Итерация: {i}")
            ax2.plot(x, y, 'ro')
            ax2.set_xlim(self.start, self.end)
            ax2.set_ylim(self.start, self.end)
            ax1.plot(x, y, 'ro')
            fig.savefig(fname)
            plt.close()
            fnames.append(fname)

        with imageio.get_writer('bee_colony.gif', mode='I') as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

# Пример использования
bee_colony = BeeColony(650, 50, 200, Ackley, -5, 5)
bee_colony.start_optimization()
print("РЕЗУЛЬТАТ:", bee_colony.global_best_score, "В ТОЧКЕ:", bee_colony.global_best_position)