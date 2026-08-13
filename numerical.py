from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

def euler(x: float, stepSize: float, f: Callable[[float], float])-> float:
    return x + stepSize*f(x)
    
def rungeKuttaFloat(x: float, stepSize: float, f: Callable[[float], float])->float:
    k1 = stepSize*f(x)
    k2 = stepSize*f(x + 0.5*k1)
    k3 = stepSize*f(x + 0.5*k2)
    k4 = stepSize*f(x + k3)
    return x+ (k1+2*k2+2*k3+k4)/6

def rungeKutta(state:np.ndarray[float], stepSize:float, models: np.ndarray[Callable])->list[float]:

    def derivatives(state):
        return np.array([model(state) for model in models])

    k1 = stepSize*derivatives(state)
    k2 = stepSize*derivatives(state + 0.5*k1)
    k3 = stepSize*derivatives(state + 0.5*k2)
    k4 = stepSize*derivatives(state + k3)
    return state + (k1+2*k2+2*k3+k4)/6

def solve(x0: float, f: Callable[[float], float]) -> tuple[list[float],list[float]]:
    steps = 100
    stepSize = 1e-1
    t = 0
    values = ([t], [x0])
    for i in range(steps):
        t += stepSize
        values[0].append(t)
        values[1].append(rungeKuttaFloat(values[1][-1], stepSize,f))
    return values

if __name__ == "__main__":
    fig, ax = plt.subplots()

    differentialEquation = lambda x: 2.5 - 0.5*x
    for x0 in np.linspace(start= 0,stop= 10, num= 50):
        timeValues, xValues = solve(x0, differentialEquation)
        ax.plot(timeValues, xValues)