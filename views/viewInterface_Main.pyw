# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewInterface_Main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import icons_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 614)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 1, 1, 1)
        self.scrollArea_InsertEdit = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_InsertEdit.sizePolicy().hasHeightForWidth())
        self.scrollArea_InsertEdit.setSizePolicy(sizePolicy)
        self.scrollArea_InsertEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_InsertEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_InsertEdit.setWidgetResizable(True)
        self.scrollArea_InsertEdit.setObjectName("scrollArea_InsertEdit")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 769, 85))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scrollArea_InsertEdit.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_InsertEdit, 4, 0, 1, 2)
        self.lblTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTitle.sizePolicy().hasHeightForWidth())
        self.lblTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")
        self.gridLayout.addWidget(self.lblTitle, 2, 0, 1, 2)
        self.btnCapturedRecords = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/navigation/icons/SectionClosed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/navigation/icons/SectionOpen.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnCapturedRecords.setIcon(icon)
        self.btnCapturedRecords.setCheckable(True)
        self.btnCapturedRecords.setChecked(True)
        self.btnCapturedRecords.setObjectName("btnCapturedRecords")
        self.gridLayout.addWidget(self.btnCapturedRecords, 5, 0, 1, 1)
        self.btnInsertEdit = QtWidgets.QPushButton(self.centralwidget)
        self.btnInsertEdit.setIcon(icon)
        self.btnInsertEdit.setCheckable(True)
        self.btnInsertEdit.setChecked(True)
        self.btnInsertEdit.setObjectName("btnInsertEdit")
        self.gridLayout.addWidget(self.btnInsertEdit, 3, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 5, 1, 1, 1)
        self.scrollArea_CapturedRecords = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_CapturedRecords.sizePolicy().hasHeightForWidth())
        self.scrollArea_CapturedRecords.setSizePolicy(sizePolicy)
        self.scrollArea_CapturedRecords.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_CapturedRecords.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_CapturedRecords.setWidgetResizable(True)
        self.scrollArea_CapturedRecords.setObjectName("scrollArea_CapturedRecords")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 769, 360))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.scrollAreaWidgetContents_3)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 1, 0, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.scrollArea_CapturedRecords.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout.addWidget(self.scrollArea_CapturedRecords, 7, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(4, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolbNav = QtWidgets.QToolBar(MainWindow)
        self.toolbNav.setMovable(False)
        self.toolbNav.setObjectName("toolbNav")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbNav)
        self.actionNewRecord = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/addNewRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewRecord.setIcon(icon2)
        self.actionNewRecord.setObjectName("actionNewRecord")
        self.actionFirst = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToFirstRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFirst.setIcon(icon3)
        self.actionFirst.setText("")
        self.actionFirst.setObjectName("actionFirst")
        self.actionPrev = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToPrevRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev.setIcon(icon4)
        self.actionPrev.setText("")
        self.actionPrev.setObjectName("actionPrev")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToNextRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon5)
        self.actionNext.setText("")
        self.actionNext.setObjectName("actionNext")
        self.actionLast = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToLastRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLast.setIcon(icon6)
        self.actionLast.setText("")
        self.actionLast.setObjectName("actionLast")
        self.actionRecordNr = QtWidgets.QAction(MainWindow)
        self.actionRecordNr.setObjectName("actionRecordNr")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/deleteRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon7)
        self.actionDelete.setObjectName("actionDelete")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionFind = QtWidgets.QAction(MainWindow)
        self.actionFind.setIcon(icon1)
        self.actionFind.setObjectName("actionFind")
        self.toolbNav.addAction(self.actionFirst)
        self.toolbNav.addAction(self.actionPrev)
        self.toolbNav.addAction(self.actionRecordNr)
        self.toolbNav.addAction(self.actionNext)
        self.toolbNav.addAction(self.actionLast)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Entity"))
        self.lblTitle.setText(_translate("MainWindow", "Title"))
        self.btnCapturedRecords.setText(_translate("MainWindow", "Captured Records"))
        self.btnInsertEdit.setText(_translate("MainWindow", "Insert/Edit Record"))
        self.pushButton_2.setText(_translate("MainWindow", "Search"))
        self.toolbNav.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNewRecord.setText(_translate("MainWindow", "New"))
        self.actionNewRecord.setToolTip(_translate("MainWindow", "Add a New Record"))
        self.actionFirst.setToolTip(_translate("MainWindow", "Go to First Record"))
        self.actionPrev.setToolTip(_translate("MainWindow", "Go to Previous Record"))
        self.actionNext.setToolTip(_translate("MainWindow", "Go to Next Record"))
        self.actionLast.setToolTip(_translate("MainWindow", "Go to Last Record"))
        self.actionRecordNr.setText(_translate("MainWindow", "Record ... of ..."))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setToolTip(_translate("MainWindow", "Delete Record/s"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save all Records"))
        self.actionFind.setText(_translate("MainWindow", "Find"))
        self.actionFind.setToolTip(_translate("MainWindow", "Find a record"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

