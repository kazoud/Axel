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
            self.ui.NeuronModels.clicked.connect(self.IncrementStackedWidget)
            self.ui.LIF.clicked.connect(self.IncrementStackedWidget)
            self.ui.SimulationButton.clicked.connect(self.runSimulation)

            self.ui.spikeRateAdaptation.clicked.connect(self.ToggleSpikeRateAdaptation)

    @QtCore.Slot()
    def IncrementStackedWidget(self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
    @QtCore.Slot()
    def ToggleSpikeRateAdaptation(self):
        checked = self.ui.spikeRateAdaptation.isChecked()
        self.ui.potassiumVrest.setEnabled(checked)
        self.ui.potassiumVrestLabel.setEnabled(checked)
        self.ui.potassiumConductance.setEnabled(checked)
        self.ui.potassiumConductanceLabel.setEnabled(checked)
        self.ui.potassiumTau.setEnabled(checked)
        self.ui.potassiumTauLabel.setEnabled(checked)

    @QtCore.Slot()
    def runSimulation(self):
        match self.ui.stackedWidget.currentIndex():
            case 2: #LIF
                plotData = self.simulationController.lifSequence(self.ui)
                self.__plotData(plotData)
                
    def __plotData(self, data:list[PlotElement]):
        plotWindows = []
        for plotElement in data:
            plotWindows.append(PlotWindow(plotElement.xData, plotElement.yData, plotElement.xLabel, plotElement.yLabel, plotElement.title))
        self.plotWindows = plotWindows
        for plotWindow in plotWindows:
            plotWindow.show()

class PlotWindow(QtWidgets.QMainWindow):
    def __init__(self,x: list[float], y:list[float], xlabel: str, ylabel: str, title: str):
        super().__init__()
        self.plotWidget = pyqtgraph.PlotWidget()
        self.setCentralWidget(self.plotWidget)
        plotItem = self.plotWidget.getPlotItem()
        plotItem.setLabels(bottom = xlabel, left = ylabel)
        plotItem.setTitle(title)
        plotItem.plot(x,y)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())