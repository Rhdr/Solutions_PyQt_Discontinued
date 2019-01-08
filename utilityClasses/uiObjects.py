from PyQt5 import QtWidgets, QtCore
class QLineEditExt(QtWidgets.QLineEdit):
    gotFocus = QtCore.pyqtSignal()
    lostFocus = QtCore.pyqtSignal()
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)

    def focusInEvent(self, QFocusEvent):
        self.gotFocus.emit()
        super(QLineEditExt, self).focusInEvent(QFocusEvent)

    def focusOutEvent(self, QFocusEvent):
        self.lostFocus.emit()
        super(QLineEditExt, self).focusOutEvent(QFocusEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()
        super(QLineEditExt, self).mouseReleaseEvent(QMouseEvent)