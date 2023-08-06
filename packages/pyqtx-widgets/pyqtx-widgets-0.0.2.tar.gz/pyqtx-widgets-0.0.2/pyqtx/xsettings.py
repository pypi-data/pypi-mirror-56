# -*- coding: utf-8 -*-

import urllib
from Qt import Qt, QtCore


class Srv(object):

    def __init__(self, name=None, ki=None, url=None):
        self.name = name
        self.ki = ki
        self.url = url

    def __repr__(self):
        return "<Src url=%s>"

    @property
    def host(self):
        return urllib.parse.urlparse(self.url).netloc

class XSettings( QtCore.QSettings ):

    CURR_SERVER_KI = "current/server_ki"

    def __init__( self, parent=None ):
        QtCore.QSettings.__init__( self, parent )

        #self.qsettings = QtCore.QSettings()
        self.server_auth = False


    def current_server( self ):
        return self.qsettings.value( "server.server" )

    @property
    def cache_enabled(self):
        #return False
        return bool(self.qsettings.value("cache-enabled", True))

    def set_cache_enabled(self, state):
        self.qsettings.setValue("cache-enabled", state)
        self.qsettings.sync()


    ##==============================
    ## Window Save/Restore
    def save_window( self, window ):
        name = window.objectName()
        if len(name) == 0:
            return
        self.qsettings.setValue( "window/%s/geometry" % name, QtCore.QVariant( window.saveGeometry() ) )

    def restore_window( self, window ):
        name = str(window.objectName())
        if len(name) == 0:
            return
        window.restoreGeometry( self.qsettings.value( "window/%s/geometry" % name ) )


    def save_splitter(self, splitter):
        wname = str(splitter.objectName())
        if not wname:
            print ("Splitter has no name", splitter)
        self.qsettings.setValue("splitter/%s" % wname, splitter.saveState())

    def restore_splitter(self, splitter):
        wname = str(splitter.objectName())
        if not wname :
            print ("Splitter has no name")
            return
        v = self.qsettings.value("splitter/%s" % wname)
        if v:
            splitter.restoreState(v)



