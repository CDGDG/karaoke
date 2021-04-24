from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
import requests
from bs4 import BeautifulSoup

main_ui = "./karaoke_main.ui"
popular_ui = "./karaoke_popular.ui"

popular_site = 'https://www.tjmedia.co.kr/tjsong/song_monthPopular.asp'

class Karaoke(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)

        uic.loadUi(main_ui, self)

        self.stackedWidget.setCurrentWidget(self.main_page)

        popular_list = []
        recent_list = []

        po_rq = requests.get(popular_site);po_rq.encoding='utf-8'
        populars = BeautifulSoup(po_rq.text, 'html.parser').select('tbody > tr')
        for popular in populars:
            p = popular.text.strip().split("\n")
            popular_list.append(Song(p[1],p[2],p[3]))
        del popular_list[0]

        for i,song in enumerate(popular_list):
            newButton = QPushButton(text="{:03d} | {:<05d} | {:가<15s} | {:가<7s}".format(i+1,int(song.number),song.title,song.singer));
            newButton.setStyleSheet('border-bottom:2px solid rgb(0,0,0);Text-align: Left');newButton.setFont(QFont('맑은 고딕',20));
            self.popular_frame.layout().addWidget(newButton)


        self.popular_btn.clicked.connect(self.move_popular)
        self.recent_btn.clicked.connect(self.move_recent)
        self.title_btn.clicked.connect(self.move_title)
        self.singer_btn.clicked.connect(self.move_singer)
        self.my_btn.clicked.connect(self.move_my)

    def move_popular(self):
        print('popular')
        self.stackedWidget.setCurrentWidget(self.popular_page)

    def move_recent(self):
        pass

    def move_title(self):
        pass

    def move_singer(self):
        pass

    def move_my(self):
        pass

class Song():
    def __init__(self,number,title,singer,composer='-'):
        self.number = number
        self.title = title
        self.singer = singer
        self.composer = composer

    def __str__(self):
        return "번호:{} | 제목:{} | 가수:{} | 작곡가:{}".format(self.number,self.title,self.singer,self.composer)





if __name__ == '__main__':
    karaoke = QApplication(sys.argv)
    main_window = Karaoke()
    main_window.show()
    sys.exit(karaoke.exec_())