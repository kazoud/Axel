import sys
from PySide6 import QtCore, QtWidgets
import pyqtgraph
from application import Ui_MainWindow

from SimulationController import SimulationController, PlotElement

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.simulationController = SimulationController()
        self.__initializeConnections()

    def __initializeConnections(self):
            self.ui.NeuronModelsButton.clicked.connect(self.IncrementStackedWidget) #def gonna need refactoring at some point
            self.ui.LIFButton.clicked.connect(self.IncrementStackedWidget)
            self.ui.LIFSimulationButton.clicked.connect(self.runSimulation)
            self.ui.LowRankRnnsSimulationButton.clicked.connect(self.runSimulation)
            self.ui.activityAlongMButton.clicked.connect(lambda: self.runSimulation(True))

            self.ui.NeuralNetworksButton.clicked.connect(self.NeuralNetworksPage)
            self.ui.LowRankRnnsButton.clicked.connect(self.IncrementStackedWidget)

            self.ui.spikeRateAdaptationCheckBox.clicked.connect(self.ToggleSpikeRateAdaptation)
            self.ui.synapticConductanceCheckBox.clicked.connect(self.ToggleSynapticConductance)

    @QtCore.Slot()
    def IncrementStackedWidget(self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
    def NeuralNetworksPage(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    @QtCore.Slot()
    def ToggleSpikeRateAdaptation(self):
        checked = self.ui.spikeRateAdaptationCheckBox.isChecked()
        self.ui.potassiumVrest.setEnabled(checked)
        self.ui.potassiumVrestLabel.setEnabled(checked)
        self.ui.potassiumConductance.setEnabled(checked)
        self.ui.potassiumConductanceLabel.setEnabled(checked)
        self.ui.potassiumTau.setEnabled(checked)
        self.ui.potassiumTauLabel.setEnabled(checked)

    @QtCore.Slot()
    def ToggleSynapticConductance(self):
        checked = self.ui.synapticConductanceCheckBox.isChecked()
        self.ui.synapseVrest.setEnabled(checked)
        self.ui.synapseVrestLabel.setEnabled(checked)
        self.ui.rmgSyn.setEnabled(checked)
        self.ui.rmgSynLabel.setEnabled(checked)

    @QtCore.Slot()
    def runSimulation(self, activityAlongM: bool = False):
        match self.ui.stackedWidget.currentIndex():
            case 2: #LIF
                plotData = self.simulationController.lifSequence(self.ui)
                self.__plotData(plotData)
            case 4: #Low-rank rnns
                if activityAlongM:
                    plotData = self.simulationController.activityAlongMSequence(self.ui)
                    self.__plotData(plotData, True)
                else:
                    plotData = self.simulationController.lowRankRnnsSequence(self.ui)
                    self.__plotData(plotData)
                
    def __plotData(self, data:list[PlotElement], dots: bool = False):
        plotWindows = []
        for plotElement in data:
            plotWindows.append(PlotWindow(plotElement.data, plotElement.xLabel, plotElement.yLabel, plotElement.title, dots))
        self.plotWindows = plotWindows
        for plotWindow in plotWindows:
            plotWindow.show()

class PlotWindow(QtWidgets.QMainWindow):
    def __init__(self,data: list[tuple[list[float],list[float]]], xlabel: str, ylabel: str, title: str, dots: bool):
        super().__init__()
        self.plotWidget = pyqtgraph.PlotWidget()
        self.setCentralWidget(self.plotWidget)
        plotItem = self.plotWidget.getPlotItem()
        plotItem.setLabels(bottom = xlabel, left = ylabel)
        plotItem.setTitle(title)
        if dots:
            for tuple in data:
                plotItem.plot(tuple[0],tuple[1],pen=None, symbol='o')
        else:
            for tuple in data:
                plotItem.plot(tuple[0],tuple[1])

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())