import math


def f(t):

    return math.sin(t ** 2)


def simpson_13(f, a, b, n):

    h = (b - a) / n
    f0 = f(a)
    fn = f(b)
    suma_impares = sum(f(a + i * h) for i in range(1, n, 2))
    suma_pares = sum(f(a + i * h) for i in range(2, n, 2))
    A = (h / 3) * (f0 + fn + 4 * suma_impares + 2 * suma_pares)
    return A, h, f0, fn, suma_impares, suma_pares


def fresnel_s_serie(x, terminos=40):

    return sum((-1) ** k * x ** (4 * k + 3) / (math.factorial(2 * k + 1) * (4 * k + 3))
               for k in range(terminos))


def main():
    a = float(input("Límite inferior a (ej. 0): "))
    b = float(input("Límite superior b = x (ej. 1): "))
    n = int(input("Número de subintervalos n, PAR (ej. 10): "))

    if n <= 0 or n % 2 != 0:
        print("Error: Simpson 1/3 requiere que n sea un entero par positivo.")
        return

    A, h, f0, fn, s_imp, s_par = simpson_13(f, a, b, n)

    print("\nMétodo de Simpson 1/3")
    print(f"h = (b - a) / n = ({b} - {a}) / {n} = {h}")
    print(f"f0 = {f0}")
    print(f"fn = {fn}")
    print(f"Σ impares (f1 + f3 + ... + f{n-1}) = {s_imp}")
    print(f"Σ pares   (f2 + f4 + ... + f{n-2}) = {s_par}")
    print(f"\nA = h/3 [f0 + fn + 4(Σ impares) + 2(Σ pares)]")
    print(f"A = {h}/3 [{f0} + {fn} + 4({s_imp}) + 2({s_par})]")
    print(f"A ≈ {A}")


    if a == 0:
        ref = fresnel_s_serie(b)
        print(f"\nS({b}) por serie de Taylor = {ref}")
        print(f"Error absoluto = {abs(A - ref)}")


if __name__ == "__main__":
    main()
