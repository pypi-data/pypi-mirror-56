# -*- coding: utf-8 -*-

import qtawesome as qta

class Ico:
    """Icons Helper


      - All icons used are listed as class constants.
      - This is a base set using `QtAwesome <https://github.com/spyder-ide/qtawesome>`_.
      - Its recommended to override this class as a base set and add custom and overrides etc

      .. code-block:: python

          from pyqtx.xico import Ico as XIco

          class Ico(Xico):

              # Custom attrib
              my_custom = "fa5s.car-crash"

              # Override
              cancel = "fa5s.caret-down"

             # Override main logo

             @staticmethod
             def logo():
                Ico.icon("fa5s.circle-notch")

          widget.setIcon(Ico.icon(Ico.cancel))


    """
    favicon = "fa5s.cat"
    caret_down = "fa5s.angle-down"
    help = "fa5s.question-circle"
    node = "fa5s.angle-right"

    commander = "fa5s.solar-panel"
    terminal = "fa5s.desktop"
    return_key = "ei.return-key"
    connect = "fa5s.sign-in-alt"

    add = "fa5s.plus"
    edit = "fa5.edit"
    delete = "fa5.trash-alt"

    cancel = "ei.remove"
    save = "ei.ok-circle"

    settings = "fa5s.cog"
    refresh = "ei.refresh"
    login = "ei.lock"

    start = "fa5s.play"
    stop = "fa5s.stop"

    up = "ei.arrow-up"
    down = "ei.arrow-down"

    quit = "ei.eject"
    clear = "ei.remove-circle"

    filter_on = "fa5s.server"
    filter_off = "fa5s.server"

    server = "fa5s.server"
    servers = "ei.th-list"

    db = "fa5s.database"
    db_tables = "ei.th-list"
    db_table = "fa5s.table"

    @staticmethod
    def i(name):
        """Shortcut to :meth:`Ico.icon` """
        return Ico.icon(name)

    @staticmethod
    def icon( name ):
        """Creates a QIcon

        :param name: font icon to load
        :type name: str
        :return: QIcon
        :rtype: QIcon
        """

        return qta.icon(name)

    @staticmethod
    def logo():
        """Override this to custom logo"""
        return Ico.icon(Ico.favicon)

