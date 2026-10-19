from diferencias_divididas import EJEMPLO_CLASE, tabla_diferencias_divididas, evaluar_newton
from funciones import leer_funcion, leer_lista, leer_nodos, evaluar_en_nodos, pedir_csv, leer_ejercicio
from graficas import graficar_interpolacion, argumentos


def gauss(A, b):


    n = len(b)
    M = [fila[:] + [b[i]] for i, fila in enumerate(A)]
    for k in range(n):
        p = max(range(k, n), key=lambda r: abs(M[r][k]))
        if abs(M[p][k]) < 1e-14:
            raise ValueError("Sistema singular")
        M[k], M[p] = M[p], M[k]
        for r in range(k + 1, n):
            m = M[r][k] / M[k][k]
            for c in range(k, n + 1):
                M[r][c] -= m * M[k][c]
    sol = [0.0] * n
    for k in range(n - 1, -1, -1):
        sol[k] = (M[k][n] - sum(M[k][c] * sol[c] for c in range(k + 1, n))) / M[k][k]
    return sol


def fila_valor(t):
    return [t ** 3, t ** 2, t, 1.0]


def fila_d1(t):
    return [3 * t ** 2, 2 * t, 1.0, 0.0]


def fila_d2(t):
    return [6 * t, 2.0, 0.0, 0.0]


def splines_cubicos_naturales(x, f):

    n = len(x) - 1
    N = 4 * n
    A = []
    b = []

    def ecuacion(bloques, rhs):

        fila = [0.0] * N
        for i, coefs in bloques:
            for j in range(4):
                fila[4 * i + j] += coefs[j]
        A.append(fila)
        b.append(rhs)


    for i in range(n):
        ecuacion([(i, fila_valor(x[i]))], f[i])
        ecuacion([(i, fila_valor(x[i + 1]))], f[i + 1])


    for i in range(1, n):
        ecuacion([(i - 1, fila_d1(x[i])), (i, [-v for v in fila_d1(x[i])])], 0.0)
        ecuacion([(i - 1, fila_d2(x[i])), (i, [-v for v in fila_d2(x[i])])], 0.0)


    ecuacion([(0, fila_d2(x[0]))], 0.0)
    ecuacion([(n - 1, fila_d2(x[n]))], 0.0)

    sol = gauss(A, b)
    return [tuple(sol[4 * i:4 * i + 4]) for i in range(n)]


def evaluar_spline(splines, x, t):


    i = 0
    while i < len(splines) - 1 and t > x[i + 1]:
        i += 1
    a, b, c, d = splines[i]
    return a * t ** 3 + b * t ** 2 + c * t + d


def imprimir_splines(splines, x):

    for i, (a, b, c, d) in enumerate(splines):
        print(f"S_{i},{i + 1}(x) = {a:.6g}x^3 {b:+.6g}x^2 {c:+.6g}x {d:+.6g}"
              f"   en [{x[i]:g}, {x[i + 1]:g}]")


def resolver(nombre, x, f, evaluar, funcion=None):

    if len(x) < 2 or len(x) != len(f):
        print(f"\n{nombre}: se necesitan al menos 2 puntos y la misma cantidad de x y f.")
        return
    if any(x[i] >= x[i + 1] for i in range(len(x) - 1)):
        print(f"\n{nombre}: se requiere x_i < x_(i+1).")
        return

    splines = splines_cubicos_naturales(x, f)
    _, coef = tabla_diferencias_divididas(x, f)

    print(f"\n===== {nombre} =====")
    imprimir_splines(splines, x)

    if evaluar:
        if funcion is None:
            print(f"\n{'x':>10} | {'Spline':>12} | {'Dif. divid.':>12} | {'Diferencia':>12}")
            for t in evaluar:
                s = evaluar_spline(splines, x, t)
                p = evaluar_newton(coef, x, t)
                print(f"{t:>10.6g} | {s:>12.6f} | {p:>12.6f} | {abs(s - p):>12.3e}")
        else:
            print(f"\n{'x':>10} | {'f(x) real':>12} | {'Spline':>12} | {'error':>10} | {'Dif. divid.':>12} | {'error':>10}")
            for t in evaluar:
                r = funcion(t)
                s = evaluar_spline(splines, x, t)
                p = evaluar_newton(coef, x, t)
                print(f"{t:>10.6g} | {r:>12.6f} | {s:>12.6f} | {abs(s - r):>10.3e} | {p:>12.6f} | {abs(p - r):>10.3e}")

    if funcion is not None:

        m = 1000
        ts = [x[0] + (x[-1] - x[0]) * k / m for k in range(m + 1)]
        err_s = max(abs(evaluar_spline(splines, x, t) - funcion(t)) for t in ts)
        err_p = max(abs(evaluar_newton(coef, x, t) - funcion(t)) for t in ts)
        print(f"\nError máximo en [{x[0]:g}, {x[-1]:g}]:  spline = {err_s:.3e},  dif. divididas = {err_p:.3e}")

    graficar_interpolacion(f"Splines vs Newton - {nombre}", x, f,
                           [("Spline cúbico natural", lambda t: evaluar_spline(splines, x, t)),
                            (f"Newton P_{len(x) - 1}(x)", lambda t: evaluar_newton(coef, x, t))],
                           evaluar, funcion)


def desde_csv():

    try:
        ruta, (x, f) = pedir_csv(argumentos())
    except (OSError, ValueError) as e:
        print(f"No se pudo leer el archivo: {e}")
        return
    print(f"Leídos {len(x)} puntos de {ruta}")
    evaluar = leer_lista("Puntos a evaluar (opcional, Enter para omitir): ")
    resolver(ruta, x, f, evaluar)


def main():
    print("Splines cúbicos naturales vs diferencias divididas")
    if len(argumentos()) > 1:

        desde_csv()
        return

    print("0) Leer datos de un archivo .csv (columnas x, f)")
    print("1) Interpolar una función f(x) cualquiera")
    print("2) Ingresar una tabla de datos (x, f)")
    print("3) Ejemplo de clase")
    print("4) Ejercicios de clase (f(x) en [a, b] con n subintervalos)")
    opcion = input("Opción: ").strip()

    if opcion == "0":
        desde_csv()
    elif opcion == "1":
        funcion, texto = leer_funcion()
        x = sorted(leer_nodos())
        try:
            f = evaluar_en_nodos(funcion, x)
        except ValueError as e:
            print(e)
            return
        evaluar = leer_lista("Puntos donde estimar f(x) (opcional): ")
        resolver(f"f(x) = {texto}", x, f, evaluar, funcion)
    elif opcion == "2":
        x = leer_lista("Valores x0 x1 ... xn (crecientes): ")
        f = leer_lista("Valores f0 f1 ... fn: ")
        evaluar = leer_lista("Puntos a evaluar (opcional): ")
        resolver("Datos ingresados", x, f, evaluar)
    elif opcion == "4":
        try:
            descripcion, funcion, x, F = leer_ejercicio()
        except ValueError as e:
            print(e)
            return
        evaluar = leer_lista("Puntos donde estimar f(x) (opcional): ")
        resolver(descripcion, x, F, evaluar, funcion)
    else:
        resolver("Ejemplo de clase (14/9)", **EJEMPLO_CLASE)


if __name__ == "__main__":
    main()
