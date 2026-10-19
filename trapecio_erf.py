import math


def f(t):

    return math.exp(-t ** 2)


def trapecio(f, a, b, n):

    h = (b - a) / n
    f0 = f(a)
    fn = f(b)
    suma = sum(f(a + i * h) for i in range(1, n))
    A = (h / 2) * (f0 + fn + 2 * suma)
    return A, h, f0, fn, suma


def main():
    a = float(input("Límite inferior a (ej. 0): "))
    b = float(input("Límite superior b = x (ej. 1): "))
    n = int(input("Número de subintervalos n (ej. 10): "))

    A, h, f0, fn, suma = trapecio(f, a, b, n)


    erf_aprox = 2 / math.sqrt(math.pi) * A
    promedio = A / (b - a)

    print("\nMétodo del trapecio")
    print(f"h = (b - a) / n = ({b} - {a}) / {n} = {h}")
    print(f"f0 = {f0}")
    print(f"fn = {fn}")
    print(f"Σ f(xi), i=1..n-1 = {suma}")
    print(f"\nA = h/2 [f0 + fn + 2·Σ] = {h}/2 [{f0} + {fn} + 2·{suma}]")
    print(f"A ≈ {A}")
    print(f"\nPromedio de f en [a, b] = A / (b - a) ≈ {promedio}")
    print(f"erf({b}) ≈ 2/√π · A = {erf_aprox}")
    print(f"erf({b}) real (math.erf) = {math.erf(b)}")
    print(f"Error absoluto = {abs(erf_aprox - math.erf(b))}")


if __name__ == "__main__":
    main()
