import math
import numpy as np
import expressionParser
import numerical
from typing import Callable

def parseCurrent(current: str, duration: float, timeStep: float)->tuple[list[float], list[float]]:
    steps = math.floor(duration/timeStep)
    timeValues = np.linspace(0, duration, steps)
    currentValues = expressionParser.parseExpression(input = current, timeValues = timeValues)
    return (timeValues,currentValues)

def leakyIntegrateAndFire(vRest: float, vThreshold: float, vReset, rMembrane: float, tau: float, milliseconds: float, timeStep: float, currentValues:list[float], spikeRateAdaptation:bool, potassiumVrest:float, conductanceIncrement:float, potassiumTau:float)-> tuple[list[float], list[float]]:
    steps = math.floor(milliseconds/timeStep)
    if not spikeRateAdaptation:
        potassiumVrest = 0
    dvdt = lambda voltage, rmgSra, current : (vReset + rMembrane*current +rmgSra*potassiumVrest -(voltage*(1+rmgSra))) /tau
    voltages = [vRest]
    drmgSradt = lambda rmgSra : -rmgSra/tau
    rmgSraValues = [0]

    for i in range(steps):
        models = np.array([
            lambda state : dvdt(state[0],state[1], currentValues[i]),
            lambda state: drmgSradt(state[1])
        ])
        nextState = numerical.rungeKutta(np.array([voltages[-1], rmgSraValues[-1]]), timeStep, models)
        voltage = nextState[0]
        rmgSra = nextState[1]
        if (voltage >= vThreshold): #fire an action potential
            voltages.append(0)
            voltage = vReset
            if spikeRateAdaptation:
                rmgSra += conductanceIncrement

        rmgSraValues.append(rmgSra)
        voltages.append(voltage)

    voltageTimeValues = timeStep*np.arange(len(voltages)) #Technically, doing this distorts time slightly because we don't have t values for the action potential. 
                                                          #This is due to the limitations of the model. 
                                                          #In practice, we could measure the duration of an action potential and adapt the code accordingly
    return [voltageTimeValues, voltages]

def __computeInterspikeIntervalRate(current:float, r:float, vRest: float, vThreshold: float, vReset: float, tau: float, linear: bool)->float:
    if (linear):
        return (r*current + vRest - vThreshold)/(tau*(vThreshold-vReset))
    return 1/(tau*math.log((r*current+vRest-vReset)/(r*current+vRest-vThreshold)))

def interspikeIntervalRate(r:float, vRest:float, vThreshold: float, vReset: float, tau: float, linear: bool) ->tuple[list[float],list[float]]:
    currents = np.arange(3,10,0.5)
    interspikeRates = []
    for current in currents:
        interspikeRates.append(__computeInterspikeIntervalRate(current,r, vRest,vThreshold,vReset,tau,linear))
    return [currents, interspikeRates]

if __name__ == "__main__": 
    print("lif")
