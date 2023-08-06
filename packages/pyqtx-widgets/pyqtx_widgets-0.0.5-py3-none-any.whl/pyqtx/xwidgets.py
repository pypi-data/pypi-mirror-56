# -*- coding: utf-8 -*-


from pyqtx.Qt import QtCore, QtGui, QtWidgets, Qt, pyqtSignal
from pyqtx.xico import Ico

DEFAULT_SPACING = 0
DEFAULT_MARGIN = 0
DEFAULT_BUTTON_WIDTH = 80



#=====================================================
# Layouts

def hlayout(spacing=DEFAULT_SPACING, margin=DEFAULT_MARGIN):
    """Convenience function to create a QHBoxLayout"""
    lay = QtWidgets.QHBoxLayout()
    if isinstance(margin, bool):
        margin = DEFAULT_SPACING
    if isinstance(spacing, bool):
        spacing = DEFAULT_SPACING
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    return lay

def vlayout(spacing=DEFAULT_SPACING, margin=DEFAULT_MARGIN):
    """Convenience function to create a QVBoxLayout"""
    lay = QtWidgets.QVBoxLayout()
    if isinstance(margin, bool):
        margin = DEFAULT_SPACING
    if isinstance(spacing, bool):
        spacing = DEFAULT_SPACING
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    return lay



class XButtonGroup(QtWidgets.QButtonGroup):
    def __init__( self, parent, callback=None, exclusive=True):
        super().__init__( self)

        self.setExclusive(exclusive)
        if callback:
            self.buttonClicked.connect(callback)

class XToolButton( QtWidgets.QToolButton ):

    def __init__( self, parent=None, colors=None, style=None,
                    autoRaise=True, menu=None,
                    text="", tooltip=None, ico=None, iconTop=False, iconSize=16,
                    bold=False, disabled=False,
                    width=None, popup=False,
                    clicked=None, ki=None,
                    both=True, checkable=False
                    ):

        super().__init__(parent)

        self.colors = colors


        if ki:
            self.setProperty("ki", ki)

        if width:
            self.setFixedWidth(width)

        if style:
            self.setStyleSheet(style)

        if disabled:
            self.setDisabled(True)


        if both:
            if iconTop:
                self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
            else:
                self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon)
        else:
            self.setToolButtonStyle( Qt.ToolButtonIconOnly)

        if checkable:
            self.setCheckable(True)

        if clicked:
            self.clicked.connect(clicked)

        if tooltip:
            self.setToolTip(tooltip)

        if text:
            self.setText(text)

        #== Font
        # Try and avoid styleSheet maybe
        if bold:
            self.setBold(bold)
        # < font

        if ico:
            self.setIco(ico)
            if iconSize:
                if isinstance(iconSize, list):
                    self.setIconSize( QtCore.QSize(iconSize[0],iconSize[0]))
                else:
                    self.setIconSize( QtCore.QSize(iconSize, iconSize))

        self.setAutoRaise(autoRaise)
        if popup:
            self.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        if menu:
            self.setMenu(QtWidgets.QMenu())

    @property
    def ki(self):
        return self.property("ki")

    def setIco(self, ico, iconSize=16):
        self.setIcon(Ico.icon(ico))
        self.setIconSize( QtCore.QSize(iconSize, iconSize))

    def setEnabled(self, state):
        if self.colors:
            color = self.colors[1] if state else self.colors[0]
            self.setStyleSheet("background-color: %s" % color)
        QtWidgets.QToolButton.setEnabled(self, state)

    def setBold(self, state):
        f = self.font()
        f.setBold(state)
        self.setFont(f)

class Spacer( QtWidgets.QWidget ):

    def __init__( self, parent=None, width=None ):
        super().__init__()

        if width:
            self.setFixedWidth(width)
        else:
            sp = QtWidgets.QSizePolicy()
            sp.setHorizontalPolicy( QtWidgets.QSizePolicy.Expanding )
            self.setSizePolicy( sp )


class XTreeWidgetItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, parent=None):
        super().__init__()


    def set_row_bg(self, color):
        for col_idx in range(0, self.columnCount()):
            self.setBackground(col_idx, QtGui.QColor(color))

    def set_row_fg(self, color):
        for col_idx in range(0, self.columnCount()):
            self.setForeground(col_idx, QtGui.QColor(color))

    def set_cell_bg(self, col_idx, color):
        self.setBackground(col_idx, QtGui.QColor(color))

    def set_cell_fg(self, col_idx, color):
        self.setForeground(col_idx, QtGui.QColor(color))

    def i(self, cidx):
        return ut.to_int(self.text(cidx))

    def set_bold(self, idx, state=True):
        f = self.font(idx)
        f.setBold(state)
        self.setFont(idx, f)

    def set(self, cidx, text=None, ico=None):
        if ico:
            self.setIcon(cidx, Ico.i(ico))
        if text:
            self.setText(cidx, str(text))

