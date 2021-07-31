#!/usr/bin/env python3

import os
import sys
import ouiread

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QFrame, QProgressBar

ouiread.appName = "Backups"

l1 = QVBoxLayout()
l1.setAlignment(Qt.AlignTop | Qt.AlignLeft)
l1.addWidget(lab := QLabel("What would you like to name the backup?"))
l1.addWidget(fil := QLineEdit())

l1.addWidget(w1 := QWidget())
w1.setLayout(h1 := QHBoxLayout())
l1.addSpacing(5)
l1.addWidget(QPushButton("Start Backup"))
l1.addSpacing(10)
l1.addWidget(pb := QProgressBar())
h1.addWidget(QLabel("Include Applications folder"))
h1.addWidget(ouiread.Switch())
fil.setText("backup-2021-07-23")
lab.setWordWrap(True)
l2 = QVBoxLayout()
l2.setAlignment(Qt.AlignTop | Qt.AlignLeft)
l2.addWidget(QLabel("nothing's in here..."))
pb.setMinimum(0)
pb.setMaximum(100)
pb.setValue(0)
p1 = ouiread.Page(l1, name="Create a Backup")
p2 = ouiread.Page(l2, name="Restore a Backup")
w = ouiread.BasicWindow()
w.show()
w.loadPages([p1, p2])
sys.exit(ouiread.run())
