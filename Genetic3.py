import random
import Horarios
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#   Genera dos listas de tuplas ([0 - 4], [0 - 11]):
#       Una aleatoria, del tamaño del número de materias.
#       Otra con una selección aleatoria del las horas restrictas de cada materia restricta
#   Cada tupla es el índice (dia, hora) en el horario
def generar_poblacion(size:int, materias:int, materias_restrictas:list)->list:
    horarios = []
    for _ in range(size):
        horario = []
        horario_restricto = []
        for _ in range(materias):
            horario.append((random.randint(0, 4), random.randint(0, 11)))
        for i in range(len(materias_restrictas)):
            horario_restricto.append(random.choice(materias_restrictas[i]))
        horarios.append((horario, horario_restricto))
    return horarios

#   Convierte el horario representado por las listas de tuplas ([0 - 4], [0 - 11]) a una lista de listas (horario[dia][hora])
def generar_horario_tab(materias:list, materias_restrictas:list)->list:
    new_horario = [[0]*16 for _ in range(5)]
    materias_irrestrictas = len(materias)
    for i in range(len(materias)):
        dia = materias[i][0]
        hora = materias[i][1]
        new_horario[dia][hora] = i+1
    for i in range(len(materias_restrictas)):
        dia = materias_restrictas[i][0]
        hora = materias_restrictas[i][1]
        new_horario[dia][hora] = i+materias_irrestrictas+1
    return new_horario

def fitness(materias:list, n_materias:int, materias_restrictas:list, alpha:float, beta:float, gamma:float, delta:float)->float:
    anomalia = 0
    horario = generar_horario_tab(materias, materias_restrictas)
    for dia in horario:
        d = Horarios.generar_dia(dia)
        anomalia += (len(Horarios.n_choques_(d))*alpha + len(Horarios.n_horas_libres(dia))*beta)
    anomalia += Horarios.uniformidad(horario, n_materias)*gamma
    anomalia += ((n_materias + len(materias_restrictas))-len(Horarios.total_materias((horario))))*delta
    return anomalia

def reporte_individuo(materias:list, materias_restrictas:list, n_materias):
    horario = generar_horario_tab(materias, materias_restrictas)
    choques = 0
    horas_libres = 0
    for dia in horario:
        d = Horarios.generar_dia(dia)
        choques += len(Horarios.n_choques_(d))
        horas_libres += len(Horarios.n_horas_libres(dia))
    uniformidad = Horarios.uniformidad(horario, n_materias)
    materias_faltantes = ((n_materias + len(materias_restrictas))-len(Horarios.total_materias((horario))))
    return choques, horas_libres, uniformidad, materias_faltantes

#   Selección por ruleta
def seleccionar_padres(poblacion:list, puntuaciones:list):
    padres = []
    puntuaciones_total = sum(puntuaciones)
    for _ in range(2):
        puntuacion_acumulada = 0
        rand = random.uniform(0, puntuaciones_total)
        for i, fitness in enumerate(puntuaciones):
            puntuacion_acumulada += fitness
            if puntuacion_acumulada >= rand:
                padres.append(poblacion[i])
                break
    return padres

#   Combinación intercalada de índices
def crossover(padres:list, crossover_rate:float, materias:int):
    hijo = []
    hijo_2 = []
    for i in range(materias):
        if i%2 == 0:
            hijo.append(padres[0][0][i])
        else:
            hijo.append(padres[1][0][i])
    for i in range(len(padres[1])):
        if i%2 == 0:
            hijo_2.append(padres[0][1][i])
        else:
            hijo_2.append(padres[1][1][i])
    return (hijo, hijo_2)

#   Índice medio
def crossover_(padres:list, crossover_rate:float, materias:int):
    hijo = []
    for i in range(materias):
        hijo.append((int((padres[0][0][i][0] + padres[1][0][i][0]) / 2), int((padres[0][0][i][1] + padres[1][0][i][1]) / 2)))
    return (hijo, random.choice([padres[0][1], padres[1][1]]))

#   Suma modular de índices
def crossover__(padres:list, crossover_rate:float, materias:int):
    hijo = []
    for i in range(materias):
        hijo.append(((padres[0][0][i][0] + padres[1][0][i][0] + 2) % 5, (padres[0][0][i][1] + padres[1][0][i][1] + 2) % 12))
    return (hijo, random.choice([padres[0][1], padres[1][1]]))

def mutate(child, mutation_rate:float):
    materia = random.randint(0, len(child)-1)
    new_day = child[0][materia][0]
    new_hour = child[0][materia][1]
    if random.random() <= mutation_rate:
        new_day = (child[0][materia][0] + random.choice([-1, 1]))%5
        new_hour = (child[0][materia][1] + random.choice([-1, 1]))%12
    child[0][materia] = (new_day, new_hour)
    return child