class CancelButton( QtWidgets.QPushButton ):
    def __init__( self, parent, text="Cancel", callback=None ):
        super().__init__()

        self.setText( text )
        self.setIcon( Ico.icon( Ico.cancel ) )
        if callback:
            self.clicked.connect(callback)
            return
        self.clicked.connect(parent.on_cancel)

class SaveButton( QtWidgets.QPushButton ):
    def __init__( self, parent, text="Save", ico=None, callback=None, width=None):
        super().__init__()

        self.dirty = False
        if width:
            self.setMinimumWidth( width )
        self.setText( text )
        self.setIcon( Ico.i( ico if ico else Ico.save ) )

        if callback:
            self.clicked.connect(callback)
        else:
            self.clicked.connect(parent.on_save)

    def set_dirty(self):
        self.dirty = True
        self.up_style()

    def clear_dirty(self):
        self.dirty = False
        self.up_style()

    def up_style(self):
        c = "pink" if self.dirty else "white"
        self.setStyleSheet("background-color: %s;" % c)

class DeleteButton( QtWidgets.QPushButton ):
    def __init__( self, parent, text="Delete", callback=None ):
        super().__init__()

        self.setText( text )
        self.setIcon( Ico.icon( Ico.delete ) )
        if callback:
            self.clicked.connect(callback)
            return
        self.clicked.connect(parent.on_delete)


class FormActionBar(QtWidgets.QWidget):

    def __init__(self, parent, delete=False, cancel=True, refresh=True, text="Save"):
        super().__init__()

        self.outerLayout = vlayout(margin=5, spacing=5)
        self.setLayout(self.outerLayout)

        self.outerLayout.addSpacing(10)

        lbl = XLabel(style="background-color: #cccccc;")
        lbl.setFixedHeight(1)
        self.outerLayout.addWidget(lbl)

        self.mainLayout = hlayout(margin=5, spacing=5)
        self.outerLayout.addLayout(self.mainLayout)




        if delete:
            self.buttDelete = DeleteButton(parent)
            self.mainLayout.addWidget(self.buttDelete)



        self.statusBar = StatusBar(self, refresh=refresh)
        self.mainLayout.addWidget(self.statusBar)

        #self.mainLayout.addStretch(1)
        if cancel:
            self.buttCancel = CancelButton(parent)
            self.mainLayout.addWidget(self.buttCancel)


        self.buttSave = SaveButton(parent, text=text)
        self.mainLayout.addWidget(self.buttSave)

    def showMessage(self, mess, timeout=None, warn=None, info=None):
        self.statusBar.showMessage(mess, timeout=timeout, warn=warn, info=info)

    def set_busy(self, state):
        self.statusBar.set_busy(state)

    def set_dirty(self, *args):
        self.buttSave.set_dirty()

    def clear_dirty(self):
        self.buttSave.clear_dirty()
    @property
    def dirty(self):
        return self.buttSave.dirty

C_FG = "color: #222222;"
C_BG = "background-color: white;"

C_FG_FOCUS = "color: black;"
C_BG_FOCUS = "background-color: #FFFA93"


class XLineEdit( QtWidgets.QLineEdit ):

    sigFocused = pyqtSignal(bool)
    sigMove = pyqtSignal(bool)
    sigDoubleClicked = pyqtSignal()

    def __init__( self, parent=None, show_focus=False, width=None,
                  dirty=True, changed=None ):
        super().__init__()

        self._show_focus = show_focus

        if width:
            self.setFixedWidth(width)

        if dirty:
            if hasattr(parent, "set_dirty"):
                self.textChanged.connect(parent.set_dirty)
        if changed:
            self.textChanged.connect(changed)

    def stripped(self):
        self.setText( self.text().strip() )
        return self.text()

    def s(self):
        return self.stripped()

    def setText(self, txt):
        if txt == None:
            self.setText("")
            return
        super().setText(txt.strip())

    def set_bold(self, state):
        f = self.font()
        f.setBold(state)
        self.setFont(f)

    def mouseDoubleClickEvent_MAYBE(self, ev):
        ev.ignore()
        self.sigDoubleClicked.emit(ev)

    def focusInEvent(self, ev):
        """Changes style if show_focus """
        if self._show_focus:
            self.setStyleSheet(C_FG_FOCUS + C_BG_FOCUS)
        QtWidgets.QLineEdit.focusInEvent(self, ev)
        self.sigFocused.emit(True)

    def focusOutEvent(self, ev):
        """Changes style if show_focus """
        if self._show_focus:
            self.setStyleSheet(C_FG + C_BG)

        QtWidgets.QLineEdit.focusOutEvent(self, ev)
        self.sigFocused.emit(False)


    def keyPressEvent(self, ev):
        """Clear field with esc, otherwise passthough"""
        if ev.key() == Qt.Key_Escape:
            self.setText("")
            return
        if ev.key() == Qt.Key_Up:
            self.sigMove.emit(False)
            return
        if ev.key() == Qt.Key_Down:
            self.sigMove.emit(True)
            return
        QtWidgets.QLineEdit.keyPressEvent( self, ev )





