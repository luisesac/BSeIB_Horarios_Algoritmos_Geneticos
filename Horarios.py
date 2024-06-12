def primer_hora(dia:list)->int:
    i = 0
    for hora in dia:
        if hora != 0:
            return i
        i+=1
    return -1   # No hay horas asignadas

def hora_salida(dia:list)->int:
    i = len(dia) - 1
    for j in reversed(dia):
        if j != 0:
            return i+4
        i -= 1
    return -1   # No hay horas asignadas

def n_choques(dia:list)->list:
    inicio = primer_hora(dia)
    fin = hora_salida(dia)
    choques = []
    for i in range(inicio, fin + 1):
        if dia[i] != 0:
            for c in range(i+1, i+5):
                if dia[c] != 0 :
                    choques += [a for a in range(c, i+5)]
    return choques

def n_choques_(dia:list)->list:
    inicio = primer_hora(dia)
    fin = hora_salida(dia)
    choques = []
    for horas in dia:
        if horas == -1:
            choques.append(1)
    return choques

def n_horas_libres(dia:list):
    horario = generar_dia(dia)
    inicio = primer_hora(dia)
    fin = hora_salida(dia)
    horas_libres = []
    for i in range(inicio, fin+1):
        if horario[i] == 0:
            horas_libres.append(i)
    return horas_libres

def anomalias(horario:list, n_materias:int, alpha:float, beta:float, gamma:float)->float:
    anomalia = 0
    for dia in horario:
        d = generar_dia(dia)
        anomalia += (len(n_choques_(d))*alpha + len(n_horas_libres(dia))*beta)
    anomalia += uniformidad(horario, n_materias)*gamma
    return anomalia

def uniformidad(horario:list, n_materias:int)->float:
    horas = []
    esperado = n_materias / 5
    for dia in horario:
        materias_en_el_dia = list(set(dia))
        materias_en_el_dia.remove(0)
        horas.append(len(materias_en_el_dia))
    mse = 0
    for i in range(5):
        mse += horas[i] - esperado
    return abs(mse/5)

def generar_dia(dia:list)->list:
    inicio = primer_hora(dia)
    fin = hora_salida(dia)
    horario = [0 for _ in range(len(dia))]
    for i in range(inicio, fin +1):
        if dia[i] != 0:
            horario[i:i+5] = [dia[i]]*5
    for i in n_choques(dia):
        horario[i] = -1
    return horario
    #a = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0]
    #a = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0]

    #b = [0, 1, 0, 0, 2, 0, 0, 0, 0]
    #b = [0, 1, 1, 1, -1, -1, 2, 2, 2,]

def tab2d_tab1d(horario:list)->list:
    horario1d = []
    for dia in horario:
        horario1d += dia
    return horario1d

import numpy as np

def tab1d_tab2d(horario:list)->list:
    horario2d = []
    for i in range(0, 80, 16):
        horario2d.append(horario[i:i+16])
    return horario2d

def total_materias(horario:list)->list:
    materias = []
    for dia in horario:
        for materia in dia:
            materias.append(materia)
    materias = list(set(materias))
    materias.remove(0)
    return materias
"""
def main():
    a = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0]
    a = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0]
    print(generar_dia(a))
    print(len(ver_choques(a)))
    print(ver_horas_libres(a))

if __name__ == "__main":
    main()"""