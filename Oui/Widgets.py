import os
import sys
import time

sys.path.append("/usr/share/omega")

from PySide2.QtCore import QTimer, Qt, QSize
from PySide2.QtGui import (QGuiApplication, QIcon, QCursor,
        QBrush, QPixmap, QPainter, QGuiApplication, QFont, QBrush,
                                                QColor, QPainterPath)
from PySide2.QtWidgets import (QApplication, QWidget, QFrame, QSizeGrip,
            QPushButton, QVBoxLayout, QLabel, QStackedWidget, QScrollArea)

from OPlatform.SettingsAPI import Settings

# import widgets that I've split off
from . import OuiSettings as settings
from .Buttons import *
#from Display import *
#from Input import *
#from Misc import *

class ODraggableWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.pressedDown = False
        self.xo = 0
        self.yo = 0

    def mousePressEvent(self, me):
        if self.pressedDown or me.button() ^ me.buttons():
            QWidget.mousePressEvent(self, me)
            return
        if me.button() == Qt.LeftButton:
            self.pressedDown = True
            self.xo = me.globalX() - self.parentWidget().x()
            self.yo = me.globalY() - self.parentWidget().y()
            me.accept()
            return
        QWidget.mousePressEvent(self, me)
        QGuiApplication.setOverrideCursor(QCursor(Qt.ClosedHandCursor))
        QGuiApplication.changeOverrideCursor(QCursor(Qt.ClosedHandCursor))
        pass

    def mouseReleaseEvent(self, me):
        if not self.pressedDown:
            QWidget.mouseReleaseEvent(self, me)
            return
        self.pressedDown = False
        QGuiApplication.restoreOverrideCursor()
        me.accept()

    def mouseMoveEvent(self, me):
        self.parentWidget().move(me.globalX() - self.xo,
                                 me.globalY() - self.yo)
        me.accept()

accent = settings.accent
sidebarShown = True
sidebarExplicitlyShown = False
sidebarExplicitlyHidden = False
animating = False
appName = os.path.basename(os.path.dirname(__file__))

a = sys.argv[0]
if not a.startswith("/"):
    a = os.path.abspath(a)

bundle = os.path.basename(a).replace(".py", "")
while len(a) > 5:
    a = os.path.dirname(a)
    if a.endswith(".app"):
        bundle = a
        break

localSettings = Settings("app."+bundle)

_qss_Main = """
QScrollBar {
    border: 0px solid transparent;
    background: transparent;
}

QScrollBar::handle {
    border: 1px solid #0f000000;
    background: :P;
    border-radius: 5px;
}

QScrollBar:horizontal {
    height: 10px;
}

QScrollBar:vertical {
    width: 10px;
}

QScrollBar::add-line, QScrollBar::sub-line,
QScrollBar:left-arrow, QScrollBar::right-arrow,
QScrollBar::add-page, QScrollBar::sub-page,
QScrollBar:up-arrow, QScrollBar::down-arrow {
    border: 0px solid transparent;
    background: transparent;
    height: 0px;
    width: 0px;
}

QScrollArea {
    background: transparent;
    border: 0px solid transparent;
}

QScrollArea > QWidget {
    background: transparent;
    border: 0px solid transparent;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
    border: 0px solid transparent;
}
"""

qss_Main = settings.pss(_qss_Main)
