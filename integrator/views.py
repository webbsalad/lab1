from django.shortcuts import render
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
import numpy as np
from numpy import sin, cos, tan


def sol_func(fun: str, x: int) -> float:
    return eval(fun, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": x})

def method_right(func: str, a: float, b: float, pieces: int) -> float:
    step = (b - a) / pieces
    x = a
    ans = 0
    while x < (b - step):
        ans += sol_func(func, x)
        x += step

    return ans * step


def method_left(func: str, a: float, b: float, pieces: int) -> float:
    step = (b - a) / pieces
    x = a
    ans = 0
    while x < b:
        ans += sol_func(func, x)
        x += step

    return ans * step


def method_parabol(func: str, a: float, b: float, pieces: int) -> float:
    step = (b - a) / pieces
    x = a + step
    ans = 0
    while x < b - step:
        ans += 4 * sol_func(func, x)
        ans += 2 * sol_func(func, x+step)
        x += step * 2
    ans = (step / 3) * (
                ans + eval(func, {"__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": a}) + eval(func, {
            "__builtins__": None}, {"cos": cos, "sin": sin, "tan": tan, "x": b}))

    return ans


def method_trap(func: str, a: float, b: float, pieces: int) -> float:
    step = (b - a) / pieces
    x = a + step
    ans = 0
    while x < (b - step):
        ans += ((sol_func(func, x) + sol_func(func, x+step)) / 2)
        x += step
    ans = step * (((sol_func(func, a) + sol_func(func, b)) / 2) + ans)

    return ans


def printing_func(func: str, a: float, b: float, pieces: int) -> None:
    x = np.linspace(a, b, pieces)
    y = sol_func(func, x)

    plt.title(f"График функции " + func + ": ")
    plt.xlabel("Ось X")
    plt.ylabel("Ось Y")

    plt.grid(True)

    plt.plot(x, y)

    plt.plot(x, [0]*len(x), color='m', linestyle='--', linewidth=1.5) 
    plt.plot((a, a), (sol_func(func, x[0]), 0), color='m', linestyle='--', linewidth=1.5)
    plt.plot((b, b), (sol_func(func, x[-1]), 0), color='m', linestyle='--', linewidth=1.5)
    plt.fill_between(x, y, where=(x >= a) & (x <= b), color='lavender', hatch='/', alpha=0.5) 
    plt.text(x[-1], y[-1], func, fontsize=12, verticalalignment='bottom', horizontalalignment='right')
    plt.xlim(x.min() - 0.2, x.max() + 0.2)
    plt.ylim(min(y) - 0.2, max(y) + 0.2)

    buffer = BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer


# ------------------------------------------------------------------------------------------------------------#


def exchange(reqests):
    calc_method = {"Правых частей": 1, "Левых частей": 2, "Параболы": 3, "Трапеции": 4}
    calc_alg = {"Постоянный шаг": 1, "Переменный шаг": 2}
    # начальное заполнение
    if reqests.method == "GET":
        context = {
            'calc_method': calc_method,
            'calc_alg': calc_alg
        }
        return render(request=reqests, template_name='integrator/index.html', context=context)

    # при нажатии 
    if reqests.method == "POST":
        # обработка не всех введенных значений
        if not reqests.POST.get('function') or not reqests.POST.get('first-limit') or not reqests.POST.get(
                'second-limit') or not reqests.POST.get('count-pieces'):
            function = str(reqests.POST.get('function')) if reqests.POST.get('function') else None
            fir_limit = float(reqests.POST.get('first-limit')) if reqests.POST.get('first-limit') else None
            sec_limit = float(reqests.POST.get('second-limit')) if reqests.POST.get('second-limit') else None
            pieces = int(reqests.POST.get('count-pieces')) if reqests.POST.get('count-pieces') else None
            met = reqests.POST.get('calculation-method') if reqests.POST.get('calculation-method') else None
            alg = reqests.POST.get('calculation-algoritm') if reqests.POST.get('calculation-algoritm') else None

            context = {
                'func': function,
                'low_lim': str(fir_limit),
                'up_lim': str(sec_limit),
                'pieces': pieces,
                'alg': alg,
                'met': met,

                'calc_method': calc_method,
                'calc_alg': calc_alg
            }
            return render(request=reqests, template_name='integrator/index.html', context=context)
        

        function = str(reqests.POST.get('function'))
        fir_limit = float(reqests.POST.get('first-limit'))
        sec_limit = float(reqests.POST.get('second-limit'))
        pieces = int(reqests.POST.get('count-pieces'))
        met = reqests.POST.get('calculation-method')
        alg = reqests.POST.get('calculation-algoritm')

        match (calc_method[met]):
            case 1:
                ans = method_right(function, fir_limit, sec_limit, pieces)
            case 2:
                ans = method_left(function, fir_limit, sec_limit, pieces)
            case 3:
                ans = method_parabol(function, fir_limit, sec_limit, pieces)
            case 4:
                ans = method_trap(function, fir_limit, sec_limit, pieces)

        # Построение графика
        graphic = printing_func(function, fir_limit, sec_limit, pieces)
        plt.clf()

        context = {
            'ans': ans,
            'func': function,
            'low_lim': str(fir_limit),
            'up_lim': str(sec_limit),
            'pieces': pieces,
            'alg': alg,
            'met': met,

            'calc_method': calc_method,
            'calc_alg': calc_alg
        }


        if "graph" in reqests.POST:
            return HttpResponse(graphic.getvalue(), content_type='image/png')
        if "sub" in reqests.POST:
            return render(request=reqests, template_name='integrator/index.html', context=context)