PAGE_SIZE = 100


class StatusBar(QtWidgets.QWidget):
    """A QWidget with many embedded widgets for StatusBar"""

    sigRefresh = pyqtSignal()

    def __init__(self, parent, refresh=True, status=True,
                 pager=False, mode=True):
        super().__init__()

        if isinstance(parent, bool):
            print("STATUSBar is not correct parent")
            # print Tantrum
            return

        self._lastReply = None

        self._refresh = refresh
        self._status = status

        self.mainLayout = QtWidgets.QHBoxLayout()
        m = 0
        self.mainLayout.setContentsMargins(m, m, m, m)
        self.setLayout(self.mainLayout)

        ##=======================================================================
        ### Pager Widget
        self.pagerWidget = None
        if pager:
            self.pagerWidget = QtWidgets.QWidget()
            self.pagerWidget.setMinimumWidth(300)
            self.mainLayout.addWidget(self.pagerWidget)
            pagerLayout = QtWidgets.QHBoxLayout()
            pagerLayout.setContentsMargins(0, 2, 0, 2)
            pagerLayout.setSpacing(2)
            self.pagerWidget.setLayout(pagerLayout)

            pagerLayout.addWidget(QtWidgets.QLabel("Page:"))

            self.buttonGroupPager = QtWidgets.QButtonGroup(self)
            self.buttonGroupPager.setExclusive(True)

            for i in range(1, 10):
                butt = QtWidgets.QToolButton()
                butt.setText(" %s " % i)
                butt.setStyleSheet("font-weight: bold;")
                butt.setCheckable(True)
                butt.setVisible(False)
                pagerLayout.addWidget(butt)
                self.buttonGroupPager.addButton(butt, i)

            pagerLayout.addStretch(20)
            self.buttonGroupPager.buttonClicked.connect(self.on_page_button)
            # self.connect( self.buttonGroupPager, QtCore.SIGNAL( "buttonClicked(QAbstractButton*)" ), self.on_page_button )

        ##=======================================================================
        ## Status Bar
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setSizeGripEnabled(False)
        self.showMessage(" ")
        self.mainLayout.addWidget(self.statusBar, 1)

        ## Main layout to add
        self.extrasLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.extrasLayout, 0)

        self.lblCount = QtWidgets.QLabel()
        self.mainLayout.addWidget(self.lblCount)

        ## Status widget setup
        """
        pagerLayout.addWidget(QtWidgets.QLabel("Page "))
        self.lblPage = QtWidgets.QLabel("-")
        self.lblPage.setFrameStyle(QtWidgets.QFrame.Sunken)
        self.lblPage.setFrameShape(QtWidgets.QFrame.Panel)
        pagerLayout.addWidget(self.lblPage)

        pagerLayout.addWidget(QtWidgets.QLabel(" of "))
        self.lblPages = QtWidgets.QLabel("-")
        self.lblPages.setFrameStyle(QtWidgets.QFrame.Sunken)
        self.lblPages.setFrameShape(QtWidgets.QFrame.Panel)
        pagerLayout.addWidget(self.lblPages)
        """

        self.lblStatus = QtWidgets.QLabel()
        self.lblStatus.setFixedWidth(30)
        self.lblStatus.setStyleSheet("background-color: #efefef;")
        self.mainLayout.addWidget(self.lblStatus)


        #== Progress Bar
        progressWidget = QtWidgets.QWidget()
        progressWidget.setFixedWidth(40)
        #progressWidget.setMaximumWidth(200)
        self.mainLayout.addWidget(progressWidget)

        progressLayout = QtWidgets.QHBoxLayout()
        m = 0
        progressLayout.setContentsMargins(m, m, m, m)
        progressWidget.setLayout(progressLayout)

        self.progress = QtWidgets.QProgressBar(self)
        # self.progress.setFixedWidth( 40 )
        self.progress.setFixedHeight(15)
        # self.setContentsMargins( m, m, m, m )
        self.progress.setMinimum(0)
        self.progress.setMaximum(1)
        self.progress.setInvertedAppearance(False)
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        # self.connect( self.progress, QtCore.SIGNAL('valueChanged(int)'), self.on_progress_value_changed)
        progressLayout.addWidget(self.progress)


        ################################################################
        ## Refrehsing Button
        self.buttRefresh = None
        self.popMenu = None
        if refresh:
            self.buttRefresh = QtWidgets.QToolButton()
            self.mainLayout.addWidget(self.buttRefresh)

            self.buttRefresh.setIcon(Ico.i(Ico.refresh))
            # self.buttRefresh.setFlat(True)
            self.buttRefresh.setAutoRaise(True)
            self.buttRefresh.setIconSize(QtCore.QSize(16, 16))
            self.buttRefresh.setStyleSheet("padding: 0px;")
            self.buttRefresh.clicked.connect(self.on_refresh)
            if hasattr(parent, "on_refresh"):
                self.buttRefresh.clicked.connect(parent.on_refresh)


    def show_count(self, total=0, count=0, single="", multi="",):

        s = "%s of %s %s" % (count, total, multi)
        self.lblCount.setText(s)


    def on_refresh(self):
        self.sigRefresh.emit()

    ##==============================================================================
    ## Pager
    ##===============================================================================
    def set_pager(self, items):

        count = len(items)
        if count <= PAGE_SIZE:
            page_count = 1
        else:
            page_count = int(count / PAGE_SIZE)
            if count - (page_count * PAGE_SIZE) > 0:
                page_count = page_count + 1

        for b in self.buttonGroupPager.buttons():

            # no, ok = b.text().toInt()
            # b.setEnabled( no <= page_count )
            page_no = self.buttonGroupPager.id(b)
            b.setVisible(page_no <= page_count)

            start = (PAGE_SIZE * page_no) - PAGE_SIZE
            if page_no < page_count:
                end = start + PAGE_SIZE
            else:
                end = count
            b.setProperty("start", QtCore.QVariant(start))
            b.setProperty("end", QtCore.QVariant(end))
            b.setToolTip("%s - %s" % (start + 1, end + 1))
            # print "set_pager", start, end
            if page_no == 1 and count > 0:
                b.setChecked(True)

    def page(self):

        butt = self.buttonGroupPager.checkedButton()
        # print "butt", butt
        if butt == None:
            return 0, 0
        start = int(butt.property("start"))
        end = int(butt.property("end"))
        return start, end

    def on_page_button(self, butt):
        if self.pagerWidget == None:
            return
        start = int(butt.property("start").toString())
        end = int(butt.property("end").toString())
        self.emit(QtCore.SIGNAL("page"), start, end)

    ###################################################################
    def showMessage(self, mess, timeout=None, warn=None, info=None):
        if warn:
            self.statusBar.setStyleSheet("color: #990000;")
        elif info:
            self.statusBar.setStyleSheet("color: #3361C2;")
        else:
            self.statusBar.setStyleSheet("color: black;")

        if timeout == None:
            self.statusBar.showMessage(mess)
        else:
            self.statusBar.showMessage(mess, timeout)

    def addWidget(self, widget):
        self.extrasLayout.addWidget(widget)

    def addPermanentWidget(self, widget):
        self.mainLayout.addWidget(widget)

    def insertPermanentWidget(self, idx, widget):
        self.statusBar.insertPermanentWidget(idx, widget)

    def on_menu(self, point):
        # print "on_menu", point
        self.popMenu.exec_(self.mapToGlobal(point))

    def set_status(self, sta):

        self.lblStatus.setText(sta.status)
        if sta.busy == False:
            self.progress_stop()
            return

        self.progress_start()

    def set_reply(self, reply):
        self.lblStatus.setText(reply.status)
        if reply.busy:
            self.progress_start()
            return

        self.progress_stop()
        self._reply = reply
        if reply.error:
            self.showMessage(reply.error, warn=True)

    def progress_start(self):
        self.progress.setMaximum(0)
        self.progress.setVisible(True)
        if self.buttRefresh:
            self.buttRefresh.setDisabled(True)

    def progress_stop(self):
        self.progress.setVisible(False)
        self.progress.setMaximum(1)
        if self.buttRefresh:
            self.buttRefresh.setDisabled(False)

    def showBusy(self, state):
        if state:
            self.progress_start()
        else:
            self.progress_stop()


