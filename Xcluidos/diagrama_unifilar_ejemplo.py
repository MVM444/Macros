# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'diagrama_unifilar_ejemplo.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_DiagramaUnifilar(object):
    def setupUi(self, DiagramaUnifilar):
        if not DiagramaUnifilar.objectName():
            DiagramaUnifilar.setObjectName(u"DiagramaUnifilar")
        DiagramaUnifilar.resize(800, 817)
        self.centralwidget = QWidget(DiagramaUnifilar)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(600, 400))

        self.verticalLayout.addWidget(self.graphicsView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnAgregarComponente = QPushButton(self.centralwidget)
        self.btnAgregarComponente.setObjectName(u"btnAgregarComponente")

        self.horizontalLayout.addWidget(self.btnAgregarComponente)

        self.btnDibujarConexion = QPushButton(self.centralwidget)
        self.btnDibujarConexion.setObjectName(u"btnDibujarConexion")

        self.horizontalLayout.addWidget(self.btnDibujarConexion)


        self.verticalLayout.addLayout(self.horizontalLayout)

        DiagramaUnifilar.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(DiagramaUnifilar)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        DiagramaUnifilar.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(DiagramaUnifilar)
        self.statusbar.setObjectName(u"statusbar")
        DiagramaUnifilar.setStatusBar(self.statusbar)

        self.retranslateUi(DiagramaUnifilar)

        QMetaObject.connectSlotsByName(DiagramaUnifilar)

        self.label.setText("Diagrama Unifilar")
        self.pushButton.setText("Presionar")
        self.btnAgregarComponente.setText("Agregar Componente")
        self.btnDibujarConexion.setText("Dibujar Conexion")

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
    # setupUi

    def retranslateUi(self, DiagramaUnifilar):
        _translate = QCoreApplication.translate
        DiagramaUnifilar.setWindowTitle(_translate("DiagramaUnifilar", "Diagrama Unifilar"))
        self.label.setText(_translate("DiagramaUnifilar", "Diagrama Unifilar"))
        self.pushButton.setText(_translate("DiagramaUnifilar", "Presionar"))
        self.btnAgregarComponente.setText(_translate("DiagramaUnifilar", "Agregar Componente"))
        self.btnDibujarConexion.setText(_translate("DiagramaUnifilar", "Dibujar Conexion"))
    # retranslateUi

    def on_pushButton_clicked(self):
        print("Botón presionado")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    DiagramaUnifilar = QMainWindow()
    ui = Ui_DiagramaUnifilar()
    ui.setupUi(DiagramaUnifilar)
    DiagramaUnifilar.show()
    sys.exit(app.exec())

