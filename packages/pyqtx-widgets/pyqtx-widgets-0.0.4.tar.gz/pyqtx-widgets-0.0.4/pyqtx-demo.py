

import os
import sys

# HERE_PATH = os.path.abspath( os.path.dirname( __file__ ))
# if sys.path.count(HERE_PATH) == 0:
#     sys.path.insert(0, HERE_PATH)

# ROOT_PATH = os.path.abspath( os.path.join(HERE_PATH, "pyqtx"))
# if sys.path.count(ROOT_PATH) == 0:
#     sys.path.insert(0, ROOT_PATH)


from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from pyqtx import xwidgets
from pyqtx.xico import Ico





class MainWindow(QtWidgets.QWidget):


    def __init__(self):
        super().__init__()


        self.setWindowTitle("pyqtx Demo")
        self.setWindowIcon(Ico.logo())



        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)



        ## Toolbar
        self.toolbar = xwidgets.XToolBar()
        self.mainLayout.addWidget(self.toolbar)

        self.tbgActions = xwidgets.ToolBarGroup(title="Actions")
        self.toolbar.addWidget(self.tbgActions)
        self.tbgActions.addButton(ico=Ico.add, text="Add", callback=self.on_nothing)
        self.buttEdit = self.tbgActions.addButton(ico=Ico.edit, text="Edit", callback=self.on_nothing)
        self.buttDelete = self.tbgActions.addButton(ico=Ico.delete, text="Delete", callback=self.on_nothing)

        self.toolbar.addStretch()

        self.tbgRight = xwidgets.ToolBarGroup(title="Actions")
        self.toolbar.addWidget(self.tbgRight)
        self.tbgRight.addButton(ico=Ico.help, text="Help", callback=self.on_nothing)
        self.tbgRight.addButton(ico=Ico.refresh, text="Refresh", callback=self.on_refresh)


        # Status Bar
        self.statusBar = xwidgets.StatusBar(self)
        self.mainLayout.addWidget(self.statusBar)



    def on_nothing(self):
        s = "Click from %s " % self.sender().text()
        self.statusBar.showMessage(s)

    def on_refresh(self):
        self.statusBar.showMessage("Loading", info=True)
        self.statusBar.showBusy(True)
        #QtCore.QTimer.singleShot(3000, self.on_reply)



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit( app.exec_() )
