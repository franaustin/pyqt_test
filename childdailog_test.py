# -*- coding:utf-8 -*-
'''
Created on 2015-8-20
@author: sfit0212
@subject: pyqt.childdailog_test
'''
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
import sys  

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

class Ui_FirstDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 120, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.childPushButton = QtGui.QPushButton(Dialog)
        self.childPushButton.setGeometry(QtCore.QRect(160, 170, 75, 23))
        self.childPushButton.setObjectName(_fromUtf8("child"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "First Dialog", None))
        self.childPushButton.setText(_translate("Dialog", "子窗口", None))

class Ui_SecondDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 120, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.closePushButton = QtGui.QPushButton(Dialog)
        self.closePushButton.setGeometry(QtCore.QRect(160, 170, 75, 23))
        self.closePushButton.setObjectName(_fromUtf8("close"))
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Second Dialog", None))
        self.closePushButton.setText(_translate("Dialog", "关闭", None))
        
class Ui_ThirdDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 120, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.childPushButton = QtGui.QPushButton(Dialog)
        self.childPushButton.setGeometry(QtCore.QRect(160, 170, 75, 23))
        self.childPushButton.setObjectName(_fromUtf8("child"))
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Third Dialog", None))
        self.childPushButton.setText(_translate("Dialog", "动态加载", None))
        
          
class TestDialog(QDialog):  
    def __init__(self,parent=None):  
        super(TestDialog,self).__init__(parent)  
          
        firstUi=Ui_FirstDialog()  
        secondUi=Ui_SecondDialog()  
        self.thirdUi=Ui_ThirdDialog()  
          
        tabWidget=QTabWidget(self)  
        w1=QWidget()  
        firstUi.setupUi(w1)  
        w2=QWidget()  
        secondUi.setupUi(w2)  
        
        tabWidget.addTab(w1,"First")  
        tabWidget.addTab(w2,"Second")  
        tabWidget.resize(380,380)  
  
        self.connect(firstUi.childPushButton,SIGNAL("clicked()"),self.slotChild)  
        self.connect(secondUi.closePushButton,SIGNAL("clicked()"),self,SLOT("reject()"))  
        
        
    def slotChild(self):  
        dlg=QDialog()  
        self.thirdUi.setupUi(dlg)  
        #dlg.exec_()  
        self.connect(self.thirdUi.childPushButton,SIGNAL("clicked()"),self,self.slotui())
        
    def slotui(self):  
        from PyQt4 import uic
        dlg=uic.loadUi("firstdialog.ui")  
        dlg.exec_()     
               
app=QApplication(sys.argv)  
dialog=TestDialog()  
dialog.show()  
app.exec_()  