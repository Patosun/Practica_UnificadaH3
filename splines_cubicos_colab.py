import numpy as np
import matplotlib.pyplot as plt

def cubic_spline(x, f):
    n = len(x) - 1
    h = np.diff(x)


    a = np.array(f)


    A = np.zeros((n + 1, n + 1))
    B = np.zeros(n + 1)

    A[0, 0] = 1
    A[n, n] = 1

    for i in range(1, n):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        B[i] = 3 * ((a[i + 1] - a[i]) / h[i] - (a[i] - a[i - 1]) / h[i - 1])


    c = np.linalg.solve(A, B)


    b = np.zeros(n)
    d = np.zeros(n)
    for i in range(n):
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])
        b[i] = (a[i + 1] - a[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3

    return a[:-1], b, c[:-1], d

def evaluate_spline(x_points, f_points, a, b, c, d, t):
    if not (x_points[0] <= t <= x_points[-1]):
        raise ValueError("El punto t debe estar dentro del rango de x_points.")


    i = np.searchsorted(x_points, t) - 1
    if i < 0: i = 0
    if i >= len(x_points) - 1: i = len(x_points) - 2

    delta_x = t - x_points[i]
    return a[i] + b[i] * delta_x + c[i] * delta_x**2 + d[i] * delta_x**3


x = np.array([0, 1, 2, 3])
f = np.array([0, 1, 0, 1])


a, b, c, d = cubic_spline(x, f)

print("Coeficientes a:", a)
print("Coeficientes b:", b)
print("Coeficientes c:", c)
print("Coeficientes d:", d)


t_eval = np.linspace(x.min(), x.max(), 100)
y_eval = [evaluate_spline(x, f, a, b, c, d, ti) for ti in t_eval]


plt.figure(figsize=(10, 6))
plt.plot(x, f, 'o', label='Puntos de datos originales')
plt.plot(t_eval, y_eval, '-', label='Spline cúbico interpolado')
plt.title('Interpolación con Splines Cúbicos Naturales')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()
