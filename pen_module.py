import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np 
import time
import json
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filename', metavar='N', type=str,
                    help='an integer for the accumulator')

args = parser.parse_args()

# List that saves the tablet data
pen_data = []
begin_time = time.time()


class TabletSampleWindow(QWidget):
    def __init__(self, parent=None):
        super(TabletSampleWindow, self).__init__(parent)
        self.pen_is_down = False
        self.pen_x = 0
        self.pen_y = 0
        self.pen_pressure = 0
        self.text = ""
        # Resizing the sample window to full desktop size:
        frame_rect = app.desktop().frameGeometry()
        width, height = frame_rect.width(), frame_rect.height()
        self.resize(width, height)
        self.move(-9, 0)
        self.setWindowTitle("Sample Tablet Event Handling")

    def tabletEvent(self, tabletEvent):
        self.pen_x = tabletEvent.globalX()
        self.pen_y = tabletEvent.globalY()
        self.pen_pressure = int(tabletEvent.pressure() * 100)
        if tabletEvent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.text = "TabletPress event"
        elif tabletEvent.type() == QTabletEvent.TabletMove:
            self.pen_is_down = True
            self.text = "TabletMove event"
        elif tabletEvent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "TabletRelease event"
        self.text += " at x={0}, y={1}, pressure={2}%,".format(self.pen_x, self.pen_y, self.pen_pressure)
        pen_data.extend([self.pen_x, self.pen_y, self.pen_pressure, time.time()])
        
        # Change the duration of recording of the data, default: 30 secs
        if (time.time()- begin_time>30.0):
            with open('./data/'+ args.filename +'.json', 'w') as f:
                json.dump(json.dumps(pen_data), f)
            exit()
        if self.pen_is_down:
            self.text += " Pen is down."
        else:
            self.text += " Pen is up."
        tabletEvent.accept()
        self.update()

    def paintEvent(self, event):
        text = self.text
        i = text.find("\n\n")
        if i >= 0:
            text = text.left(i)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignLeft , text)

app = QApplication(sys.argv)
mainform = TabletSampleWindow()
mainform.show()
app.exec_()

    
    