from PySide6 import QtWidgets
from dataclasses import dataclass
import leakyIntegrateFire

@dataclass
class Inputs:
    vRest: float
    vThreshold: float
    vReset: float
    r: float
    tau:float
    duration:float
    current:float
    timeStep:float

@dataclass
class PlotElement:
    xData: list[float]
    yData: list[float]
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
        interspikeRateAnalysis = True
        inputs = self.__extractInputs(widget)

        xVoltage, yVoltage, xCurrent, yCurrent = leakyIntegrateFire.leakyIntegrateAndFire(inputs.vRest,
                                                                                          inputs.vThreshold,
                                                                                          inputs.vReset,
                                                                                          inputs.r,
                                                                                          inputs.tau,
                                                                                          inputs.duration,
                                                                                          inputs.timeStep,
                                                                                          inputs.current)

        plotElements.append(PlotElement(xVoltage, yVoltage, voltageXlabel, voltageYlabel, voltageTitle))
        plotElements.append(PlotElement(xCurrent, yCurrent, currentXlabel, currentYLabel, currentTitle))

        if (interspikeRateAnalysis):
                xInterspike, yInterspike = leakyIntegrateFire.interspikeIntervalRate(inputs.r, inputs.vRest, inputs.vThreshold, inputs.vReset, inputs.tau, linear = False)
                plotElements.append(PlotElement(xInterspike,yInterspike, "current (nA)", "Interspike Interval Rate (Hz)", ""))

        return plotElements

    def __extractInputs(self,widget : QtWidgets.QWidget)-> Inputs:
        vRest = widget.vRest.value()
        vThreshold = widget.vThreshold.value()
        vReset = widget.vReset.value()
        r = widget.r.value()
        tau = widget.tau.value()
        duration = widget.duration.value()
        current = widget.current.value()
        timeStep = widget.timeStep.value()

        return Inputs(vRest,vThreshold, vReset, r, tau, duration, current, timeStep)

