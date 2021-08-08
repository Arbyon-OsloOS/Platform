import time

from PySide2.QtCore import QTimer, Qt, QSize, Signal
from PySide2.QtGui import (QIcon, QCursor, QPixmap, QPainter,
                           QFont, QBrush, QColor, QPainterPath)
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget

from . import OuiSettings

class OButton(QWidget):
    def __init__(self, text=None, icon=None, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.text = text
        self.icon = icon
        self.setMinimumSize(40, 40)
        if self.text is None:
            self.tool = True
        else:
            self.setMinimumSize(216, 40)
            self.tool = False
        self.pushed = False

    def paintEvent(self, e):
        path = QPainterPath()
        path.moveTo(0, 0)
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if self.pushed:
            bkgd = QColor(OuiSettings.p_P)
        else:
            bkgd = QColor(OuiSettings.p_A)
        p.fillPath(path, bkgd)

    def mousePressEvent(self, me):
        self.pushed = True
        self.repaint()

    def mouseReleaseEvent(self, me):
        self.pushed = False
        self.repaint()
        self.clicked.emit()

    clicked = Signal()

class OSwitch(QWidget):
    def __init__(self, on=False, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setMinimumSize(40, 24)
        self.on = on
        self.onFlick = lambda e: None
        self.bx = 18 if on else 0

    def paintEvent(self, e):
        path = QPainterPath()
        path.moveTo(0, 2)
        path.arcTo(0, 2, 14, 18, 90, 180)
        path.arcTo(24, 2, 14, 18, 270, 180)
        p = QPainter(self)
        p.setPen(QColor(OuiSettings.p_P))
        p.setRenderHint(QPainter.Antialiasing)
        b = QBrush()
        b.setColor(QColor(OuiSettings.p_P))
        p.setBrush(b)
        p.drawRoundedRect(0, 2, 38, 18, 8, 8)
        if self.on:
            bkgd = QColor(OuiSettings.accent)
        else:
            bkgd = QColor(OuiSettings.p_A)
        c = QPainterPath()
        c.moveTo(0, 0)
        c.addRoundedRect(self.bx, 0, 22, 22, 11, 11)
        p.fillPath(path, bkgd)
        p.fillPath(c, QColor(OuiSettings.p_B))
        p.drawRoundedRect(self.bx, 0, 22, 22, 11, 11)

    flicked = Signal(bool)

    def flick(self, value=None):
        oldon = self.on
        if value is None:
            self.on = not self.on
        else:
            self.on = value
        if self.on:
            xs = [8, 11, 15, 18]
        else:
            xs = [15, 11, 8, 0]
        for n in xs:
            self.bx = n
            if self.on != oldon:
                self.repaint()
                time.sleep(0.025)
        if self.on != oldon:
            self.flicked.emit(self.on)

    def mousePressEvent(self, e):
        self.flick()
