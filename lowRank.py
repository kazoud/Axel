import numerical
import numpy as np

def simulate(N: int, g: float, meanOfM: float, standardDeviationOfM: float, meanOfN: float, standardDeviationOfN: float):
    m = numerical.getRandomVector(N, meanOfM, standardDeviationOfM)
    n = numerical.getRandomVector(N, meanOfN, standardDeviationOfN)
    return simulateWithFixedConnectivity(N, m, n, g)

def simulateWithFixedConnectivity(N: int, m:np.array, n:np.array, g:float, initialValue: float = 1.0):
    structured = numerical.getStructuredMatrix(m,n,N)
    chaotic = g * numerical.getRandomMatrix(N)
    connectivity = chaotic + structured

    def rnn(state):
        return -state + connectivity @ np.tanh(state)
    
    steps = 100
    stepSize = 0.1
    time = [0]
    states = np.empty((N, steps))
    states[:,0] = initialValue
    current = np.full(N, initialValue)
    for i in range(1,steps):
        current = numerical.rungeKuttaVectorized(state = current, stepSize=stepSize, f =rnn)
        time.append(time[-1] + stepSize)
        states[:,i] = current

    return states.tolist(), time

def getGValuesForActivityAlongM(start: float, end:float, points: int):
    return np.linspace(start=start, stop=end, num = points)

def activityAlongM(N:int, meanOfM:float, standardDeviationOfM:float, meanOfN:float, standardDeviationOfN:float):
    gValues = getGValuesForActivityAlongM(start = 0, end = 4, points = 20).tolist()
    m = numerical.getRandomVector(N, meanOfM, standardDeviationOfM)
    n = numerical.getRandomVector(N, meanOfN, standardDeviationOfN)

    initialValue = 1.0
    plottingData = []
    print("Computing activity along m for positive initial conditions:")
    print("Computing neural activity for different values of g:")
    __simulateTrials(gValues, N, m, n, initialValue, plottingData)

    print("Computing activity along m for negative initial conditions:")
    print("Computing neural activity for different values of g:")
    __simulateTrials(gValues, N, m, n, -initialValue, plottingData)
        
    return plottingData, gValues * 2

def __simulateTrials(gValues: list[float], N, m, n, initialValue, plottingData):
    trials = 15
    for g in gValues:
            print("g = " + str(g))
            meanFiringRate = None
            for i in range(trials):
                neuralData, time = simulateWithFixedConnectivity(N, m, n, g, initialValue=initialValue)
                steadyState = np.array(neuralData)[:, -10:]
                firingRate = np.mean(steadyState, axis = 1)
                if meanFiringRate is None:
                    meanFiringRate = firingRate
                else:
                    meanFiringRate += firingRate
            meanFiringRate /= trials
            plottingData.append((1/N) * np.inner(n, meanFiringRate).item())