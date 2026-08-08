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
    current:str
    timeStep:float
    spikeRateAdaptation:bool
    potassiumVrest:float
    potassiumConductanceIncrement:float
    potassiumTau:float

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
        #interspikeRateAnalysis = True
        inputs = self.__extractInputs(widget)

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
                                                                    inputs.potassiumTau)

        plotElements.append(PlotElement(xVoltage, yVoltage, voltageXlabel, voltageYlabel, voltageTitle))
        plotElements.append(PlotElement(timeValues, currentValues, currentXlabel, currentYLabel, currentTitle))

        #it works but it's cumbersome for now
        # if (interspikeRateAnalysis):
        #         xInterspike, yInterspike = leakyIntegrateFire.interspikeIntervalRate(inputs.r, inputs.vRest, inputs.vThreshold, inputs.vReset, inputs.tau, linear = False)
        #         plotElements.append(PlotElement(xInterspike,yInterspike, "current (nA)", "Interspike Interval Rate (Hz)", ""))

        return plotElements

    def __extractInputs(self,widget : QtWidgets.QWidget)-> Inputs:
        vRest = widget.vRest.value()
        vThreshold = widget.vThreshold.value()
        vReset = widget.vReset.value()
        r = widget.r.value()
        tau = widget.tau.value()
        duration = widget.duration.value()
        current = widget.current.toPlainText()
        timeStep = widget.timeStep.value()
        spikeRateAdaptation = widget.spikeRateAdaptation.isChecked()
        potassiumVrest = widget.potassiumVrest.value()
        potassiumConductanceIncrement = widget.potassiumConductance.value()
        potassiumTau = widget.potassiumTau.value()

        return Inputs(vRest,vThreshold, vReset, r, tau, duration, current, timeStep, spikeRateAdaptation, potassiumVrest, potassiumConductanceIncrement, potassiumTau)

