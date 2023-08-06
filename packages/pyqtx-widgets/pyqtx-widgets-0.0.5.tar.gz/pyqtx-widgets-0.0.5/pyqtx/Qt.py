# -*- coding: utf-8 -*-

"""
Converience import of Qt (idea is later to import pyside or PyQt5)

.. code-block::

    from Qt import Qt, QtCore, QtWidgets, QtSql, pyqtSignal
"""

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5 import QtNetwork

try:
    from PyQt5 import QtSql
except:
    pass