class XComboBox( QtWidgets.QComboBox ):

    sigFocus = pyqtSignal(bool)

    def __init__( self, parent=None, show_focus=False, editable=None, dirty=True ):
        super().__init__()

        self._show_focus = show_focus

        if editable:
            self.setEditable(True)

        if dirty and parent:
            #self.activated.connect(parent.set_dirty)
            self.currentIndexChanged.connect(parent.set_dirty)
            self.currentTextChanged.connect(parent.set_dirty)

    def stripped(self):
        self.setEditText( self.currentText().strip() )
        return self.currentText()

    def s(self):
        return self.stripped()

    def set_text(self, txt):
        if txt == None:
            self.setEditText("")
            return
        self.setEditText(txt.strip())

    def get_index(self, xid):
        if xid == None or xid == "":
            return None
        idx =  self.findData(str(xid), QtCore.Qt.UserRole, QtCore.Qt.MatchExactly)
        if idx == -1:
            return None
        return idx

    def val(self):
        v = self.get_id()
        if v == None:
            return ""
        return v


    def get_id(self, as_int=True):

        s = self.itemData(self.currentIndex())
        if s == None:
            return None
        if as_int:
            return int(s)
        return s

    def select_id(self, sid):
        idx = self.findData(str(sid))
        if idx != -1:
            self.setCurrentIndex(idx)

    def setItemDisabled(self, idx, state=True):
        #http://qt-project.org/forums/viewthread/27969
        if state:
            self.setItemData(idx, 0, QtCore.Qt.UserRole - 1)
        else:
            self.setItemData(idx, 33, QtCore.Qt.UserRole - 1)

    def focusInEvent(self, ev):
        QtWidgets.QComboBox.focusInEvent(self, ev)
        self.sigFocus.emit(True)
        if self._show_focus:
            if self.isEditable():
                self.setStyleSheet(C_FG_FOCUS + C_BG_FOCUS)
            else:
                self.setStyleSheet(C_FG_FOCUS)

    def focusOutEvent(self, ev):
        if self._show_focus:
            if self.isEditable():
                self.setStyleSheet(C_FG + C_BG)
            else:
                self.setStyleSheet(C_FG)
        QtWidgets.QComboBox.focusOutEvent(self, ev)

    def keyPressEvent(self, ev):

        if self._show_focus and not self.isEditable():
            self.showPopup()
        QtWidgets.QComboBox.keyPressEvent(self, ev)

