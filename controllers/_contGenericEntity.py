from PyQt5 import QtWidgets, QtCore
import utilityClasses.delegates

class ContGenericEntity(QtCore.QObject):
    def __init__(self, ui, contGeneric, parent):
        QtCore.QObject.__init__(self, parent)
        # setup & link delegates
        lineEditDelegate = utilityClasses.delegates.LineEditDelegate(ui.tableView)
        spinBoxDelegate = utilityClasses.delegates.SpinBoxDelegate(ui.tableView)
        ui.tableView.setItemDelegateForColumn(1, lineEditDelegate)
        ui.tableView.setItemDelegateForColumn(2, lineEditDelegate)
        ui.tableView.setItemDelegateForColumn(3, lineEditDelegate)
        ui.tableView.setItemDelegateForColumn(4, lineEditDelegate)
        ui.tableView.setItemDelegateForColumn(5, spinBoxDelegate)
        spinBoxDelegate.commitData.connect(contGeneric.delegateCommitData)
        lineEditDelegate.commitData.connect(contGeneric.delegateCommitData)