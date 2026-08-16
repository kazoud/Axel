import math
import numpy as np
import expressionParser
import numerical

def parseCurrent(current: str, duration: float, timeStep: float)->tuple[list[float], list[float]]:
    steps = math.floor(duration/timeStep)
    timeValues = np.linspace(0, duration, steps)
    currentValues = expressionParser.parseExpression(input = current, timeValues = timeValues)
    return (timeValues,currentValues)

def leakyIntegrateAndFire(vRest: float, vThreshold: float, vReset, rMembrane: float, tau: float, milliseconds: float, timeStep: float, 
                          currentValues:list[float], spikeRateAdaptation:bool, potassiumVrest:float, conductanceIncrement:float, 
                          potassiumTau:float, synapticConductance: bool, rmgSyn:float, synapseVrest:float)-> tuple[list[float], list[float]]:
    steps = math.floor(milliseconds/timeStep)
    if not spikeRateAdaptation:
        potassiumVrest = 0
    if not synapticConductance:
        rmgSyn = 0

    dvdt = lambda voltage, rmgSra, Ps, current : (vReset + rMembrane*current +rmgSra*potassiumVrest + rmgSyn*Ps*synapseVrest -(voltage*(1+rmgSra+rmgSyn*Ps))) /tau
    drmgSradt = lambda rmgSra : -rmgSra/potassiumTau
    dPsdt = lambda Ps, z: math.exp(1)*0.5*z*(1-Ps) - Ps
    dzdt = lambda z: -z/10

    voltages = [vRest]
    rmgSraValues = [0]
    PsValues = [0]
    zValues = [0]

    for i in range(steps):
        models = np.array([
            lambda state : dvdt(state[0],state[1], state[2], currentValues[i]),
            lambda state: drmgSradt(state[1]),
            lambda state: dPsdt(state[2], state[3]),
            lambda state: dzdt(state[3])
        ])
        nextState = numerical.rungeKutta(np.array([voltages[-1], rmgSraValues[-1], PsValues[-1], zValues[-1]]), timeStep, models)
        voltage = nextState[0]
        rmgSra = nextState[1]
        Ps = nextState[2]
        z = nextState[3]

        if (voltage >= vThreshold): #fire an action potential
            voltages.append(0)
            voltage = vReset
            if spikeRateAdaptation:
                rmgSra += conductanceIncrement
        if i == 500 or i == 1500 or i == 1900 or i == 3000 or i == 3200 or i == 4000 or i == 4100:
            z = 1

        voltages.append(voltage)
        rmgSraValues.append(rmgSra)
        PsValues.append(Ps)
        zValues.append(z)

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