class XTextEdit( QtWidgets.QTextEdit):

    #sigFocused = pyqtSignal(bool)
    #sigMove = pyqtSignal(bool)

    def __init__( self, parent=None, dirty=None ):
        super().__init__()

        if dirty:
            self.textChanged.connect(parent.set_dirty)

    def stripped(self):
        self.setText( self.toPlainText().strip() )
        return self.toPlainText()

    def s(self):
        return self.stripped()


class TimeRangeEdit(QtWidgets.QWidget):

    def __init__( self, parent=None, dirty=None ):
        super().__init__()


        self.mainLayout = hlayout(spacing=2)
        self.setLayout(self.mainLayout)

        self.chk = QtWidgets.QCheckBox()
        self.mainLayout.addWidget(self.chk, 0)
        self.chk.clicked.connect(self.on_checked)

        self.timeStart = QtWidgets.QTimeEdit()
        self.timeStart.setDisplayFormat("h.mm ap")
        self.mainLayout.addWidget(self.timeStart, 0)
        self.timeStart.setDisabled(True)

        self.timeEnd = QtWidgets.QTimeEdit()
        self.timeEnd.setDisplayFormat("h.mm ap")
        self.mainLayout.addWidget(self.timeEnd, 0)
        self.timeEnd.setDisabled(True)

        self.setMaximumWidth(190)

    def on_checked(self, v=None):
        self.timeStart.setDisabled(not self.chk.isChecked())
        self.timeEnd.setDisabled(not self.chk.isChecked())
        self.timeStart.setFocus()

    def setTimes(self, start, end):
        if start == None or start == "00:00:00":
            return

        self.timeStart.setTime(QtCore.QTime.fromString(start))
        self.timeEnd.setTime(QtCore.QTime.fromString(end))

        self.chk.setChecked(True)
        self.timeStart.setDisabled(False)
        self.timeEnd.setDisabled(False)


    def time_start(self):
        if self.chk.isChecked():
            return self.timeStart.time().toString("hh:mm:ss")
        return None

    def time_end(self):
        if self.chk.isChecked():
            return self.timeEnd.time().toString("hh:mm:ss")
        return None



class XToolBar(QtWidgets.QToolBar):

    def __init__( self, parent=None):
        super().__init__()

    def addStretch(self):

        widget = QtWidgets.QWidget()
        sp = QtWidgets.QSizePolicy()
        sp.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        widget.setSizePolicy(sp)

        self.addWidget(widget)



class XSplitter(QtWidgets.QSplitter):

    def __init__( self, parent=None):
        super().__init__()

class VWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.setLayout(vlayout())


