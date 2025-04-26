import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
from matplotlib.animation import FuncAnimation

def animar_medias_tiempo(x, n_realizaciones, a=2, tau=100):
    """
    Visualiza cómo cambian las medias de una señal procesada por:
    1. Un sistema FIR (con coeficientes [1, -1/a, 1/(2*a)])
    2. Un sistema no lineal (x²)

    Se usan múltiples realizaciones y se comparan las medias en dos instantes 
    de tiempo t1 y t2. Se anima la evolución de las medias a lo largo del tiempo.

    Parámetros:
    - x: matriz (n_realizaciones, 1000) con las realizaciones de la señal.
    - n_realizaciones: número de realizaciones.
    - a: La mediana de los dígitos del código de todos los integrantes del grupo.
    - delta: Diferencia entre t1 y t2.
    """

    # -------------------------------
    # Procesamiento por los sistemas
    # -------------------------------

    # Definir el filtro FIR
    b = [1, -1/a, 1/(2*a)]

    # Aplicar el filtro FIR a cada realización
    y_fir = np.array([lfilter(b, [1], x[i]) for i in range(n_realizaciones)])

    # Aplicar el sistema no lineal (x²) a cada realización
    y_nl = x ** 2

    # Vector de tiempo
    tiempo = np.arange(1000)

    # -------------------------------
    # Crear figura para la animación
    # -------------------------------
    fig, axs = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    fig.suptitle("Realizaciones y medias en t1 y t2")

    ax1, ax2 = axs # Ejes para FIR (arriba) y no lineal (abajo)

    # Dibujar señales (solo las primeras 10 realizaciones)
    fir_lines = [ax1.plot(tiempo, y_fir[i], alpha=0.4)[0] for i in range(min(n_realizaciones, 10))]
    nl_lines = [ax2.plot(tiempo, y_nl[i], alpha=0.4)[0] for i in range(min(n_realizaciones, 10))]

    # Líneas verticales que marcan t1 y t2
    vline1_fir = ax1.axvline(0, color='g', linestyle='--', label="t1")
    vline2_fir = ax1.axvline(0, color='m', linestyle='--', label="t2")
    vline1_nl = ax2.axvline(0, color='g', linestyle='--')
    vline2_nl = ax2.axvline(0, color='m', linestyle='--')

    ax1.legend()
    ax1.set_title("Sistema FIR")
    ax2.set_title("Sistema no lineal (x²)")
    ax1.grid(True)
    ax2.grid(True)

    # Textos para mostrar las medias
    txt1 = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)
    txt2 = ax2.text(0.02, 0.95, '', transform=ax2.transAxes)

    # -------------------------------
    # Función de animación
    # -------------------------------
    def update(frame):
        # t1 y t2 se van desplazando en el tiempo
        t1 = frame
        t2 = frame + tau
        if t2 >= 1000:
            return []

        # Calcular medias en t1 y t2 para cada sistema
        media_fir_t1 = np.mean(y_fir[:, t1])
        media_fir_t2 = np.mean(y_fir[:, t2])
        media_nl_t1 = np.mean(y_nl[:, t1])
        media_nl_t2 = np.mean(y_nl[:, t2])

        # Actualizar líneas verticales (usar listas para evitar el error)
        vline1_fir.set_xdata([t1, t1])
        vline2_fir.set_xdata([t2, t2])
        vline1_nl.set_xdata([t1, t1])
        vline2_nl.set_xdata([t2, t2])

        # Actualizar textos de media
        txt1.set_text(f"Media FIR\nμ(t1={t1})={media_fir_t1:.3f}, μ(t2={t2})={media_fir_t2:.3f}, diferencia={np.abs(media_fir_t2 - media_fir_t1):.3f}")
        txt2.set_text(f"Media x²\nμ(t1={t1})={media_nl_t1:.3f}, μ(t2={t2})={media_nl_t2:.3f}, diferencia={np.abs(media_nl_t2 - media_nl_t1):.3f}")

        return fir_lines + nl_lines + [vline1_fir, vline2_fir, vline1_nl, vline2_nl, txt1, txt2]


    ani = FuncAnimation(fig, update, frames=range(0, 1000 - tau, 10), interval=200, blit=True)
    plt.tight_layout()
    plt.show()


# -------------------------------
# Canal con ruido térmico
# -------------------------------

n_realizaciones = 3000
x_ruido = np.random.normal(0, 4, (n_realizaciones, 1000))

animar_medias_tiempo(x_ruido, n_realizaciones, a=2, tau=100)

# -------------------------------
# Demodulación cuadrática de una señal AM
# -------------------------------

t = np.arange(1000)
mensaje = 0.5 * np.sin(2 * np.pi * 0.01 * t)  # mensaje
portadora = np.cos(2 * np.pi * 0.1 * t)       # portadora
x_am = np.array([(1 + mensaje) * portadora + np.random.normal(0, 0.5, 1000) for _ in range(n_realizaciones)])

animar_medias_tiempo(x_am, n_realizaciones, a=2, tau=100)

# -------------------------------
# Canal no estacionario
# -------------------------------

x_variante = np.array([np.random.normal(0, 0.5 + 0.01 * t, 1000) for t in range(n_realizaciones)])

animar_medias_tiempo(x_variante, n_realizaciones, a=2, tau=100)




