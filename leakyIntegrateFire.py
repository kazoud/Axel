import math
import numpy as np

def leakyIntegrateAndFire(vRest: float, vThreshold: float, vReset, r: float, tau: float, milliseconds: float, timeStep: float, current:float)-> tuple[list[float], list[float]]:
    steps = math.floor(milliseconds/timeStep)
    intSteps = math.floor
    currents = [current] * steps
    # currents = [0] * math.floor(steps*0.2)
    # currents.extend(4*math.pow(math.sin(0.4*i*2*math.pi/1000),2) for i in range(math.floor(steps*0.6)))
    # currents.extend([0]*math.floor(steps*0.2))
    #keep those for when you can customize the current input
    model = lambda voltage, current : vReset + r*current + (voltage - (vReset + r*current))*math.exp(-timeStep/tau)
    voltages = [vRest]
    for i in range(steps):
        value = model(voltages[-1],currents[i])
        if (value > vThreshold): #fire an action potential
            voltages.append(0)
            value = vReset
        voltages.append(value)

    voltageTimeValues = timeStep*np.arange(len(voltages))
    currentTimeValues = timeStep*np.arange(len(currents))
    return [voltageTimeValues, voltages, currentTimeValues,currents]

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