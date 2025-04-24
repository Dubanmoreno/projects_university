from django.shortcuts import render
from itertools import combinations, product
from math import comb

def subconjuntos(conjunto):
    return [list(s) for i in range(len(conjunto)+1) for s in combinations(conjunto, i)]

def subconjuntos_propios(conjunto):
    return [s for s in subconjuntos(conjunto) if len(s) != len(conjunto)]

def numero_bell(n):
    bell = [0] * (n+1)
    bell[0] = 1
    for i in range(1, n+1):
        bell[i] = sum(comb(i-1, j) * bell[j] for j in range(i))
    return bell[n]

def particiones(conjunto):
    if not conjunto:
        return [[]]
    if len(conjunto) == 1:
        return [[[conjunto[0]]]]
    res = []
    primer = conjunto[0]
    for sub in particiones(conjunto[1:]):
        for i in range(len(sub)):
            copia = sub[:i] + [[primer] + sub[i]] + sub[i+1:]
            res.append(copia)
        res.append([[primer]] + sub)
    return res

def index(request):
    resultado = ""
    if request.method == 'POST':
        conjunto_a = request.POST.get('conjunto_a', '')
        conjunto_b = request.POST.get('conjunto_b', '')
        try:
            A = [x.strip() for x in conjunto_a.split(',') if x.strip()]
            B = [x.strip() for x in conjunto_b.split(',') if x.strip()]
            if len(set(A)) != len(A) or len(set(B)) != len(B):
                raise ValueError("Los conjuntos no deben tener elementos repetidos.")

            operacion = request.POST.get('operacion')
            if operacion == 'subconjuntos':
                subconjs = subconjuntos(A)
                propios = subconjuntos_propios(A)
                resultado = f"Subconjuntos: {len(subconjs)}<br>" + "<br>".join(map(str, subconjs))
                resultado += f"<br><br>Subconjuntos propios: {len(propios)}<br>" + "<br>".join(map(str, propios))
            elif operacion == 'potencia':
                potencia = subconjuntos(A)
                resultado = f"Conjunto potencia ({len(potencia)}):<br>" + "<br>".join(map(str, potencia))
            elif operacion == 'particiones':
                partes = particiones(A)
                bell = numero_bell(len(A))
                resultado = f"Número de particiones (Bell): {bell}<br><br>" + "<br>".join(map(str, partes))
            elif operacion == 'cartesiano':
                pares = product(A, B)
                resultado = f"Producto cartesiano ({len(A)*len(B)}):<br>" + "<br>".join(map(str, pares))
        except Exception as e:
            resultado = f"Error: {str(e)}"
    return render(request, 'conjuntos/index.html', {'resultado': resultado})
