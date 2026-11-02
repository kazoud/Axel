import numerical
import numpy as np
import scipy

def simulate(N: int, g: float, meanOfM: float, standardDeviationOfM: float, meanOfN: float, standardDeviationOfN: float):
    m = numerical.getRandomVector(N, meanOfM, standardDeviationOfM)
    n = numerical.getRandomVector(N, meanOfN, standardDeviationOfN)
    structured = numerical.getStructuredMatrix(m,n,N)
    chaotic = g * numerical.getRandomMatrix(N)
    connectivity = chaotic + structured
    phi = lambda x : np.tanh(x)

    equations = []
    for i in range(N):
        equation = lambda state, i=i: -state[i] + sum(
                                                        (connectivity[i][j])*phi(state[j])
                                                        for j in range(N)
                                                        )
        equations.append(equation)
    models = np.array(equations)

    steps = 100
    stepSize = 0.1
    time = [0]
    states = [[1] for i in range(N)]
    current = np.array([1]*N)
    for i in range(1,steps):
        current = numerical.rungeKutta(state = current, stepSize=stepSize, models =models)
        time.append(time[-1] + stepSize)
        for j in range(N):
            states[j].append(current[j])

    return states, time, m/np.linalg.norm(m)


