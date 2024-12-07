from math import *
import random as rnd
import matplotlib.pyplot as plt
import imageio
import os
from all_functions import Ackley  # Подключаем тестовые функции


class HybridOptimizer:
    def __init__(self, function, start, end, step_size, perturbation_rate, meta_iters, grad_iters):
        # Функция для оптимизации
        self.function = function
        # Границы поиска
        self.start = start
        self.end = end
        # Размер шага градиентного спуска
        self.step_size = step_size
        # Вероятность случайного изменения (метаэвристика)
        self.perturbation_rate = perturbation_rate
        # Количество итераций для метаэвристики
        self.meta_iters = meta_iters
        # Количество итераций градиентного спуска
        self.grad_iters = grad_iters
        # Текущая позиция
        self.position = [rnd.uniform(start, end), rnd.uniform(start, end)]
        self.best_position = self.position[:]
        self.best_score = self.function(*self.position)

    def gradient(self, position):
        """ Метод для приближенного вычисления градиента с помощью численной дифференциации """
        epsilon = 1e-8  # Малое значение для вычисления производной
        grad = []
        for i in range(len(position)):
            pos1 = position[:]
            pos2 = position[:]
            pos1[i] += epsilon
            pos2[i] -= epsilon
            grad.append((self.function(*pos1) - self.function(*pos2)) / (2 * epsilon))
        return grad

    def update_position(self):
        """ Метод для выполнения шага оптимизации """
        for _ in range(self.grad_iters):
            grad = self.gradient(self.position)
            self.position = [
                max(self.start, min(self.end, self.position[i] - self.step_size * grad[i]))
                for i in range(len(self.position))
            ]
            score = self.function(*self.position)
            if score < self.best_score:
                self.best_score = score
                self.best_position = self.position[:]

        # Метахевристика: случайное "возмущение" позиции
        if rnd.random() < self.perturbation_rate:
            self.position = [
                rnd.uniform(self.start, self.end) if rnd.random() < 0.5 else coord
                for coord in self.position
            ]
            score = self.function(*self.position)
            if score < self.best_score:
                self.best_score = score
                self.best_position = self.position[:]


class HybridGradientMetaSearch:
    def __init__(self, function, start, end, step_size, perturbation_rate, meta_iters, grad_iters, total_iters):
        # Гибридный оптимизатор
        self.optimizer = HybridOptimizer(function, start, end, step_size, perturbation_rate, meta_iters, grad_iters)
        # Общее количество итераций
        self.total_iters = total_iters
        # Для визуализации
        self.data_for_gif = []

    def run(self):
        """ Запуск алгоритма """
        for _ in range(self.total_iters):
            self.optimizer.update_position()
            self.data_for_gif.append(self.optimizer.position[:])

    def save_gif(self):
        """ Создание и сохранение GIF """
        fnames = []
        for i, position in enumerate(self.data_for_gif, 1):
            fname = f"hybrid{i}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Итерация: {i}")

            # Левый график: без ограничений масштаба
            ax1.plot(position[0], position[1], 'ro')

            # Правый график: с фиксированным масштабом
            ax2.plot(position[0], position[1], 'ro')
            ax2.set_xlim(self.optimizer.start, self.optimizer.end)
            ax2.set_ylim(self.optimizer.start, self.optimizer.end)

            fig.savefig(fname)
            plt.close()
            fnames.append(fname)

        # Сохранение GIF
        with imageio.get_writer("hybrid_gradient_meta_search.gif", mode="I") as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        # Удаление временных файлов
        for filename in fnames:
            os.remove(filename)


# Настройка и запуск
hybrid_search = HybridGradientMetaSearch(
    function=Ackley,  # Функция для оптимизации
    start=-5,
    end=5,
    step_size=0.1,  # Размер шага градиентного спуска
    perturbation_rate=0.2,  # Вероятность случайного возмущения
    meta_iters=5,  # Итерации метаэвристики
    grad_iters=5,  # Итерации градиентного спуска
    total_iters=200,  # Общее количество итераций
)
hybrid_search.run()
hybrid_search.save_gif()

print("РЕЗУЛЬТАТ:", hybrid_search.optimizer.best_score, "В ТОЧКЕ:", hybrid_search.optimizer.best_position)
