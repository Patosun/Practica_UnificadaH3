import os
import sys

SIN_VENTANA = "--sin-ventana" in sys.argv
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficas")
MAX_FIGURAS = 60


AZUL = "#6C9BD2"
ROSA = "#E58C9A"
MENTA = "#79BF9C"
MIEL = "#E3B26A"
COLORES = [AZUL, ROSA, MENTA, MIEL]
RELLENO = {AZUL: "#C9DCF2", ROSA: "#F7D3D9"}
TINTA = "#4B4B5C"
SUAVE = "#CFC6BA"

ESTILO = {
    "figure.facecolor": "#FBF7F0",
    "axes.facecolor": "#FFFDF8",
    "savefig.facecolor": "#FBF7F0",
    "axes.edgecolor": SUAVE,
    "axes.linewidth": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
    "axes.titlecolor": TINTA,
    "axes.labelcolor": TINTA,
    "axes.grid": True,
    "grid.color": "#EDE6DB",
    "grid.linestyle": "-",
    "grid.linewidth": 0.8,
    "xtick.color": "#8A8578",
    "ytick.color": "#8A8578",
    "text.color": TINTA,
    "font.family": "DejaVu Sans",
    "legend.frameon": True,
    "legend.fancybox": True,
    "legend.framealpha": 0.9,
    "legend.facecolor": "#FFFFFF",
    "legend.edgecolor": "#EDE6DB",
    "lines.solid_capstyle": "round",
    "figure.titleweight": "bold",
    "figure.titlesize": 14,
}


def argumentos():


    return [a for a in sys.argv if not a.startswith("--")]


def _pyplot():

    try:
        import matplotlib
        if SIN_VENTANA:
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams.update(ESTILO)
        return plt
    except ImportError:
        print("(matplotlib no está instalado: se omite la gráfica)")
        return None


def _guardar(plt, fig, titulo):

    os.makedirs(CARPETA, exist_ok=True)
    nombre = "".join(c if c.isalnum() else "_" for c in titulo)
    nombre = "_".join(p for p in nombre.split("_") if p)[:80]
    ruta = os.path.join(CARPETA, nombre + ".png")
    fig.tight_layout()
    fig.savefig(ruta, dpi=130)
    print(f"Gráfica guardada en {ruta}")
    if not SIN_VENTANA:
        plt.show()
    plt.close(fig)


def _muestreo(a, b, m=600):

    return [a + (b - a) * k / m for k in range(m + 1)]


def _evaluar_seguro(g, ts):

    ys = []
    for t in ts:
        try:
            ys.append(float(g(t)))
        except (ValueError, ZeroDivisionError, OverflowError):
            ys.append(float("nan"))
    return ys


def graficar_interpolacion(titulo, x, f, curvas, evaluar=(), funcion=None):

    plt = _pyplot()
    if plt is None:
        return

    a = min([x[0]] + list(evaluar))
    b = max([x[-1]] + list(evaluar))
    ts = _muestreo(a, b)
    colores = COLORES

    if funcion is not None:
        fig, (ax, ax_err) = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True,
                                         gridspec_kw={"height_ratios": [3, 2]})
    else:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax_err = None

    if funcion is not None:
        ax.plot(ts, _evaluar_seguro(funcion, ts), color=SUAVE, lw=6, alpha=0.7, label="f(x) real")

    for k, (etiqueta, g) in enumerate(curvas):
        color = colores[k % len(colores)]
        estilo = "-" if k == 0 else "--"
        ax.plot(ts, _evaluar_seguro(g, ts), estilo, color=color, lw=2.4, label=etiqueta)
        for t in evaluar:
            y = g(t)
            ax.plot([t], [y], "D", color=color, ms=8, mec="white", mew=1.5, zorder=5)
            ax.annotate(f"{y:.4g}", (t, y), textcoords="offset points",
                        xytext=(8, 8 if k == 0 else -16), fontsize=8.5, color=color,
                        fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8, alpha=0.9))

    ax.plot(x, f, "o", color=TINTA, ms=7, mec="white", mew=1.5, zorder=6, label="Nodos (x_i, f_i)")
    for t in evaluar:
        ax.axvline(t, color=SUAVE, ls="--", lw=1)

    ax.set_title(titulo)
    ax.set_ylabel("f(x)")
    ax.grid(True)
    ax.legend(loc="best", fontsize=9)

    if ax_err is not None:
        real = _evaluar_seguro(funcion, ts)
        for k, (etiqueta, g) in enumerate(curvas):
            err = [abs(p - r) if p == p and r == r else float("nan")
                   for p, r in zip(_evaluar_seguro(g, ts), real)]

            err = [e if e > 1e-16 else 1e-16 for e in err]
            ax_err.semilogy(ts, err, color=colores[k % len(colores)], lw=1.8, label=etiqueta)
        ax_err.set_ylabel("|P(x) − f(x)|")
        ax_err.set_xlabel("x")
        ax_err.grid(True, which="major")
        ax_err.legend(loc="best", fontsize=9)
    else:
        ax.set_xlabel("x")

    _guardar(plt, fig, titulo)


