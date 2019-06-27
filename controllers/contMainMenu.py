from PyQt5 import QtWidgets, QtCore

import models._databaseConnection
import utilityClasses.paletteFunctions
import utilityClasses.utilityFunctions
import views.viewMainMenu


class ContMainMenu(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__ui = views.viewMainMenu.Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__p = utilityClasses.paletteFunctions.Pallet()
        self.__hideUnauthorizedMenuItems()

        self.__ui.treeWidgetMainMenu.itemClicked.connect(self.treeWidgetMainMenuClicked)
        self.__ui.treeWidgetExitMenu.itemClicked.connect(self.treeWidgetExitMenuClicked)
        self.__ui.actionMbiTabView.triggered.connect(self.actionMbiTabView)
        self.__ui.actionMbiWindowView.triggered.connect(self.actionMbiWindowView)

        self.__lastConnectionStatus = False     #used to see last conn status; faster than checking connection again
        self.__conn = models._databaseConnection.DBConnection()
        self.__checkConnectionStatus()

    def refreshMDIView(self):
        if self.__ui.mdiArea.viewMode() == 0:
            #windowed refresh
            self.actionMbiWindowView()
        #else:
        #    tab - no need to refresh view

    def __checkConnectionStatus(self):
        #recheck connection status ever 10 secconds - disable controls if disconnected
        if self.__conn.connect():
            self.__p.set_greenPallet()
            self.__ui.lblDBConnStatus.setPalette(self.__p)
            self.__ui.lblDBConnStatus.setText("Connected")
            self.__ui.lblDBConnStatusWarning.hide()
            self.__lastConnectionStatus = True
            self.__ui.treeWidgetMainMenu.setEnabled(True)
            self.__ui.mdiArea.setEnabled(True)
        else:
            self.__p.set_redPallet()
            self.__ui.lblDBConnStatus.setPalette(self.__p)
            self.__ui.lblDBConnStatus.setText("Disconnected")
            self.__ui.lblDBConnStatusWarning.show()
            self.__lastConnectionStatus = False
            self.__ui.treeWidgetMainMenu.setDisabled(True)
            self.__ui.mdiArea.setDisabled(True)
        QtCore.QTimer.singleShot(15000, lambda: self.__checkConnectionStatus())
        #self.__conn.closeConnection()

    def treeWidgetMainMenuClicked(self, item, column):
        #handel menu - if disconnected disable except for exit/logout btn's
        if self.__lastConnectionStatus == True:
            #Disable menu if not connected
            if item.text(column + 1) == "EntityMain":
                #Entity / Person
                self.__ui.treeWidgetMainMenu.expand(self.__ui.treeWidgetMainMenu.currentIndex())

            elif item.text(column + 1) == "Entity_MyEntity":
                #My Entity
                print("My Entity Clicked")
                import controllers.contMyEntity
                self.__MyEntity = models.modelMyEntity.ModelMyEntity()
                self.__subWindow = controllers.contMyEntity.ContMyEntity(self)
                self.__ui.mdiArea.addSubWindow(self.__subWindow)
                self.__subWindow.showNormal()
                #self.refreshMDIView()

            elif item.text(column) == "Property":
                print("Property clicked")

            elif item.text(column) == "Finances/Accounting":
                import controllers.contDlgSelectMyEntity
                self.__subWindow = controllers.contDlgSelectMyEntity.ContDlgSelectMyEntity(self)
                #self.__ui.mdiArea.addSubWindow(self.__subWindow)
                self.__subWindow.show()

            elif item.text(column) == "a":
                print("a")
            elif item.text(column) == "Maintenance":
                print("Maintenance")

    def treeWidgetExitMenuClicked(self, item, column):
        #this menu remain active even if disconnected
        if item.text(column) == "Sign Out":
            import contLogin
            self.__cntLogin = contLogin.ContLogin()
            self.__cntLogin.show()
            self.__keepConnectionOpen = True
            self.close()

        elif item.text(column) == "Exit":
            #self.__conn.closeConnection()
            self.close()

    def __hideUnauthorizedMenuItems(self):
        #hide Unauthorized Menu Items & columns
        userAccessLevel = 10
        print("User Access Level not yet implemented in contMainMenu funciton __hideUnauthorizedMenuItems")

        iterator = QtWidgets.QTreeWidgetItemIterator(self.__ui.treeWidgetMainMenu)
        while iterator.value():
            item = iterator.value()
            if int(userAccessLevel) < int(utilityClasses.utilityFunctions.nz(item.text(2), 10)):
                item.setHidden(True)
            iterator += 1
        self.__ui.treeWidgetMainMenu.hideColumn(1)
        self.__ui.treeWidgetMainMenu.hideColumn(2)

    def actionMbiTabView(self):
        #switch to tabbed view
        self.__ui.mdiArea.setViewMode(1)

    def actionMbiWindowView(self):
        self.showNormal()
        #window view & switch between tile & cascade
        self.__ui.mdiArea.setViewMode(0)
        self.__ui.mdiArea.tileSubWindows()
        self.showMaximized()

    def closeEvent(self, event):
        try:
            if self.__keepConnectionOpen == False:
                self.__conn.closeConnection()
        except:
            self.__conn.closeConnection()
        finally:
            event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    contMain = ContMainMenu()
    contMain.showMaximized()
    sys.exit(app.exec_())