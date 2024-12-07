import random as rnd
import matplotlib.pyplot as plt
import imageio
import os
from all_functions import Ackley  # Ваша функция

class Ant:
    def __init__(self, start, end, alpha, beta, function):
        self.start = start
        self.end = end
        self.alpha = alpha
        self.beta = beta
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

        # Улучшение движения к лучшему решению
        self.position = [
            rnd.uniform(self.start, self.end) * 0.2 + 0.8 * self.best_position[0],
            rnd.uniform(self.start, self.end) * 0.2 + 0.8 * self.best_position[1]
        ]
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
        self.pheromones = [1.0] * num_ants  # Изначально феромоны одинаковы
        self.ants = [Ant(start, end, alpha, beta, function) for _ in range(num_ants)]
        self.global_best_score = float('inf')
        self.global_best_position = []

    def update_pheromones(self):
        """ Метод обновления феромонов"""
        for i, ant in enumerate(self.ants):
            if ant.best_score < self.global_best_score:
                self.global_best_score = ant.best_score
                self.global_best_position = ant.best_position[:]
            # Усиление феромонов на основе лучших результатов
            self.pheromones[i] = (
                (1 - self.evaporation_rate) * self.pheromones[i] +
                (1 / (1 + ant.best_score))  # Пропорционально лучшей оценке муравья
            )

    def start_optimization(self):
        """ Запуск алгоритма муравьиной колонии"""
        data_for_gif = []
        for iteration in range(self.iterations):
            one_data_x = []
            one_data_y = []
            for ant in self.ants:
                heuristic_info = [1 / (1 + ant.score) for ant in self.ants]  # Зависимость от текущих оценок
                ant.update_position(self.pheromones, heuristic_info)
                one_data_x.append(ant.position[0])
                one_data_y.append(ant.position[1])
            self.update_pheromones()
            data_for_gif.append([one_data_x, one_data_y])

        # Создание GIF с вашей системой координат
        fnames = []
        for i, (x, y) in enumerate(data_for_gif, 1):
            fname = f"ACO{i}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Итерация: {i}")

            # Левый график
            ax1.plot(x, y, 'ro')

            # Правый график
            ax2.plot(x, y, 'ro')
            ax2.set_xlim(self.start, self.end)
            ax2.set_ylim(self.start, self.end)

            fig.savefig(fname)
            plt.close()
            fnames.append(fname)

        with imageio.get_writer('ant_colony.gif', mode='I') as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)


# Тестирование
aco = AntColony(
    num_ants=200,  # Увеличено количество муравьев для более точного поиска
    alpha=1, 
    beta=5,  # Усиление влияния эвристической информации
    evaporation_rate=0.05,  # Более медленное испарение феромонов
    iterations=300,  # Увеличено количество итераций
    function=Ackley,
    start=-5,
    end=5
)
aco.start_optimization()
print("РЕЗУЛЬТАТ:", aco.global_best_score, "В ТОЧКЕ:", aco.global_best_position)
