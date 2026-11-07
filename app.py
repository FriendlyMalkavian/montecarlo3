from random import random
import matplotlib.pyplot as plt
import math
import numpy as np

#Основная функция программы
def MonteCarloBinomial(numberOfExperiments, N_trials, p):
    experiments = []
    
    #Моделирование значений биномиальной СВ
    for _ in range(numberOfExperiments):
        successes = 0
        for _ in range(N_trials):
            if random() < p:
                successes += 1
        experiments.append(successes)
    
    #Значения СВ в промежутке [0, N_trials]
    segments = list(range(N_trials + 1))
    results = [0] * (N_trials + 1)
    
    #Подсчитываем число попаданий в каждый сегмент
    for value in experiments:
        results[value] += 1
    
    #Относительная частота в каждом сегменте = число_попаданий_в_сегмент / numOfExperiments
    y_values = [count / numberOfExperiments for count in results] #Значения для отрисовки на итоговом графике
    
    return segments, y_values, experiments



#Теоретические значения биномиального распределения
def theoryBinomial(m, N , p):
    """Формула биномиального распределения: P(X=m) = C(N,m) * p^N * (1-p)^(N-m)"""
    C = math.comb(N, m)
    return C * (p**m) * ((1-p)**(N-m))

def pCheck():
    while True:
        p = input("Введите вероятность успеха: ")
        try:
            if ',' in p:
                p = float(p.replace(',','.'))
                if 0 < p <= 1:
                    return p
                else:
                    print("Проверьте значение аргумента p")
                    continue
            else:
                p = float(p)
                if 0 < p <= 1:
                    return p
                else:
                    print("Проверьте значение аргумента p")
                    continue
        except ValueError:
            print("Проверьте значение аргумента p")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
        
def nCheck():
    while True:
        n = input("Введите число испытаний Бернулли в каждом опыте: ")
        try:
            n = int(n)
            if n > 0:
                return n
            else:
                print("n должно быть натуральным")
                continue
        except ValueError:
            print("Проверьте значение аргумента n")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

def chCheck():
    while True:
        ch = input("Введите число опытов: ")
        try:
            ch = int(ch)
            if ch > 0:
                if ch > 1000000:
                    ans = input("Большое число опытов займёт много времени. Введите y/Y чтобы продолжить либо любую клавишу чтобы повторить ввод числа опытов")
                    if ans == "y" or ans == "Y":
                        print("Думаю")
                        return ch
                    else:
                        continue
                return ch
            else:
                print("Число опытов должно быть натуральным")
                continue
        except ValueError:
            print("Проверьте значение числа опытов")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
    
def usersInput():
    n = nCheck()#Проверка содержимого на натуральное значение
    p = pCheck()#проверка содержимого на запятую, но не на значение
    ch = chCheck()
    return n, p , ch

#Главная функция
def main():
    # Параметры эксперимента
    
    #n=10
    #p=0.32#Вероятность наступления успеха
    #ch = 40000
    
    n, p , ch = usersInput()
    
    if n > 0 and ch > 0:
        while True:
            segments, y_values, experiments = MonteCarloBinomial(ch, n, p)

            #Список полученных теоретических значений
            y_theory = [theoryBinomial(m, n, p) for m in segments]

            #Визуализация
            plt.figure(figsize=(10, 6))
            plt.bar(segments, y_values, width=0.6, color='skyblue',
                    edgecolor='black', alpha=0.7, label = 'Биномиальное распределение')
            plt.plot(segments, y_theory, 'ro-', linewidth=2, markersize=6,
                     label=f'Теоретическое распределение ({n}, {p})')
            plt.xlabel('Число успехов m')
            plt.ylabel('Относительная частота P (X = m)')
            plt.title('Биномиальное распределение: метод Монте-Карло и теория')
            plt.xticks(segments)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            plt.legend()
            plt.tight_layout()
            plt.show()
            break
    
    else:
        print("Некорректный ввод. Аргументы n, p и ch должны быть положительными")

#Вызов главной функции при запуске
main()   
    
    
            

 