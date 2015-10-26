# -*- coding:utf-8 -*-
'''
Created on 2015-8-20
@author: sfit0212
@subject: 23.程序启动画面 - QSplashScreen_test
'''

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
import sys  
  
class MainWindow(QMainWindow):  
    def __init__(self,parent=None):  
        super(MainWindow,self).__init__(parent)  
        self.setWindowTitle("Splash Example")  
        edit=QTextEdit()  
        edit.setText("Splash Example")  
        self.setCentralWidget(edit)  
  
        self.resize(600,450)  
  
        QThread.sleep(3)  
          
app=QApplication(sys.argv)  
  
splash=QSplashScreen(QPixmap("image/23.png"))  
splash.show()  
app.processEvents()  
window=MainWindow()  
window.show()  
splash.finish(window)  
app.exec_()  


