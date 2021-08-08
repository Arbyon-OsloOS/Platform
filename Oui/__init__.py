import os
import sys
import time

import Widgets as Widgets

sys.path.append("/usr/share/omega")

from PySide2.QtCore import QTimer, Qt, QSize
from PySide2.QtGui import (QGuiApplication, QIcon, QCursor,
        QBrush, QPixmap, QPainter, QGuiApplication, QFont, QBrush,
                                                QColor, QPainterPath)
from PySide2.QtWidgets import (QApplication, QWidget, QFrame, QSizeGrip,
            QPushButton, QVBoxLayout, QLabel, QStackedWidget, QScrollArea)

from OPlatform.SettingsAPI import Settings

bundle = Widgets.bundle

app = QApplication([])
app.setApplicationName(bundle)
app.setStyleSheet(Widgets.qss_Main)

def run():
    return app.exec_()