class XLabel(QtWidgets.QLabel):

    sigClicked = pyqtSignal()
    sigDoubleClicked = pyqtSignal()

    def __init__( self, parent=None, bold=False,
                  style=None, base_style="", align=None,
                  text=None, frame=None, expanding=True,
                  wrap=False, hover_color=None,
                  height=None, width=None):
        super().__init__()

        self.hover_color = hover_color

        self.base_style = base_style
        self.style = ""
        if style != None:
            self.style = style
        self.setStyleSheet(self.style)

        if bold:
            f = self.font()
            f.setBold(True)
            self.setFont(f)

        if align != None:
            self.setAlignment(align)

        if text:
            self.setText(text)

        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)

        self.setWordWrap(wrap)

        if frame:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)

        if self.hover_color:
            self.set_border("#dddddd")

    def setStyleSheet(self, sty):
        QtWidgets.QLabel.setStyleSheet(self, sty + self.base_style)



class HeaderBar( QtWidgets.QWidget ):

    def __init__( self, parent, title=None, bg_dark="#dddddd"):
        super().__init__()


        self.fg_color = "black"
        self.bg_dark = bg_dark
        self.bg_light = "#dddddd"


        #########################################################
        ## Container Layout
        self.containerLayout = hlayout()
        self.setLayout( self.containerLayout )

        #self.width_height = 22 if self.subTitle  else 16

        #self.setFixedHeight(40 if self.subTitle else 30)

        #########################################################
        ## mainWidget Container widget##

        self.lblCTop = XLabel(height=2)
        self.containerLayout.addWidget(self.lblCTop)


        mainWidget = QtWidgets.QWidget()
        self.containerLayout.addWidget( mainWidget, 10 )
        mainWidget.setStyleSheet( "background-color: %s;" %  self.bg_light )

        ### Main Box accross
        mainHBox = hlayout()
        mainWidget.setLayout( mainHBox )


        ### Icon Widget
        self.iconWidget = XLabel(style="background: transparent;")
        #self.iconWidget.setPixmap( self.get_pixmap( self.ico , self.width_height ) )
        #self.iconWidget.setContentsMargins( 10, 0, 0, 0 )
        mainHBox.addWidget( self.iconWidget, 0 )

        ### Vertical Box for Labels
        vLabelBox = vlayout() #margin=[10, 5, 0, 5])
        #vLabelBox.setContentsMargins( 10, 5, 0, 5 )
        mainHBox.addLayout( vLabelBox, 2 )


        ### Main Label
        sty = " padding: 5px; font-size: 14pt; color: %s;" % ( self.fg_color )
        self.mainLabel = XLabel( text=title, style=sty )
        #self.mainLabel.setStyleSheet(  )
        vLabelBox.addWidget( self.mainLabel )

        ### Sub Label
        #if self.lines == 2:
        #    self.subLabel = QtWidgets.QLabel( self.sub_title )
        #    self.subLabel.setStyleSheet( " font-size: 7em; color: %s;" % self.sub_color )
        #    vLabelBox.addWidget( self.subLabel )




        self.gradientLabel = QtWidgets.QLabel()
        self.gradientLabel.setMinimumWidth( 50 )
        #self.gradientLabel.setMaximumWidth( 400 )
        mainHBox.addWidget( self.gradientLabel,2)
        #self.set_gradient( self.wash_color )

        # if self.right_title:
        #     self.rightLabel = QtWidgets.QLabel( self.right_title )
        #     self.rightLabel.setAlignment(Qt.AlignRight)
        #     self.rightLabel.setStyleSheet( " font-size: 8em; font-weight: bold; padding: 3px; background-color: %s; color: %s" % (self.sub_color, "white") )
        #     mainHBox.addWidget( self.rightLabel )



        self.lblCBottom = XLabel(height=2)
        self.containerLayout.addWidget(self.lblCBottom)


        ######################
        ##Status==================
        www = 80
        if False:
            self.statusWidget = QtWidgets.QWidget()
            #self.statusWidget.setMinimumWidth(80)
            self.statusWidget.setFixedWidth(www)
            outerLayout.addWidget(self.statusWidget, 0)

            self.statusLayout = QtWidgets.QVBoxLayout()
            self.statusLayout.setContentsMargins(0,0,0,0)
            self.statusLayout.setSpacing(0)
            self.statusWidget.setLayout(self.statusLayout)
                ### Gradient albel

            self.statusBar = QtWidgets.QStatusBar(self)
            #self.statusBar.setFixedHeight(15)
            self.statusBar.setFixedWidth(www)
            self.statusBar.showMessage("")
            self.statusBar.setSizeGripEnabled(False)
            self.statusLayout.addWidget(self.statusBar, 1)

            self.progress = QtWidgets.QProgressBar()
            self.progress.setRange(0, 0)
            self.progress.setFixedHeight(15)
            self.progress.setFixedWidth(www)
            #sp = self.progress.sizePolicy()
            #sp.setHorizontalPolicy(QtWidgets.QSizePolicy.Maximum)
            #self.progress.setSizePolicy(sp)
            self.statusLayout.addWidget(self.progress, 1)
            self.progress.hide()

            #self.statusLayout.addStretch(1)

            self.timerBusy = QtCore.QTimer()
            self.timerBusy.setInterval( 300 )
            #self.timmy = 0
            self.connect( self.timerBusy, QtCore.SIGNAL( 'timeout()' ), self.on_busy_timer )
            self.c = 0
            self.twips = ['. ', ' .']

            self.timerReset = QtCore.QTimer()
            self.timerReset.setSingleShot( True )
            self.connect( self.timerReset, QtCore.SIGNAL( 'timeout()' ), self.on_reset_timer )


        self.set_gradient()

    def on_busy_timer( self ):
        #print " on_busy_timer "
        #self.timmy = self.timmy + self.timerBusy.interval()
        #self.setText( "%s%s %s" % ("Busy ", self.twips[self.c], self.timmy) )
        try:
            self.statusBar.showMessage( "%s%s" % ( "Busy ", self.twips[self.c] ) )
        except RuntimeError as e:
            print("error.busy", e)
        self.c = self.c + 1
        if self.c == 2:
            self.c = 0


    def on_reset_timer( self ):
        #print "one shot reset"
        try:
            self.setStyleSheet( "" )
            self.statusBar.showMessage( "error" )
        except RuntimeError as  e:
            print(e)

    ###################################################################
    def showMessage( self, mess, timeout=None, warn=None ):
        if timeout == None:
            self.statusBar.showMessage( mess )
        else:
            self.statusBar.showMessage( mess, timeout )
        if warn:
            self.statusBar.setStyleSheet("color: #990000;")
        else:
            self.statusBar.setStyleSheet("")

    def set_gradient( self ):
        style_grad = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 %s, stop: 1 %s);" % (self.bg_light, self.bg_dark)
        self.gradientLabel.setStyleSheet( style_grad )

    def get_pixmap( self, ico, wh ):
        #print "PIX", self.img_dir + ico
        pixmap = QtWidgets.QPixmap( self.img_dir + ico )
        return pixmap.scaled( wh, wh, QtCore.Qt.IgnoreAspectRatio )

    def setHeaders( self, txt, txt_small=None ):
        self.mainLabel.setText( txt )
        if txt_small and self.lines == 2:
            self.subLabel.setText( txt_small )

    def setTitle( self, txt ):
        self.mainLabel.setText( txt )


    def setSubTitle( self, txt ):
        self.subLabel.setText( txt )

    def setIcon( self, icon, wid_hei=None, is_staff=None, from_attrib=False ):
        #self.iconWidget.setPixmap( self.get_pixmap( icon, wid_hei if wid_hei else self.width_height ) )
        #print "type=", type(icon)
        if isinstance(icon, QtWidgets.QIcon):
            self.iconWidget.setPixmap( icon.pixmap( QtCore.QSize( 16, 16 )) )
            return
        if from_attrib:
            self.iconWidget.setPixmap( Ico.get(icon, pixmap=True) )
        else:
            self.iconWidget.setPixmap( Ico.icon(icon, pixmap=True) )

