from all_functions import *
import random as rnd
import matplotlib.pyplot as plt
import imageio
import os

class Ant:
    def __init__(self, start, end, alpha, beta, function):
        # область поиска
        self.start = start
        self.end = end
        self.alpha = alpha  # влияние феромона
        self.beta = beta  # влияние эвристической информации
        self.function = function
        self.position = self.get_initial_position()
        self.score = self.function(*self.position)
        self.best_position = self.position[:]
        self.best_score = self.score

    def get_initial_position(self):
        """ Метод для получения начальной позиции"""
        return [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]

    def update_position(self, pheromones, heuristic_info):
        """ Обновление позиции на основе феромонов и эвристики"""
        probabilities = []
        for p, h in zip(pheromones, heuristic_info):
            probabilities.append((p ** self.alpha) * (h ** self.beta))
        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]

        # Рулетка для выбора новой позиции
        choice = rnd.choices(range(len(probabilities)), probabilities)[0]
        new_pos = [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]
        self.position = new_pos
        self.score = self.function(*self.position)
        if self.score < self.best_score:
            self.best_position = self.position[:]
            self.best_score = self.score

class AntColony:
    def __init__(self, num_ants, alpha, beta, evaporation_rate, iterations, function, start, end):
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.iterations = iterations
        self.function = function
        self.start = start
        self.end = end
        self.pheromones = [1.0] * self.num_ants
        self.ants = [Ant(start, end, alpha, beta, function) for _ in range(self.num_ants)]
        self.global_best_score = float('inf')
        self.global_best_position = []

    def update_pheromones(self):
        """ Метод обновления феромонов"""
        for ant in self.ants:
            if ant.best_score < self.global_best_score:
                self.global_best_score = ant.best_score
                self.global_best_position = ant.best_position[:]
        for i in range(len(self.pheromones)):
            self.pheromones[i] = (1 - self.evaporation_rate) * self.pheromones[i] + (1 / (1 + self.global_best_score))

    def start_optimization(self):
        """ Запуск алгоритма муравьиной колонии"""
        data_for_gif = []
        for _ in range(self.iterations):
            one_data_x = []
            one_data_y = []
            for ant in self.ants:
                heuristic_info = [1 / (1 + ant.score) for _ in range(self.num_ants)]
                ant.update_position(self.pheromones, heuristic_info)
                one_data_x.append(ant.position[0])
                one_data_y.append(ant.position[1])
            self.update_pheromones()
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

        with imageio.get_writer('ant_colony.gif', mode='I') as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

# Пример использования
aco = AntColony(650, 1, 2, 0.5, 200, Ackley, -5, 5)
aco.start_optimization()
print("РЕЗУЛЬТАТ:", aco.global_best_score, "В ТОЧКЕ:", aco.global_best_position)