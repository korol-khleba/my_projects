# библиотеки
import random
import math
import itertools
import matplotlib.pyplot as plt
import time 


# вычисление расстояния между точками
def distancer(point, sorted_point, i, j):
    point1 = point[i]
    point2 = sorted_point[j]
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


# считаем радиус вектор
def radius_vector(point):
    return math.sqrt(point[0]**2 + point[1]**2)

# проверка точек на коллинеарность
def are_points_collinear(check):
    x1, y1 = check[0]
    x2, y2 = check[1]
    x3, y3 = check[2]
    determinant = x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)
    return determinant


# считаем полярный угол
def get_angle(p):
    # вычисляем угол в радианах
    angle = math.atan2(p[1], p[0])
    
    # приводим угол к положительному значению в диапазоне от 0 до π
    if angle < 0:
        angle += 2 * math.pi
    if angle * 57.29580406904963> 180:
        angle = 2*math.pi - angle

    return angle * 57.29580406904963


# слияем списки по критерию
def merge_two_list(a, b):
    c = []
    i = j = 0
    while i < len(a) and j < len(b):
        a1 = a[i]
        a2 = b[j]
        # if radius_vector(a1) * math.sin(get_angle(a1)) < radius_vector(a2) * math.sin(get_angle(a2)):
        if a1[0] * a2[1] < a2[0] * a1[1]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1

    if i < len(a):
        c += a[i:] 

    if j < len(b):

        c += b[j:]

    return c


# сортировка слиянием
def merge_sort(s):
    if len(s) == 1:
        return s
    middle = len(s) // 2
    left = merge_sort(s[:middle])
    right = merge_sort(s[middle:])
    return merge_two_list(left, right) 


# считаем площадь треугольника
def calculate_area(p1, p2, p3):
    return round(abs(0.5 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))), 10)


# генерируем случайные числа
def generate_random_point(num_point):
    # здесь приравниваем значение к пустому списку
    point = []
    # генерация случайных координат c плавающей точкой в указанном диапазоне с округлением до одного знака 
    # _ значит что сами элементы списка не используются в цикле
    for _ in range(num_point):
        x = round(random.uniform(-10000, 10000), 1)  
        y = round(random.uniform(-10000, 10000), 1)
        # записываем сгенерированные координаты в конец списка
        point.append((x, y))
    return point


# поиск треугольника с минимальной площадью за O(n^2*log(n))
def find_minimum_area_triangle_1(point):
    # делаем переменную глобальной, чтобы потом вызвать ее для вывода ответа 
    global min_area 

    # приравниваем к максимально возможному числу с плавающей точкой, чтобы первая площадь, которую мы обнаружим, автоматически стала минимальной
    min_area = float('inf')

    # а здесь приравниваем значение списка к пустоте, а не к пустому списку
    min_triangle = None

    # проверка на адекватность данных
    if num_point < 3:
        print("NOT ENOUGH POINTS")
        return
    
    # фиксируем точку в пространстве
    for i in range(num_point):

        # передаем неотсортированный список (каждый раз по-новой, чтобы могли идти по исходному списку)
        sorted_point = list(point)
        sorted_point.pop(i)

        # передаем кортеж в список, чтобы могли итерировать  
        point1 = point[i]
        # print("\ni is", i, "\npoint is: ", point1)
        # print("sorted point before: ", sorted_point)

        # смещаем начало координат в точку point[i]
        for j in range(num_point - 1):

            # передаем кортеж в список, чтобы могли итерировать
            sorted_point1 = list(sorted_point[j])

            # смещаем начало координат
            sorted_point1[0] = sorted_point1[0] - point1[0]
            sorted_point1[1] = sorted_point1[1] - point1[1]

            # передаем обратно список в кортеж
            sorted_point[j] = tuple(sorted_point1)

        # сортируем по предикату x1 * y2 < x2 * y1
        sorted_point = list(merge_sort(sorted_point))
        #print("sorted point after: ", sorted_point)

        # возвращаем начало координат обратно
        for l in range(num_point - 1):
            sorted_point1 = list(sorted_point[l])
            sorted_point1[0] = sorted_point1[0] + point1[0]
            sorted_point1[1] = sorted_point1[1] + point1[1]
            sorted_point[l] = tuple(sorted_point1)

        #print("sorted point in the end: ", sorted_point)

        # ищем треугольник с минимальной площадью
        for t in range(num_point - 2):
            # попарно сравниваем 
            sorted_point2 = list(sorted_point[t])
            sorted_point3 = list(sorted_point[t + 1])

            # выводим пару точек
            #print(sorted_point2, sorted_point3)

            # находим треугольник с меньшей площадью - записываем значение площади, координаты найденного треугольника
            if calculate_area(point1, sorted_point2, sorted_point3) < min_area:
                min_area = calculate_area(point1, sorted_point2, sorted_point3)
                min_triangle = (point1, sorted_point2, sorted_point3)

    return min_triangle


