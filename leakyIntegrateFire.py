import math
import numpy as np
import expressionParser

def parseCurrent(current: str, duration: float, timeStep: float)->tuple[list[float], list[float]]:
    steps = math.floor(duration/timeStep)
    timeValues = np.linspace(0, duration, steps)
    currentValues = expressionParser.parseExpression(input = current, timeValues = timeValues)
    return (timeValues,currentValues)

def leakyIntegrateAndFire(vRest: float, vThreshold: float, vReset, r: float, tau: float, milliseconds: float, timeStep: float, currentValues:list[float])-> tuple[list[float], list[float]]:
    steps = math.floor(milliseconds/timeStep)
    model = lambda voltage, current : vReset + r*current + (voltage - (vReset + r*current))*math.exp(-timeStep/tau)
    voltages = [vRest]
    for i in range(steps):
        value = model(voltages[-1],currentValues[i])
        if (value > vThreshold): #fire an action potential
            voltages.append(0)
            value = vReset
        voltages.append(value)

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