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
        p.setPen(QColor(p_P))
        p.setRenderHint(QPainter.Antialiasing)
        b = QBrush()
        b.setColor(QColor(p_P))
        p.setBrush(b)
        p.drawRoundedRect(0, 2, 38, 18, 8, 8)
        if self.on:
            bkgd = QColor(accent)
        else:
            bkgd = QColor(p_A)
        c = QPainterPath()
        c.moveTo(0, 0)
        c.addRoundedRect(self.bx, 0, 22, 22, 11, 11)
        p.fillPath(path, bkgd)
        p.fillPath(c, QColor(p_B))
        p.drawRoundedRect(self.bx, 0, 22, 22, 11, 11)

    def setFlicked(self, e):
        self.onFlick = e

    def flick(self, s=True):
        self.on = not self.on
        if self.on:
            xs = [8, 11, 15, 18]
        else:
            xs = [15, 11, 8, 0]
        for n in xs:
            self.bx = n
            self.repaint()
            time.sleep(0.025)
        self.onFlick(self.on)

    def mousePressEvent(self, e):
        self.flick()

accent = "#0075db"
sidebarShown = True
sidebarExplicitlyShown = False
sidebarExplicitlyHidden = False
animating = False
appName = os.path.basename(os.path.dirname(__file__))

#    light theme, dark theme
c_B = ["#ffffff", "#282828"]
c_S = ["#eedddddd", "#ee373737"]
c_F = ["#000000", "#ffffff"]
c_A = ["#bbbbbb", "#323232"]
c_P = ["#999999", "#424242"]
c_C = ["#000000", "#ffffff"]

a = sys.argv[0]
if not a.startswith("/"):
    a = os.path.abspath(a)

bundle = os.path.basename(a).replace(".py", "")
while len(a) > 5:
    a = os.path.dirname(a)
    if a.endswith(".app"):
        bundle = a
        break

uiSettings = Settings("com.arbyon.ui")
localSettings = Settings("app."+bundle)

if uiSettings.get("accent") is None:
    uiSettings.set("accent", accent)
else:
    accent = uiSettings.get("accent")

if uiSettings.get("dark") is None:
    uiSettings.set("dark", True)
    dark = True
else:
    dark = uiSettings.get("dark")

if uiSettings.get("accentDark") is None:
    accentDark = True
else:
    accentDark = uiSettings.get("accentDark")

lscache = [accent, dark, accentDark]

p_B = c_B[int(dark)]
p_S = c_S[int(dark)]
p_F = c_F[int(dark)]
p_A = c_A[int(dark)]
p_P = c_P[int(dark)]
p_C = c_C[int(accentDark)]

def pss(s):
    return s.replace("ACCENT", accent).replace(":A", p_A).replace(":B", p_B
    ).replace(":S", p_S).replace(":F", p_F).replace(":P", p_P).replace(":C",
    p_C)

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

qss_Main = pss(_qss_Main)