class ToolBarGroup(QtWidgets.QWidget):
    def __init__(self, parent=None, title=None, width=None, hide_labels=False, bg='#999999',
                 is_group=False, toggle_icons=False, toggle_callback=None):
        super().__init__()

        if width:
            self.setFixedWidth(width)

        self.icon_on = Ico.filter_on
        self.icon_off = Ico.filter_off
        self.toggle_icons = toggle_icons
        self.toggle_callback = toggle_callback
        self.hide_labels = hide_labels

        self.buttonGroup = None
        self.is_group = is_group
        if self.is_group:
            self.buttonGroup = QtWidgets.QButtonGroup()
            self.buttonGroup.setExclusive(True)
            if self.toggle_callback:
                self.buttonGroup.buttonClicked.connect(self.on_button_clicked)

        self.group_var = None
        self.callback = None
        self.show_icons = True
        self.icon_size = 12
        self.bg_color = bg

        ## Main Layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        ## Label
        self.label = QtWidgets.QLabel()
        #bg = "#8F8F8F"  ##eeeeee"
        fg = "#eeeeee"  ##333333"
        lbl_sty = "background: %s; " % self.bg_color  # qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fefefe, stop: 1 #CECECE);"
        lbl_sty += " color: %s; font-size: 8pt; padding: 1px;" % fg  # border: 1px outset #cccccc;"
        self.label.setStyleSheet(lbl_sty)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFixedHeight(20)
        mainLayout.addWidget(self.label)

        ## Toolbar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbar.setFixedHeight(30)

        mainLayout.addWidget(self.toolbar)

        if title:
            self.set_title(title)
        #print(ere)
    def set_title(self, title):
        self.label.setText("%s" % title)

    def addWidget(self, widget):
        self.toolbar.addWidget(widget)
        return widget

    def addAction(self, act):
        self.toolbar.addAction(act)

    def addButton(self, ico=None, text=None, callback=None, idx=None, toggle_callback=None, tooltip=None,
                  ki=None, bold=False, checkable=False, checked=None, width=None, return_action=False):

        butt = XToolButton()

        if self.is_group:
            if idx != None:
                self.buttonGroup.addButton(butt, idx)
            else:
                self.buttonGroup.addButton(butt)
        if self.hide_labels == False:
            if text != None:
                butt.setText(text)
        if text == None:
            butt.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        else:
            butt.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        if tooltip:
            butt.setToolTip(tooltip)
        if self.toggle_icons:
            butt.setIconSize(QtCore.QSize(10, 10))
            butt.setIcon(Ico.icon(self.icon_off))

        if ico:
            butt.setIcon(Ico.icon(ico))
            butt.setIconSize(QtCore.QSize(10, 10))

        butt.setCheckable(checkable)
        if checked != None:
            butt.setChecked(checked)


        butt.setProperty("ki", ki)
        nuAct = self.toolbar.addWidget(butt)
        if callback:
            butt.clicked.connect(callback)
            #self.connect(butt, QtCore.SIGNAL("clicked()"), callback)
        #if toggle_callback:
        #   self.connect(butt, QtCore.SIGNAL("toggled(bool)"), toggle_callback)
        if bold:
            self.set_bold(butt)
        if width:
            butt.setFixedWidth(width)

        self.on_button_clicked(block=True)

        if return_action:
            return nuAct
        return butt

    def set_bold(self, w):
        f = w.font()
        f.setBold(True)
        w.setFont(f)

    def on_button_clicked(self, butt=None, block=False):
        if self.is_group:
            for b in self.buttonGroup.buttons():
                b.setIcon( Ico.icon(self.icon_on if b.isChecked() else self.icon_off) )

                if block == False and b.isChecked():
                    if self.toggle_callback:
                        self.toggle_callback(self.buttonGroup.id(b))

    def get_id(self):
        id = self.buttonGroup.checkedId()
        if id == -1:
            return None
        return id



