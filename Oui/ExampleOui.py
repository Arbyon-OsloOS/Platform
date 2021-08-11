#!/usr/bin/env python3

import os
import sys

sys.path.append("/usr/share/omega")

import OPlatform.Oui.ouiread as ouiread

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit

l1 = QVBoxLayout()
l1.setAlignment(Qt.AlignTop | Qt.AlignLeft)
l1.addWidget(lab := QLabel("Which file would you like me to open?"))
l1.addWidget(fil := QLineEdit())
fil.setText(os.getenv("HOME") + "/Documents/")
lab.setWordWrap(True)
l2 = QVBoxLayout()
l2.setAlignment(Qt.AlignTop | Qt.AlignLeft)
_h = QWidget()
l2.addWidget(_h)
h = QHBoxLayout()
_h.setLayout(h)
h.addWidget(y := QPushButton("Yes"))
h.addWidget(n := QPushButton("No"))
def yes():
    l2.addWidget(QLabel("Ding! Yep, that's right!"))
def no():
    l2.addWidget(QLabel("you need to fix that..."))
y.clicked.connect(lambda: yes())
n.clicked.connect(lambda: no())
p1 = ouiread.Page(l1, name="The first page")
p2 = ouiread.Page(l2, name="And the second")
w = ouiread.BasicWindow()
w.show()
w.loadPages([p1, p2])
sys.exit(ouiread.app.exec_())
