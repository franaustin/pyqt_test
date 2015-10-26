# -*- coding:utf-8 -*-
'''
Created on 2015-8-20
@author: sfit0212
@subject: 21.不规则窗体 - ShapeWidget_test
'''

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
import sys  
  
class ShapeWidget(QWidget):  
    def __init__(self,parent=None):  
        super(ShapeWidget,self).__init__(parent)  
   
        pix=QPixmap("image/21.png","0",Qt.AvoidDither|Qt.ThresholdDither|Qt.ThresholdAlphaDither)  
        self.resize(pix.size())  
        self.setMask(pix.mask())  
        self.dragPosition=None  
    
    def mousePressEvent(self,event):  
        if event.button()==Qt.LeftButton:  
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()  
            event.accept()  
        if event.button()==Qt.RightButton:  
            self.close()  
  
    def mouseMoveEvent(self,event):  
        if event.buttons() & Qt.LeftButton:  
            self.move(event.globalPos()-self.dragPosition)  
            event.accept()  
  
    def paintEvent(self,event):  
        painter=QPainter(self)  
        painter.drawPixmap(0,0,QPixmap("image/21.png"))  
          
app=QApplication(sys.argv)  
form=ShapeWidget()  
form.show()  
app.exec_()  
