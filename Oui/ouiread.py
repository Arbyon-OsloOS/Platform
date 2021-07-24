#!/usr/bin/env python3

import os
import sys
import time

sys.path.append("/usr/share/omega")

from PySide2.QtCore import QTimer, Qt, QSize
from PySide2.QtGui import (QGuiApplication, QIcon, QCursor,
              QBrush, QPixmap, QPainter, QGuiApplication, QFont)
from PySide2.QtWidgets import (QApplication, QWidget, QFrame, QSizeGrip,
            QPushButton, QVBoxLayout, QLabel, QStackedWidget, QScrollArea)

from OPlatform.SettingsAPI import Settings


class DraggableWidget(QWidget):
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


class Page():
    def __init__(self, layout, name="Page", icon=""):
        self.name = name
        self.layout = layout
        self.icon = icon


class MetalWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
    
    def paintEvent(self, ev):
        p = QPainter(self)
        p.setBrush(QBrush(QPixmap("./metal.png")))
        p.drawRect(0, 0, self.width(), self.height());
        ev.accept()


class Switch(QFrame):
    def __init__(self, on=False, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self.on = not on
        self.setFixedSize(64, 32)
        self.circle = QFrame(parent=self)
        if self.on:
            self.circle.move(0, 0)
        else:
            self.circle.move(32, 0)
        self.circle.resize(32, 32)
        self.circle.setStyleSheet(pss("""\
background-color: :B;
border-radius: 16px;
border: 1px solid :P;
"""))
        self.flicked = lambda on: None
        self.flick()
        self.uit = QTimer()
        self.uit.setInterval(2500)
        self.uit.timeout.connect(self.uir)
        self.uit.start()
        self.setFocusPolicy(Qt.StrongFocus)
    
    def uir(self):
        self.circle.setStyleSheet(pss("""\
background-color: :B;
border-radius: 16px;
border: 1px solid :P;
"""))
        self.flick(False) # Flick twice without animation, shows nothing but it
        self.flick(False) # means we refresh our stylesheet. TODO: not that.
    
    def setFlicked(self, e):
        self.flicked = e
    
    def flick(self, s=True):
        self.on = not self.on
        self.flicked(self.on)
        if self.on:
            self.setStyleSheet(pss("""\
QWidget {
    background-color: ACCENT;
    height: 32px;
    width: 64px;
    border-radius: 16px;
    border: 1px solid :P;
}

QWidget:focus {
    border: 1px solid ACCENT;
}
"""))
            if s:
                self.circle.move(8, 0)
                self.repaint()
                time.sleep(0.025)
                self.circle.move(16, 0)
                self.repaint()
                time.sleep(0.025)
                self.circle.move(24, 0)
                self.repaint()
                time.sleep(0.025)
            self.circle.move(32, 0)
        else:
            self.setStyleSheet(pss("""\
QWidget {
    background-color: :A;
    height: 32px;
    width: 64px;
    border-radius: 16px;
    border: 1px solid :P;
}

QWidget:focus {
    border: 1px solid ACCENT;
}
"""))
            if s:
                self.circle.move(24, 0)
                self.repaint()
                time.sleep(0.025)
                self.circle.move(16, 0)
                self.repaint()
                time.sleep(0.025)
                self.circle.move(8, 0)
                self.repaint()
                time.sleep(0.025)
            self.circle.move(0, 0)
    def mousePressEvent(self, e):
        self.flick()


class BasicWindow(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setMinimumSize(400, 400)
        self.pages = []
        self.selectedPage = 0
        self.redrawTimer = QTimer()
        self.redrawTimer.setInterval(16)
        self.redrawTimer.timeout.connect(self.drawme)
        self.redrawTimer.start()
        self.ts = QTimer()
        self.ts.setInterval(5000)
        self.ts.timeout.connect(self.sref)
        self.ts.start()
        self.setWindowFilePath("what does this do?")
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.sidebar = QFrame(parent=self)
        self.sidebar.resize(300, self.height())
        self.ma = QFrame(parent=self)
        self.ma.setGeometry(300, 0, self.width() - 300, self.height())
        tf = QFont("Inter")
        tf.setWeight(QFont.DemiBold)
        tf.setPixelSize(34)
        self.pageTitle = QLabel("Page 1", parent=self.ma)
        self.appTitle = QLabel(appName, parent=self.sidebar)
        self.appTitle.setFont(tf)
        self.appTitle.move(42, 45)
        self.appTitle.resize(210, 44)
        self.pageTitle.setFont(tf)
        self.pageTitle.move(42, 45)
        self.pageTitle.resize(self.ma.width() - 60, 44)
        
        # Here we need to implement the pages.
        
        self.pagesWidget = QWidget(parent=self.sidebar)
        self.pagesWidget.setGeometry(42, 128, 216, self.sidebar.height() - 170)
        self.pager = QVBoxLayout()
        self.pagesWidget.setLayout(self.pager)
        self.pager.setAlignment(Qt.AlignTop)
        self.pager.setContentsMargins(0, 0, 0, 0)
        
        self.pageWidget = QStackedWidget(parent=self.ma)
        self.pageWidget.setGeometry(42, 128, self.ma.width() - 84, self.ma.height() - 170)
        self.page1 = QVBoxLayout()
        self.sizey = QSizeGrip(self)
        self.sizey.setGeometry(self.width() - 20, self.height() - 20, 20, 20)
        self.sizey.setStyleSheet("image: transparent")
        self.titleDrag = DraggableWidget(parent=self)
        self.titleDrag.setGeometry(0, 0, self.width()+300, 128)
        self.resize(800, 600)
        self.closeBtn = QPushButton(parent=self)
        self.closeBtn.setGeometry(self.width() - 67, 42, 42, 42)
        self.closeBtn.clicked.connect(self.close)
        self.sidebar.setStyleSheet(qss_s)
        self.ma.setStyleSheet(qss_m)
        self.appTitle.setStyleSheet(pss("color: :F"))
        self.pageTitle.setStyleSheet(pss("color: :F"))
        self.closeBtn.setStyleSheet(qss_RoundButton)
        self.closeBtn.setIcon(QIcon("/usr/share/icons/Papirus%s/16x16/actions/window-close.svg" % ("-Dark" if dark else "")))
        self.closeBtn.setIconSize(QSize(16, 16))
        self.closeBtn.setFocusPolicy(Qt.NoFocus)
        self.pgBtns = []
    
    def loadPages(self, pages, destroy=True):
        if self.selectedPage < len(self.pages):
            title = self.pages[self.selectedPage].name
        else:
            title = 0 # Can't equal any string
        if destroy:
            for page in self.pages:
                try:
                    page.layout.destroy()
                finally:
                    del page
        index = -1
        for page in pages:
            index += 1
            sel = False
            if page.name == title:
                self.selectedPage = index
            if self.selectedPage == index:
                sel = True
            self.pages.append(page)
            def e():
                _w = QWidget()
                _w.setLayout(page.layout)
                _s = QScrollArea()
                _s.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                _s.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                _s.setFocusPolicy(Qt.ClickFocus)
                _s.setWidget(_w)
                _s.setWidgetResizable(True)
                self.pageWidget.addWidget(_s)
                b = QPushButton(page.name)
                if sel:
                    b.setStyleSheet(qss_Selected)
                    self.pageWidget.widget(index).show()
                    self.page1 = page.layout
                self.pager.addWidget(b)
                self.pgBtns.append(b)
                i = index
                b.clicked.connect(lambda: self.showPage(i))
                if sel:
                    n = page.name
                    self.setWindowTitle(n)
                    self.pageTitle.setText(n)
            e()
    
    def showPage(self, index):
        self.selectedPage = index
        self.page1 = self.pages[index].layout
        ind = 0
        while self.pageWidget.widget(ind):
            self.pageWidget.widget(ind).hide()
            ind += 1
        self.pageWidget.widget(index).show()
        n = self.pages[index].name
        self.setWindowTitle(n)
        self.pageTitle.setText(n)
        i = -1
        for w in self.pgBtns:
            i += 1
            if i == index:
                w.setStyleSheet(qss_Selected)
            else:
                w.setStyleSheet(qss_Main)
    
    def drawme(self):
        try:
            self.sizey.setGeometry(self.width() - 20, self.height() - 20, 20, 20)
            self.ma.resize(self.width() - 300, self.height())
            self.sidebar.resize(300, self.height())
            self.closeBtn.setGeometry(self.width() - 67, 42, 42, 42)
            self.pageWidget.resize(self.ma.width() - 84, self.ma.height() - 170)
            self.titleDrag.resize(self.width()+300, 128)
            self.pageTitle.resize(self.ma.width() - 60, 44)
            pass # put something useful here, I'll do that later :~)
        except KeyboardInterrupt:
            sys.exit(1)
    
    def sref(self):
        global accent, dark, accentDark, p_B, p_S, p_F, p_A, p_P, p_C
        global qss_m, qss_s, qss_RoundButton, qss_Main, qss_Selected
        global lscache

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

        if lscache == [accent, dark, accentDark]:
            return
        
        lscache = [accent, dark, accentDark]
        
        p_B = c_B[int(dark)]
        p_S = c_S[int(dark)]
        p_F = c_F[int(dark)]
        p_A = c_A[int(dark)]
        p_P = c_P[int(dark)]
        p_C = c_C[int(accentDark)]

        qss_m = pss(_qss_m)
        qss_s = pss(_qss_s)
        qss_RoundButton = pss(_qss_RoundButton)
        qss_Main = pss(_qss_Main)
        qss_Selected = pss(_qss_Selected)
        app.setStyleSheet(qss_Main)
        self.sidebar.setStyleSheet(qss_s)
        self.ma.setStyleSheet(qss_m)
        self.appTitle.setStyleSheet(pss("color: :F"))
        self.pageTitle.setStyleSheet(pss("color: :F"))
        self.closeBtn.setStyleSheet(qss_RoundButton)
        self.closeBtn.setIcon(QIcon("/usr/share/icons/Papirus%s/16x16/actions/window-close.svg" % ("-Dark" if dark else "")))
        
        index = self.selectedPage
        i = -1
        for w in self.pgBtns:
            i += 1
            if i == index:
                w.setStyleSheet(qss_Selected)
            else:
                w.setStyleSheet(qss_Main)


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

bundle = os.path.basename(__file__).replace(".py", "")
a = __file__
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

_qss_m = "\
BasicWindow > QFrame { \
background-color: :B; \
border-bottom-right-radius: 20px; \
border-top-right-radius: 20px; \
border-right: 1px solid #0f000000; \
border-top: 1px solid #0f000000; \
border-bottom: 1px solid #0f000000 \
}"

_qss_s = "\
BasicWindow > QFrame { \
background-color: :S; \
border-bottom-left-radius: 20px; \
border-top-left-radius: 20px; \
border-left: 1px solid #0f000000; \
border-top: 1px solid #0f000000; \
border-bottom: 1px solid #0f000000 \
}"

_qss_RoundButton = """\
QPushButton {
    background-color: :A;
    border-radius: 21px;
    border: 1px solid #0f000000;
    color: :F;
}

QPushButton:pressed {
    background-color: :P;
}
"""

_qss_Main = """\
QPushButton {
    background-color: :A;
    border-radius: 10px;
    border: 1px solid #0f000000;
    color: :F;
    height: 40px;
    selection-background-color: transparent;
    width: 100px;
}

QPushButton:pressed {
    background-color: :P;
}

QWidget:focus {
    border-color: ACCENT;
    border-width: 2px;
}

QLabel {
    color: :F
}

QWidget {
    selection-background-color: ACCENT;
}

QScrollArea {
    border: 0px solid transparent;
}

QScrollArea > QWidget {
    border: 0px solid transparent;
}

QScrollArea > QWidget > QWidget {
    background: :B;
    border: 0px solid transparent;
}

QLineEdit {
    background: :A;
    height: 40px;
    border: 1px solid #0f000000;
    border-radius: 10px;
    color: :F;
}

QProgressBar {
    border: 1px solid :P;
    border-radius: 1px;
    height: 20px;
    text-align: center;
/*    color: transparent;*/
}

QProgressBar::chunk {
    background-color: ACCENT;
    border-radius: 0px;
    width: 20px;
}
"""

_qss_Selected = """\
QWidget {
    background-color: ACCENT;/*
    height: 40px;
    border-radius: 10px;
    border: 1px solid #0f000000;*/
    color: :C;
}

QPushButton:pressed {
    background-color: :P;
    color: :F;
}

QWidget:focus {
    border-color: ACCENT;
    border-width: 2px;
}
"""
qss_m = pss(_qss_m)
qss_s = pss(_qss_s)
qss_RoundButton = pss(_qss_RoundButton)
qss_Main = pss(_qss_Main)
qss_Selected = pss(_qss_Selected)

app = QApplication([])
app.setApplicationName(bundle)
app.setStyleSheet(qss_Main)

def run():
    return app.exec_()

if __name__ == "__main__":
    widget = BasicWindow()
    widget.show()
    sys.exit(app.exec_())
