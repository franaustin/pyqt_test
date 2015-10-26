# -*- coding:utf-8 -*-
'''
Created on 2015-8-19
@author: sfit0212
@subject: pyqt.qt_gui
'''
import sys  
import time
from PyQt4 import QtGui  

app = QtGui.QApplication(sys.argv)  
label = QtGui.QLabel("Hello Qt!")  
label.show()   
time.sleep(2000)

sys.exit(app.exec_()) 