def _parabola(x0, x1, x2, y0, y1, y2):


    def p(t):
        return (y0 * (t - x1) * (t - x2) / ((x0 - x1) * (x0 - x2))
                + y1 * (t - x0) * (t - x2) / ((x1 - x0) * (x1 - x2))
                + y2 * (t - x0) * (t - x1) / ((x2 - x0) * (x2 - x1)))
    return p


def _dibujar_curva(ax, f, a, b, etiqueta):

    margen = 0.05 * (b - a)
    ts = _muestreo(a - margen, b + margen)
    ax.plot(ts, _evaluar_seguro(f, ts), color=TINTA, lw=2.2, label=etiqueta, zorder=4)
    ax.axhline(0, color=SUAVE, lw=1)
    ax.grid(True)
    ax.set_xlabel("x")


def graficar_integracion(titulo, f, a, b, n, A_t, A_s, exacto, etiqueta_f,
                         ns, err_t, err_s):

    plt = _pyplot()
    if plt is None:
        return

    h = (b - a) / n
    xs = [a + i * h for i in range(n + 1)]
    ys = _evaluar_seguro(f, xs)

    fig, (ax_t, ax_s, ax_c) = plt.subplots(1, 3, figsize=(16, 5))


    _dibujar_curva(ax_t, f, a, b, etiqueta_f)
    if n <= MAX_FIGURAS:
        for i in range(n):
            ax_t.fill([xs[i], xs[i], xs[i + 1], xs[i + 1]], [0, ys[i], ys[i + 1], 0],
                      facecolor=RELLENO[AZUL], edgecolor=AZUL, lw=1.2)
        ax_t.plot(xs, ys, "o", color=AZUL, ms=6, mec="white", mew=1.2, zorder=5)
    else:
        ax_t.fill_between(xs, ys, color=RELLENO[AZUL])
    ax_t.set_title(f"Trapecio (n = {n})\nA ≈ {A_t:.10f}   error = {abs(A_t - exacto):.2e}")
    ax_t.legend(fontsize=8)


    _dibujar_curva(ax_s, f, a, b, etiqueta_f)
    if A_s is None:
        ax_s.set_title(f"Simpson 1/3: no aplica\n(n = {n} es impar)")
    else:
        for k in range(0, n, 2):
            p = _parabola(xs[k], xs[k + 1], xs[k + 2], ys[k], ys[k + 1], ys[k + 2])
            ts = _muestreo(xs[k], xs[k + 2], 40)
            pt = [p(t) for t in ts]
            ax_s.fill_between(ts, pt, color=RELLENO[ROSA], lw=0)
            if n <= MAX_FIGURAS:
                ax_s.plot(ts, pt, color=ROSA, lw=1.4)
                ax_s.plot([xs[k + 2]] * 2, [0, ys[k + 2]], color=ROSA, lw=1.2)
        if n <= MAX_FIGURAS:
            ax_s.plot(xs, ys, "o", color=ROSA, ms=6, mec="white", mew=1.2, zorder=5)
        ax_s.set_title(f"Simpson 1/3 (n = {n}, {n // 2} parábolas)\n"
                       f"A ≈ {A_s:.10f}   error = {abs(A_s - exacto):.2e}")
    ax_s.legend(fontsize=8)


    hs = [(b - a) / m for m in ns]
    piso = 1e-16
    ax_c.loglog(ns, [max(e, piso) for e in err_t], "o-", color=AZUL, lw=2.2, ms=7, mec="white", mew=1.2, label="Trapecio")
    ax_c.loglog(ns, [max(e, piso) for e in err_s], "s-", color=ROSA, lw=2.2, ms=7, mec="white", mew=1.2, label="Simpson 1/3")

    if err_t[0] > 0:
        ax_c.loglog(ns, [err_t[0] * (hh / hs[0]) ** 2 for hh in hs], "--", color=AZUL, alpha=0.5, lw=1.4,
                    label="pendiente O(h²)")
    if err_s[0] > 0:
        ax_c.loglog(ns, [max(err_s[0] * (hh / hs[0]) ** 4, piso) for hh in hs], "--",
                    color=ROSA, alpha=0.5, lw=1.4, label="pendiente O(h⁴)")
    ax_c.set_title("Convergencia del error")
    ax_c.set_xlabel("n (número de subintervalos)")
    ax_c.set_ylabel("|A − referencia|")
    ax_c.grid(True, which="major")
    ax_c.legend(fontsize=8)

    fig.suptitle(titulo)
    _guardar(plt, fig, titulo)