# поиск треугольника с минимальной площадью за O(n^3)
def find_minimum_area_triangle_2(points):
    # делаем переменную глобальной, чтобы потом вызвать ее для вывода ответа 
    global minimum_area 
    # приравниваем к максимально возможному числу с плавающей точкой, чтобы первая площадь, которую мы обнаружим, автоматически стала минимальной
    minimum_area = float('inf')
    # а здесь приравниваем значение списка к пустоте, а не к пустому списку
    minimum_triangle = None
    # для всех возможных комбинаций из 3 точек (при этом не повторяя комбинаций)
    for p1, p2, p3 in itertools.combinations(points, 3):
        #print(f"AREA IS: {area}", p1, p2, p3)
        check = (p1, p2, p3)
        if (are_points_collinear(check)) != 0:
            area = calculate_area(p1, p2, p3)
            if area < minimum_area:
                minimum_area = area
                minimum_triangle = (p1, p2, p3)
    return minimum_triangle


# рисуем треугольники
def plot_triangles(triangles, colors):

    # создаем новый график
    fig, ax = plt.subplots()

    # проходимся по каждому треугольнику и его цвету
    for triangle, color in zip(triangles, colors):

         # извлекаем координаты каждой точки
        x = [point[0] for point in triangle]
        y = [point[1] for point in triangle]

        # добавляем первую точку в конец списка, чтобы замкнуть треугольник
        x.append(x[0])
        y.append(y[0])

        # используем аргумент color для задания цвета линии и закраски треугольника
        ax.plot(x, y, color=color)
        ax.fill(x, y, color=color, alpha = 0.1)




# ОСНОВНОЙ КОД  
# считываем число точек
num_point = int(input("ENTER NUMBER OF POINTS: "))

# генерируем случайный набор точек и выводим его
random_point = generate_random_point(num_point)
# print(f"GENERATED POINTS: {random_point}\n")

# поиск треугольника с минимальной площадью 1 способом
start_time = time.time()
min_triangle = find_minimum_area_triangle_1(random_point)
print(f"\nPOINTS OF 1 MIN AREA TRIANGLE ARE: {min_triangle}")
end_time = time.time() 
work_time = end_time - start_time
print("WORK TIME 1:", work_time)
print(f"MIN AREA 1 IS: {min_area}")


# поиск треугольника с минимальной площадью 2 способом
start_time = time.time()
minimum_triangle = find_minimum_area_triangle_2(random_point)
print(f"\nPOINTS OF 2 MININMUM AREA TRIANGLE ARE: {minimum_triangle}")
end_time = time.time() 
work_time = end_time - start_time
print("WORK TIME 2:", work_time)
print(f"MININMUM AREA 2 IS: {minimum_area}")

''' 
# рисуем все сгенерированные точки 
points_x, points_y = zip(*random_point)
plt.scatter(points_x, points_y, color='green')
plt.title('Random Points')

# рисуем найденные треугольники
# triangles = [min_triangle, minimum_triangle]
triangles = [min_triangle]
colors = ['red', 'yellow']
plot_triangles(triangles, colors)

plt.show()
'''


# функция для рисования всех точек и треугольников на одном графике
def plot_points_and_triangles(random_points, found_triangles):
    # извлекаем координаты x и y для каждой точки
    points_x, points_y = zip(*random_points)
    plt.scatter(points_x, points_y, color='green')  # рисуем все сгенерированные точки
    plt.title('Random Points')

    # проходимся по каждому треугольнику
    for triangle in found_triangles:
        # извлекаем координаты каждой точки
        x = [point[0] for point in triangle]
        y = [point[1] for point in triangle]

        # добавляем первую точку в конец списка, чтобы замкнуть треугольник
        x.append(x[0])
        y.append(y[0])

        # рисуем треугольники
        plt.plot(x, y, color='red')
        plt.fill(x, y, color='yellow', alpha=0.1)

    plt.show()


# вызовем функцию и передадим ей сгенерированные точки и найденный треугольник
plot_points_and_triangles(random_point, [minimum_triangle, min_triangle])