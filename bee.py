from all_functions import *
from math import *
import random as rnd
import matplotlib.pyplot as plt
import imageio
import os

class Bee:
    def __init__(self, start, end, function):
        self.start = start
        self.end = end
        self.function = function
        self.position = self.get_random_position()
        self.score = self.function(*self.position)

    def get_random_position(self):
        return [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]

    def explore(self, radius):
        """Локальное исследование вокруг текущей позиции."""
        new_position = [
            self.position[0] + rnd.uniform(-radius, radius),
            self.position[1] + rnd.uniform(-radius, radius)
        ]
        # Ограничение позиции в области поиска
        new_position[0] = min(max(new_position[0], self.start), self.end)
        new_position[1] = min(max(new_position[1], self.start), self.end)

        new_score = self.function(*new_position)
        if new_score < self.score:
            self.position = new_position
            self.score = new_score

    def reset_position(self):
        self.position = self.get_random_position()
        self.score = self.function(*self.position)


class BeeColony:
    def __init__(self, num_scouts, num_workers, num_iterations, radius, function, start, end):
        self.num_scouts = num_scouts
        self.num_workers = num_workers
        self.num_iterations = num_iterations
        self.radius = radius
        self.function = function
        self.start = start
        self.end = end

        # Создание разведчиков и сборщиков
        self.scouts = [Bee(start, end, function) for _ in range(num_scouts)]
        self.workers = [Bee(start, end, function) for _ in range(num_workers)]

        # Глобально лучшее решение
        self.global_best_position = None
        self.global_best_score = float('inf')

    def update_global_best(self):
        for bee in self.scouts + self.workers:
            if bee.score < self.global_best_score:
                self.global_best_score = bee.score
                self.global_best_position = bee.position

    def start_optimization(self):
        data_for_gif = []

        for iteration in range(self.num_iterations):
            # Разведчики исследуют новые области
            for scout in self.scouts:
                scout.reset_position()

            # Сборщики выполняют локальный поиск вокруг разведчиков
            for worker, scout in zip(self.workers, self.scouts):
                worker.position = scout.position[:]
                worker.score = scout.score
                worker.explore(self.radius)

            # Обновляем глобально лучшее решение
            self.update_global_best()

            # Сохраняем позиции для визуализации
            scout_positions = [scout.position for scout in self.scouts]
            worker_positions = [worker.position for worker in self.workers]
            data_for_gif.append((scout_positions, worker_positions))

        # Создаем GIF
        self.create_gif(data_for_gif)
        print("РЕЗУЛЬТАТ:", self.global_best_score, "В ТОЧКЕ:", self.global_best_position)

    def create_gif(self, data_for_gif):
        fnames = []
        for i, (scouts, workers) in enumerate(data_for_gif):
            fname = f"bee{i + 1}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
            fig.suptitle(f"Итерация: {i + 1}")

            # Скауты красные, сборщики синие
            ax1.plot([s[0] for s in scouts], [s[1] for s in scouts], 'ro', label='Scouts')
            ax1.plot([w[0] for w in workers], [w[1] for w in workers], 'bo', label='Workers')
            ax1.legend(loc="upper left")

            ax2.plot([s[0] for s in scouts], [s[1] for s in scouts], 'ro')
            ax2.plot([w[0] for w in workers], [w[1] for w in workers], 'bo')
            ax2.set_xlim(self.start, self.end)
            ax2.set_ylim(self.start, self.end)

            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
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
colony = BeeColony(
    num_scouts=10,
    num_workers=20,
    num_iterations=200,  # Увеличено число итераций для точности
    radius=0.3,          # Уменьшен радиус для более детального исследования
    function=Ackley,
    start=-5,
    end=5
)
colony.start_optimization()
