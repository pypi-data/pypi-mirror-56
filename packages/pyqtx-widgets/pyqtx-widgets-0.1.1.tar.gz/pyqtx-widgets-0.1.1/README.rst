pyqtx_widgets
=======================

This lib is in active use and makes knocking up PyQt5 apps a little quicker.

It's just a bunch of constructors and Xtended widgets to add some functionality.
Now some of you may scream about adding another layer!!
Instead is viewed as  DRY, as same stuff gets copied across projects


.. code-block:: python

    ## Layout
    lay = QtWidgets.QVBoxLayout()
    lay.setContentMargins(10,10,10,10)
    lay.setSpacing(20)

    # vs
    lay = xwidgets.vlayout(margin=10. spacing=20)

    ## Toolbutton
    butt = QtWidgets.QToolButton()
    butt.setAutoRaise(True)
    butt.setText("Foo")
    butt.clicked.connect(self.on_button)

    # vs
    butt = xwidgets.XToolButton(text="Foo", autoRaise=True, clicked=self.on_button)



