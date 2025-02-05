import matplotlib.pyplot as plt
import numpy as np

# Задаем точки для первого графика
x1 = np.array([12.5/60, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 3])
y1 = np.array([0.71, 0.85, 1.72, 2.6, 3.42, 4.2, 5, 9.7])

# Задаем точки для второго графика
x2 = np.array([12.5/60, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 3])
y2 = np.array([0.52, 0.8, 1.4, 2.2, 3, 3.6, 4.52, 8.6])

# Метод наименьших квадратов для первого графика
a1, b1 = np.polyfit(x1, y1, 1)
y_fit1 = a1 * x1 + b1

# Метод наименьших квадратов для второго графика
a2, b2 = np.polyfit(x2, y2, 1)
y_fit2 = a2 * x2 + b2

# Строим графики
plt.plot(x1, y1, 'bo', label = 'Точки графика 1')
plt.plot(x1, y_fit1, 'b-', label = 'Линия наименьших квадратов 1')
plt.plot(x2, y2, 'go', label = 'Точки графика 2')
plt.plot(x2, y_fit2, 'g-', label = 'Линия наименьших квадратов 2')

# Настройка графика
plt.xlabel('x')
plt.ylabel('y')
plt.title('Графики с методом наименьших квадратов')
plt.legend()
plt.grid(True)

# Отображение графика
plt.show()