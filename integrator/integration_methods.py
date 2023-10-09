import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO




def method_parabol(func: str, a: float, b: float, pieces: int) -> float:
    step = (b - a) / pieces
    x = a + step
    ans = 0
    while x < b - step:
        ans += 4 * eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": x})
        ans += 2 * eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": x + step})
        x += step * 2
    ans = (step / 3) * (ans + eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": a}) + eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": b}))

    return ans


def method_trap(func: str, a: float, b: float, pieces: int) -> float:
    step = (b - a) / pieces
    x = a + step
    ans = 0
    while x < (b - step):
        ans += ((eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": x}) + eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": x + step})) / 2)
        x += step
    ans = step * (((eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": a}) + eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": b})) / 2) + ans)

    return ans


def printing_func(func: str, a: float, b: float, pieces: int) -> None:
    x = np.linspace(a, b, pieces)
    y = eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": x})

    plt.title(f"График функции " + func + ": ")
    plt.xlabel("Ось X")
    plt.ylabel("Ось Y")

    plt.grid(True)

    plt.plot(x, y)

    plt.show()