class GroupHBox(QtWidgets.QGroupBox):


    def __init__(self, parent=None, spacing=5, margin=10, title=None):
        super().__init__()


        self.xlayout = hlayout(spacing=spacing, margin=margin)
        self.setLayout(self.xlayout)


    def addWidget(self, widget, stretch=0):
        self.xlayout.addWidget(widget, stretch)

    def addLayout(self, widget, stretch=0):
        self.xlayout.addLayout(widget, stretch)

    def addStretch(self, stretch):
        self.xlayout.addStretch(stretch)



class GroupVBox(QtWidgets.QGroupBox):


    def __init__(self, parent=None, bold=False, spacing=5, margin=10, title=None):
        super().__init__()

        self.xlayout = vlayout(spacing=spacing, margin=margin)
        self.setLayout(self.xlayout)

        if title:
            self.setTitle(title)

    def addLabel(self, txt):
        lbl = QtWidgets.QLabel()
        lbl.setText(txt)
        lbl.setStyleSheet("font-family: monospace; font-size: 8pt; color: black;  padding: 1px;")
        self.xlayout.addWidget(lbl)
        return lbl


    def addWidget(self, widget, stretch=0):
        self.xlayout.addWidget(widget, stretch)
        return widget

    def addLayout(self, lay, stretch=0):
        self.xlayout.addLayout(lay, stretch)
        return lay

    def addSpacing(self, s):
        self.xlayout.addSpacing( s)

    def addStretch(self, stretch):
        self.xlayout.addStretch(stretch)


    def setSpacing(self, x):
        self.xlayout.setSpacing(x)


class GroupGridBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None, spacing=5, margin=10, title=None):
        super().__init__(self)


        self.grid = QtWidgets.QGridLayout(spacing=spacing, margin=margin)
        self.setLayout(self.grid)

class XTableWidgetItem( QtWidgets.QTableWidgetItem ):

    def __init__( self ):
        super().__init__( self )

    def set_ico(self, col, ico):
        self.setIcon(col, Ico.icon(ico))

    ##==============================================================
    def set_row_bg(self, color):
        for col_idx in range(0, self.columnCount()):
            self.setBackground(col_idx, QtGui.QColor(color))

    def set_row_fg(self, color):
        for col_idx in range(0, self.columnCount()):
            self.setForeground(col_idx, QtGui.QColor(color))

    def set_bg(self, color):
        self.setBackground(QtGui.QColor(color))

    def set_fg(self, color):
        self.setForeground(QtGui.QColor(color))

class XSpinBox(QtWidgets.QSpinBox):

    def __init__( self , changed=None):
        super().__init__()


        if changed:
            self.valueChanged.connect(changed)