def evaluar_poblacion(poblacion:list, alpha:float, beta:float, gamma:float, delta:float, n_materias:int)->list:
    puntuacion = []
    for horarios in poblacion:
        score = fitness(horarios[0], n_materias, horarios[1], alpha, beta, gamma, delta)
        puntuacion.append(score)
    return puntuacion

def a(x, n_materias, alpha, beta, gamma, delta):
    libres = x[0].copy()
    restrictas = x[1].copy()
    return fitness(libres, n_materias, restrictas, alpha, beta, gamma, delta)

def evolve(poblacion:list, generaciones:int, crossover_rate:float, mutation_rate:float, alpha:float, beta:float, gamma:float, delta:float, materias:int):
    best_fit = []
    worst_fit = []
    avg_fit = []
    #best = min(poblacion, key=lambda x:fitness(generar_horario_tab_(x[0], x[1]), materias, x[1], alpha, beta, gamma))
    best = min(poblacion, key=lambda x:fitness(x[0], materias, x[1], alpha, beta, gamma, delta))
    for _ in range(generaciones):
        fits = evaluar_poblacion(poblacion, alpha, beta, gamma, delta, materias)
        padres = seleccionar_padres(poblacion, fits)
        child = crossover__(padres, crossover_rate, materias)
        child = mutate(child, mutation_rate)
        poblacion.append(child)
        poblacion.pop(0)
        best_fit.append(min(fits))
        worst_fit.append(max(fits))
        avg_fit.append(sum(fits)/len(fits))
        best = min(poblacion, key=lambda x:fitness(x[0], materias, x[1], alpha, beta, gamma, delta))
    return best, best_fit

def plot_horario(horario:list):
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    top_axis = ['Hora inicio', 'Hora fin', 'Lunes', 'Martes', 'Míercoles', 'Jueves', 'Viernes']
    horas_inicio = [
        '07:00', '07:30', '08:00', '08:30', 
        '09:00', '09:30', '10:00', '10:30', 
        '11:00', '11:30' ,'12:00', '12:30',
        '13:00','13:30', '14:00', '14:30']
    horas_fin = [
        '07:30', '08:00', '08:30', '09:00', 
        '09:30', '10:00', '10:30', '11:00', 
        '11:30' ,'12:00', '12:30','13:00',
        '13:30', '14:00', '14:30', '15:00']
    
    data = [horas_inicio] + [horas_fin] + horario
    df = pd.DataFrame(np.array(data).T)

    ax.table(cellText=df.values, colLabels=top_axis, loc='center')

    fig.tight_layout()

    plt.show()

def __main__():
    # Peso de choques
    alpha = 10
    # Peso de las horas libres
    beta = 2
    # Peso de la uniformidad del horario
    gamma = 5
    # Peso del número de materias faltantes en el horario
    delta = 10
    generaciones = 1000
    crossover_rate = 0.5
    mutation_rate = 0
    materias = 5
    tam_pob = 500
    materias_restrictas =  [
        [(0, 0)], # Primer materia restricta
        [(i, 5) for i in range(5)],  # "Sólo puedo dar todos los días después del módulo 5"
        [(i, 10) for i in range(2, 4)],  # Sólo puedo dar después del módulo 11 entre miércoles y viernes
        [(4, 8)],
        [(i, 4) for i in range(3)]  #   Sólo puedo dar de lunes a miércoles en el módulo 4
    ]

    #pob = generar_poblacion_2(tam_pob, materias, [])
    pob = generar_poblacion(tam_pob, materias, materias_restrictas)
    best, bests_scores = evolve(pob, generaciones, crossover_rate, mutation_rate, alpha, beta, gamma, delta, materias)
    print(best)
    h2 = generar_horario_tab(best[0], best[1])
    h2 = [Horarios.generar_dia(i) for i in h2]
    print("="*48)
    for dia in h2:
        print(dia)
    print("="*48)
    print("Métricas del horario")
    choques, horas_libres, mae, materias_faltantes = reporte_individuo(best[0], best[1], materias)
    print("Choques", choques)
    print("Horas libres", horas_libres)
    print("Mean Absolute Error", mae)
    print("Materias faltantes", materias_faltantes)
    print("="*48)
    print(bests_scores[-1])
    plt.plot(bests_scores)
    plt.title("Fitness por generación")
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.show()
    plot_horario(h2)

if __name__ == "__main__":
    __main__()