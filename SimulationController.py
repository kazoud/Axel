from PySide6 import QtWidgets
from dataclasses import dataclass
import leakyIntegrateFire
import lowRank

@dataclass
class LIFInputs:
    vRest: float
    vThreshold: float
    vReset: float
    r: float
    tau:float
    duration:float
    current:str
    timeStep:float
    spikeRateAdaptation:bool
    potassiumVrest:float
    potassiumConductanceIncrement:float
    potassiumTau:float
    synapticConductance:bool
    rmgSyn:float
    synpaseVrest:float

@dataclass
class lowRankRnnsInputs:
    numberOfUnits: int
    g: float
    meanOfM: float
    StandardDeviationOfM: float
    meanOfN: float
    StandardDeviationOfN: float

@dataclass
class PlotElement:
    data: list[tuple[list[float], list[float]]] #data is of the form [(x1, y1), (x2, y2), etc]
    xLabel: str
    yLabel: str
    title: str

class SimulationController():

    def lifSequence(self,widget : QtWidgets.QWidget)-> list[PlotElement]:
        voltageTitle = "Leaky Integrate-and-Fire"
        voltageXlabel = "Time (ms)"
        voltageYlabel = "Voltage (mV)"

        currentTitle = "Input Electrode Current"
        currentXlabel = "Time (ms)"
        currentYLabel = "Current (nA)"

        plotElements = []
        #interspikeRateAnalysis = True
        inputs = self.__extractLIFInputs(widget)

        timeValues, currentValues = leakyIntegrateFire.parseCurrent(current=inputs.current, duration=inputs.duration, timeStep=inputs.timeStep)

        xVoltage, yVoltage = leakyIntegrateFire.leakyIntegrateAndFire(inputs.vRest,
                                                                    inputs.vThreshold,
                                                                    inputs.vReset,
                                                                    inputs.r,
                                                                    inputs.tau,
                                                                    inputs.duration,
                                                                    inputs.timeStep,
                                                                    currentValues,
                                                                    inputs.spikeRateAdaptation,
                                                                    inputs.potassiumVrest,
                                                                    inputs.potassiumConductanceIncrement,
                                                                    inputs.potassiumTau,
                                                                    inputs.synapticConductance,
                                                                    inputs.rmgSyn,
                                                                    inputs.synpaseVrest)

        plotElements.append(PlotElement([(xVoltage , yVoltage)], voltageXlabel, voltageYlabel, voltageTitle))
        plotElements.append(PlotElement([(timeValues, currentValues)], currentXlabel, currentYLabel, currentTitle))

        #it works but it's cumbersome for now
        # if (interspikeRateAnalysis):
        #         xInterspike, yInterspike = leakyIntegrateFire.interspikeIntervalRate(inputs.r, inputs.vRest, inputs.vThreshold, inputs.vReset, inputs.tau, linear = False)
        #         plotElements.append(PlotElement(xInterspike,yInterspike, "current (nA)", "Interspike Interval Rate (Hz)", ""))

        return plotElements

    def lowRankRnnsSequence(self, widget : QtWidgets.QWidget)->list[PlotElement]:
        plotElements = []

        inputs = self.__extractLowRankRnnsInputs(widget)
        neuralData, time, m = lowRank.simulate(N = inputs.numberOfUnits,g=inputs.g, meanOfM=inputs.meanOfM, standardDeviationOfM=inputs.StandardDeviationOfM, meanOfN=inputs.meanOfN, standardDeviationOfN=inputs.StandardDeviationOfN )
        neuralPlottingData = []
        for i in range(len(neuralData)):
            neuralPlottingData.append((time, neuralData[i]))

        pca = lowRank.pca(neuralData)
        pcaPlottingData = [(time, m), (time,pca)]

        plotElements.append(PlotElement(neuralPlottingData, "Activation", "Time", "Total neural activity over time"))

        return plotElements

    def __extractLIFInputs(self,widget : QtWidgets.QWidget)-> LIFInputs:
        vRest = widget.vRest.value()
        vThreshold = widget.vThreshold.value()
        vReset = widget.vReset.value()
        r = widget.r.value()
        tau = widget.tau.value()
        duration = widget.duration.value()
        current = widget.current.toPlainText()
        timeStep = widget.timeStep.value()
        spikeRateAdaptation = widget.spikeRateAdaptationCheckBox.isChecked()
        potassiumVrest = widget.potassiumVrest.value()
        potassiumConductanceIncrement = widget.potassiumConductance.value()
        potassiumTau = widget.potassiumTau.value()
        synapticConductance = widget.synapticConductanceCheckBox.isChecked()
        rmgSyn = widget.rmgSyn.value()
        synapseVrest = widget.synapseVrest.value()

        return LIFInputs(vRest,vThreshold, vReset, r, tau, duration, current, timeStep, spikeRateAdaptation, potassiumVrest, 
                      potassiumConductanceIncrement, potassiumTau, synapticConductance, rmgSyn, synapseVrest)

    def __extractLowRankRnnsInputs(self, widget : QtWidgets.QWidget) -> lowRankRnnsInputs:
        numberOfUnits = int(widget.UnitsInTheNetwork.value())
        g = widget.g.value()
        meanOfM = widget.MeanOfM.value()
        standardDeviationOfM = widget.StandardDeviationOfN.value()
        meanOfN = widget.MeanOfN.value()
        standardDeviationOfN = widget.StandardDeviationOfN.value()

        return lowRankRnnsInputs(numberOfUnits, g, meanOfM, standardDeviationOfM, meanOfN, standardDeviationOfN)

