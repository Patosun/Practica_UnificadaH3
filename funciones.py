import math


PERMITIDOS = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
PERMITIDOS.update({"abs": abs, "ln": math.log})


def crear_funcion(texto):

    expresion = texto.strip().replace("^", "**")
    codigo = compile(expresion, "<f(x)>", "eval")
    for nombre in codigo.co_names:
        if nombre != "x" and nombre not in PERMITIDOS:
            raise ValueError(f"Nombre no permitido en la función: {nombre}")

    def f(x):
        return eval(codigo, {"__builtins__": {}}, {**PERMITIDOS, "x": x})

    return f


def leer_funcion(mensaje="f(x) = "):

    while True:
        texto = input(mensaje)
        try:
            f = crear_funcion(texto)
            return f, texto.strip()
        except (SyntaxError, ValueError) as e:
            print(f"Función no válida ({e}). Ejemplo: exp(-x^2) o sin(x)/x")


def leer_lista(mensaje):

    return [float(v) for v in input(mensaje).replace(",", " ").split()]


def leer_nodos():

    print("Nodos de interpolación:")
    print("  1) Equiespaciados en [a, b] con n intervalos (n + 1 puntos)")
    print("  2) Escribir los valores x0 x1 ... xn")
    if input("Opción: ").strip() == "2":
        return leer_lista("x0 x1 ... xn: ")
    a = float(input("a = "))
    b = float(input("b = "))
    n = int(input("n = "))
    return [a + i * (b - a) / n for i in range(n + 1)]


EJERCICIOS = {
    "1": ("f(x) = e^(-x^2) en [0.1, 10]", "exp(-x^2)", 0.1, 10.0),
}


def particion(f, a, b, n):


    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    F = [f(xi) for xi in x]
    return x, F, h


def imprimir_particion(x, F, h):

    n = len(x) - 1
    print(f"\nPartición: n = {n} subintervalos,  h = {h:g}")
    print(f"{'i':>4} | {'x_i':>12} | {'f_i':>16}")
    for i, (xi, fi) in enumerate(zip(x, F)):
        print(f"{i:>4} | {xi:>12.6g} | {fi:>16.8e}")
    print("x = [" + ", ".join(f"{v:.6g}" for v in x) + "]")
    print("F = [" + ", ".join(f"{v:.6g}" for v in F) + "]")


def leer_ejercicio():

    print("Ejercicios:")
    for clave, (descripcion, *_resto) in EJERCICIOS.items():
        print(f"  {clave}) {descripcion}")
    clave = input("Ejercicio: ").strip()
    if clave not in EJERCICIOS:
        clave = next(iter(EJERCICIOS))
    descripcion, texto, a, b = EJERCICIOS[clave]
    n = int(input(f"Número de subintervalos n para [{a:g}, {b:g}]: "))
    if n <= 0:
        raise ValueError("n debe ser positivo")
    funcion = crear_funcion(texto)
    x, F, h = particion(funcion, a, b, n)
    imprimir_particion(x, F, h)
    return descripcion, funcion, x, F


def evaluar_en_nodos(f, x):

    valores = []
    for xi in x:
        try:
            valores.append(float(f(xi)))
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            raise ValueError(f"f no se puede evaluar en x = {xi:g} ({e})")
    return valores


def leer_csv(ruta):


    import csv

    x, f = [], []
    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        contenido = archivo.read()
    separador = ";" if contenido.count(";") > contenido.count(",") else ","
    for numero, fila in enumerate(csv.reader(contenido.splitlines(), delimiter=separador), start=1):
        fila = [c.strip() for c in fila if c.strip()]
        if not fila:
            continue
        try:
            xi, fi = float(fila[0]), float(fila[1])
        except (ValueError, IndexError):
            if numero == 1:
                continue
            raise ValueError(f"{ruta}, línea {numero}: fila no válida {fila}")
        x.append(xi)
        f.append(fi)

    if len(set(x)) != len(x):
        raise ValueError(f"{ruta}: hay valores de x repetidos")

    pares = sorted(zip(x, f))
    return [p[0] for p in pares], [p[1] for p in pares]


def pedir_csv(argumentos):


    ruta = argumentos[1] if len(argumentos) > 1 else input("Ruta del archivo .csv: ").strip().strip("'\"")
    return ruta, leer_csv(ruta)
