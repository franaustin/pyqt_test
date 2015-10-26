# -*- coding:utf-8 -*-
'''
Created on 2015-8-19
@author: sfit0212
@subject: pyqt.temperature
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temperature.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import wmi
import time
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(692, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.TemperatureTool = QtGui.QWidget(self.centralwidget)
        self.TemperatureTool.setGeometry(QtCore.QRect(150, 110, 381, 251))
        self.TemperatureTool.setObjectName(_fromUtf8("TemperatureTool"))
        self.label = QtGui.QLabel(self.TemperatureTool)
        self.label.setGeometry(QtCore.QRect(150, 10, 81, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.lcdNumber = QtGui.QLCDNumber(self.TemperatureTool)
        self.lcdNumber.setGeometry(QtCore.QRect(130, 80, 141, 101))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.percentLine = QtGui.QFrame(self.TemperatureTool)
        self.percentLine.setGeometry(QtCore.QRect(130, 210, 171, 21))
        self.percentLine.setFrameShape(QtGui.QFrame.HLine)
        self.percentLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.percentLine.setObjectName(_fromUtf8("percentLine"))
        self.line = QtGui.QFrame(self.TemperatureTool)
        self.line.setGeometry(QtCore.QRect(292, 80, 20, 141))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 692, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        #Add timer
        self.timerTemp = QtCore.QTimer(self.centralwidget)       
        MainWindow.setCentralWidget(self.centralwidget)    
               
        self.timerTemp.timeout.connect(self.cpu_mem)
        self.cpu_mem()
        self.timerTemp.start(1000)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Temperature", None))

    def cpu_mem(self): 
        c = wmi.WMI ()        
        #CPU类型和内存 
#        print c.Win32_Processor()
#        for processor in c.Win32_Processor(): 
#            #print "Processor ID: %s" % processor.DeviceID 
#            print "Process Name: %s" % processor.Name.strip() 
#        for Memory in c.Win32_PhysicalMemory(): 
#            print "Memory Capacity: %.fMB" %(int(Memory.Capacity)/1048576)
#             
#        for cpu in c.Win32_Processor(): 
#            timestamp = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()) 
#            print '%s | Utilization: %s: %d %%' % (timestamp, cpu.DeviceID, cpu.LoadPercentage) 
#                         
#        self.lcdNumber.display("%.1fC" % temp)
        cpu_obj = c.Win32_Processor()[0]
#        print cpu_obj
        temp = '%d'%cpu_obj.LoadPercentage
        self.lcdNumber.display('%s'%temp)
#        print c.Win32_PhysicalMemory()[0]
#        temp_obj = c.Win32_TemperatureProbe()[0]
#        print temp_obj     
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

