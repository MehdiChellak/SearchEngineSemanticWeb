# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface2.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextBrowser,QListWidget
import webbrowser
sys.path.append(".")
from class_web import WebSemanticBackEnd
import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context
class Ui_WebSemantic(object):
    
    def setupUi(self, WebSemantic):
        WebSemantic.setObjectName("WebSemantic")
        WebSemantic.resize(956, 815)
        self.resultSearch = pd.DataFrame()
        self.centralwidget = QtWidgets.QWidget(WebSemantic)
        self.centralwidget.setObjectName("centralwidget")
        self.titleSearch = QtWidgets.QLabel(self.centralwidget)
        self.titleSearch.setGeometry(QtCore.QRect(290, -30, 301, 181))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(16)
        self.titleSearch.setFont(font)
        self.titleSearch.setObjectName("titleSearch")
        self.sentenceSearchInput = QtWidgets.QLineEdit(self.centralwidget)
        self.sentenceSearchInput.setGeometry(QtCore.QRect(200, 100, 511, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.sentenceSearchInput.setFont(font)
        self.sentenceSearchInput.setText("")
        self.sentenceSearchInput.setObjectName("sentenceSearchInput")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(370, 190, 151, 41))
        self.searchButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchButton.setAcceptDrops(False)
        self.searchButton.setObjectName("searchButton")
        self.listWidgetLinks = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetLinks.setGeometry(QtCore.QRect(150, 250, 611, 491))
        self.listWidgetLinks.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.listWidgetLinks.setObjectName("listWidgetLinks")
        
        
        self.textBrowser = QTextBrowser()
        self.textBrowser.setOpenExternalLinks(True)        
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 760, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 750, 481, 41))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        WebSemantic.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WebSemantic)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 26))
        self.menubar.setObjectName("menubar")
        WebSemantic.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WebSemantic)
        self.statusbar.setObjectName("statusbar")
        WebSemantic.setStatusBar(self.statusbar)
        self.actionsave = QtWidgets.QAction(WebSemantic)
        self.actionsave.setObjectName("actionsave")
        self.actionopen = QtWidgets.QAction(WebSemantic)
        self.actionopen.setObjectName("actionopen")

        self.retranslateUi(WebSemantic)
        QtCore.QMetaObject.connectSlotsByName(WebSemantic)
        self.searchButton.clicked.connect(self.get_sentence_search)      

    def retranslateUi(self, WebSemantic):
        _translate = QtCore.QCoreApplication.translate
        WebSemantic.setWindowTitle(_translate("WebSemantic", "Web Semantic Search"))
        self.titleSearch.setText(_translate("WebSemantic", "Put Your Sentence Here"))
        self.searchButton.setText(_translate("WebSemantic", "Search "))
        __sortingEnabled = self.listWidgetLinks.isSortingEnabled()
        self.listWidgetLinks.setSortingEnabled(False)
        self.listWidgetLinks.setSortingEnabled(__sortingEnabled)
        self.actionsave.setText(_translate("WebSemantic", "save"))
        self.actionopen.setText(_translate("WebSemantic", "open"))
        self.label.setText(_translate("WebSemantic", "Copyright ©"))
        self.label_2.setText(_translate("WebSemantic", " Kawtar Khatim, Aimad El Hammdani, El Mehdi Chellak"))

    def get_sentence_search(self):
        backend  = WebSemanticBackEnd()
        resultSearch,requete = backend.main(self.sentenceSearchInput.text(),5)
        self.toShow(resultSearch,requete)
                
    # function with styled of pertinante words
    def styled_title(self,text):
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setText(text+" :")
        self.listWidgetLinks.addItem(item)
    
    # styled normal link
    def normale_link(self,link):
        #linko = '<a href="{0}">{1}</a>'
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText(link)
        self.listWidgetLinks.addItem(item)
    
    # racine function
    def toShow(self,D1,rr):
        self.listWidgetLinks.clear()
        self.listWidgetLinks.itemPressed.connect(self.getItem)
        D2=D1
        D1=D1.head(5)
        for i in range(len(D1)):
            self.normale_link(D1.iloc[i,3])     
        #X=pd.concat([pdSim,sujet,links], axis=1)  
        for sujet in rr:
            x=D2[(D2.sujet == sujet.capitalize())] 
            if len(x)!=0:
                self.styled_title("les liens similaire à: "+sujet)
            x1=x.head(5)
            for i in range(len(x1)):
                self.normale_link(x1.iloc[i,3])
        
        
    def toTest(self,D1,Requete):
        print(D1.sujet)
        
    def getItem(self, lstItem):
        webbrowser.open(lstItem.text())
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WebSemantic = QtWidgets.QMainWindow()
    ui = Ui_WebSemantic()
    ui.setupUi(WebSemantic)
    WebSemantic.show()
    sys.exit(app.exec_())
