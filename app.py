import json

from PyQt5 import QtWidgets, QtGui
from ui_radio import Ui_MainWindow
from vlc import MediaPlayer, Media
from threading import Thread
import time

p = MediaPlayer()

class Radio(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.stream_id = 0
        self.is_playing = False
        self.play_icon = QtGui.QIcon()
        with open('stream_list.json', 'r') as openfile:
            self.streams = json.load(openfile)
        self.media = Media(self.streams[self.stream_id].get('url'))
        self.ui.play_pause.clicked.connect(lambda: self.play(False))
        self.ui.next.clicked.connect(self.next)
        self.ui.back.clicked.connect(self.previous)

    def next(self):
        if self.stream_id + 1 >= len(self.streams):
            self.stream_id = 0
        else:
            self.stream_id += 1
        self.play(True)

    def previous(self):
        if self.stream_id < 1:
            self.stream_id = len(self.streams) - 1
        else:
            self.stream_id -= 1
        self.play(True)

    def play(self, skip):
        if skip is False:
            self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_icon.addPixmap(QtGui.QPixmap("icons/pause_24dp_FFB000_FILL1_wght400_GRAD0_opsz24.png"),
                                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.media = Media(self.streams[self.stream_id].get('url'))
            p.set_media(self.media)
            p.play()
        else:
            self.play_icon.addPixmap(QtGui.QPixmap("icons/play_arrow_24dp_FFB000_FILL1_wght400_GRAD0_opsz24.png"),
                                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            p.stop()
        self.ui.play_pause.setIcon(self.play_icon)

    def get_media(self):
        return self.media

def thread():
    while True:
        time.sleep(1)
        media = window.get_media()
        meta = media.get_meta(12)
        if meta is None:
            meta = '-'
        window.ui.name_station.setText(f'{window.stream_id + 1}. {window.streams[window.stream_id].get("name")}')
        window.ui.track_name.setText(meta)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Radio()
    window.show()
    thread = Thread(target=thread)
    thread.daemon = True
    thread.start()
    app.exec_()