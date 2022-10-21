
import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

import systemInfo
 
from ui_splash_screen import Ui_SplashScreen
from ui_main import Ui_MainWindow

# variable global
counter = 0
jumper = 10

val_cpu=0

## ==> application window
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


       
        def setValue(self, slider, labelPercentage, progressBarName, color):

            
            value = slider.value()

            sliderValue = int(value)


            htmlText = """<p align="center"><span style=" font-size:50pt;">{VALUE}</span><span style=" font-size:40pt; vertical-align:super;">%</span></p>"""
            labelPercentage.setText(htmlText.replace("{VALUE}", str(sliderValue)))


            self.progressBarValue(sliderValue, progressBarName, color)


        self.ui.sliderCPU.valueChanged.connect(lambda: setValue(self, self.ui.sliderCPU, self.ui.labelPercentageCPU, self.ui.circularProgressCPU, "rgba(85, 170, 255, 255)"))
        self.ui.sliderGPU.valueChanged.connect(lambda: setValue(self, self.ui.sliderGPU, self.ui.labelPercentageGPU, self.ui.circularProgressGPU, "rgba(85, 255, 127, 255)"))
        self.ui.sliderRAM.valueChanged.connect(lambda: setValue(self, self.ui.sliderRAM, self.ui.labelPercentageRAM, self.ui.circularProgressRAM, "rgba(255, 0, 127, 255)"))

    
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.incrementCPU)
        self.timer.timeout.connect(self.incrementRAM)
       
        self.timer.start(1)

       
        self.ui.sliderGPU.setValue(1)
       

    def incrementCPU(self):
        self.ui.sliderCPU.setValue(systemInfo.getCPU())
    def incrementRAM(self):
        self.ui.sliderRAM.setValue(systemInfo.getRAM())

   
   
    def progressBarValue(self, value, widget, color):

       
        styleSheet = """
        QFrame{
        	border-radius: 110px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {COLOR});
        }
        """

       
       
        progress = (100 - value) / 100.0

       
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

       
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

       
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2).replace("{COLOR}", color)

       
        widget.setStyleSheet(newStylesheet)

## ==> THRAED CLASS eto ny thread 
class ThreadClass(QtCore.QThread):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        while 1:
            val=systemInfo.getCPU()
            val_cpu=val

## ==> SPLASHSCREEN WINDOW
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

       
        self.progressBarValue(0)

       
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

       
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)

       
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
       
        self.timer.start(15)

       
       
        self.show()
       

   
   
    def progress (self):
        global counter
        global jumper
        value = counter

        htmlText = """<p><span style=" font-size:68pt;">{VALUE}</span><span style=" font-size:58pt; vertical-align:super;">%</span></p>"""

        newHtml = htmlText.replace("{VALUE}", str(jumper))

        if(value > jumper):
           
            self.ui.labelPercentage.setText(newHtml)
            jumper += 10

       
       
        if value >= 100: value = 1.000
        self.progressBarValue(value)

       
        if counter > 100:
           
            self.timer.stop()

           
            self.main = MainWindow()
            self.main.show()

           
            self.close()

       
        counter += 0.5

   
   
    def progressBarValue(self, value):

       
        styleSheet = """
        QFrame{
        	border-radius: 150px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """

       
       
        progress = (100 - value) / 100.0

       
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

       
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

       
        self.ui.circularProgress.setStyleSheet(newStylesheet)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
