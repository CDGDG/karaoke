from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

main_ui = "karaoke_main.ui"
popular_ui = "./karaoke_popular.ui"

popular_site = 'https://www.tjmedia.co.kr/tjsong/song_monthPopular.asp'
recent_site = 'http://www.tjmedia.co.kr/tjsong/song_monthNew.asp'
search_site = 'https://www.tjmedia.co.kr/tjsong/song_search_list.asp?strType={}&strText={}&strCond=1&strSize02=100&intPage={}'

DEVELOPER_KEY = "AIzaSyCxCQR3XfJdM13CzN3IIEQOuiSPq6ocoRg"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"
youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

class Karaoke(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)

        uic.loadUi(main_ui, self)

        self.stackedWidget.setCurrentWidget(self.main_page)

        self.popular_list = []
        self.recent_list = []
        self.title_list = []

        self.make_popular()
        self.make_recent()

        self.popular_btn.clicked.connect(self.move_popular)
        self.recent_btn.clicked.connect(self.move_recent)
        self.title_btn.clicked.connect(self.move_title)
        self.singer_btn.clicked.connect(lambda : self.move_singer())
        self.my_btn.clicked.connect(self.move_my)

        self.return_btn.clicked.connect(self.return_main)
        self.return_btn_2.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.main_page))
        self.return_btn_3.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.main_page))
        self.return_btn_4.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.main_page))
        self.return_btn_5.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.main_page))

        self.title_edit.returnPressed.connect(lambda : self.make_search(1,self.title_edit.text(),self.title_frame))
        self.singer_edit.returnPressed.connect(lambda : self.make_search(2,self.singer_edit.text(),self.singer_frame))


    def make_popular(self):
        po_rq = requests.get(popular_site);
        po_rq.encoding = 'utf-8'
        populars = BeautifulSoup(po_rq.text, 'html.parser').select('tbody > tr')
        for popular in populars:
            p = popular.text.strip().split("\n")
            self.popular_list.append(Song(p[1], p[2], p[3]))
        del self.popular_list[0]

        for i, song in enumerate(self.popular_list):
            self.popular_frame.layout().addWidget(self.make_frame(i+1,song))

    def make_recent(self):
        re_rq = requests.get(recent_site)
        re_rq.encoding = 'utf-8'
        recents = BeautifulSoup(re_rq.text,'html.parser').select('tbody > tr')
        for recent in recents:
            r = recent.text.strip().split("\n")
            self.recent_list.append(Song(r[0],r[1],r[2]))
        del self.recent_list[0]

        for i, song in enumerate(self.recent_list):
            self.recent_frame.layout().addWidget(self.make_frame(song.number, song))

    def make_search(self,type1,text,frame):
        for c in frame.children():
            if str(type(c)) == "<class 'PyQt5.QtWidgets.QFrame'>":
                c.close()

        i=1
        flag = False
        while True:
            target = search_site.format(type1,text,i)
            rq = requests.get(target)
            rq.encoding = 'utf-8'
            results = BeautifulSoup(rq.text,'html.parser').select('tbody > tr')
            if len(results)==0:
                break;
            for result in results:
                r = result.text.strip().split("\n")
                if r[0]=="??? ?????? ":
                    continue
                elif "??????????????? ????????? ????????????.".__eq__(r[0]):
                    flag = True
                    break;
                elif len(r) > 2:
                    song = Song(r[0],r[1],r[2])
                    frame.layout().addWidget(self.make_frame(song.number, song))
            if flag:
                break;
            i+=1



    def move_popular(self):
        print('popular')
        self.stackedWidget.setCurrentWidget(self.popular_page)

    def move_recent(self):
        print('recent')
        self.stackedWidget.setCurrentWidget(self.recent_page)

    def move_title(self):
        print('title')
        self.make_search(1, "", self.title_frame)
        self.stackedWidget.setCurrentWidget(self.title_page)

    def move_singer(self,singer=""):
        print('singer')
        self.make_search(2, singer, self.singer_frame)
        if singer!="":
            self.singer_edit.setText(singer)
        self.stackedWidget.setCurrentWidget(self.singer_page)

    def return_main(self):
        self.youtube_view.setUrl(QUrl('none'))
        self.stackedWidget.setCurrentWidget(self.main_page)

    def move_my(self):
        pass

    def make_frame(self,number,song):
        newFrame = QFrame();newFrame.setStyleSheet('QFrame{background-color:none;border: 2px solid rgb(255,255,255);}')
        newLayout = QHBoxLayout(newFrame);newLayout.setContentsMargins(0,0,0,0);newLayout.setSpacing(0)
        numberLabel = QLabel();numberLabel.setStyleSheet('background-color:none;border:none;')
        numberLabel.setText(str(number));numberLabel.setFont(QFont('210 ???????????? 040',20))
        songButton = QPushButton();
        songButton.setText(song.title if len(song.title) < 30 else song.title[:30]);songButton.setFont(QFont('210 ???????????? 040',15));songButton.clicked.connect(lambda :song.play(self.stackedWidget,self.play_page,self.youtube_view))
        songButton.setStyleSheet('background-color:none;border:none;')
        singerButton = QPushButton()
        singerButton.setText(song.singer if len(song.singer) < 16 else song.singer[:16]);singerButton.setFont(QFont('210 ???????????? 040',15))
        singerButton.setStyleSheet('background-color:none;border:none;')
        singerButton.clicked.connect(lambda: self.move_singer(song.singer))
        newLayout.addWidget(numberLabel,2,Qt.AlignCenter)
        newLayout.addWidget(songButton,10)
        newLayout.addWidget(singerButton,5)
        return newFrame

class Song():
    def __init__(self,number,title,singer):
        self.number = number
        self.title = title
        self.singer = singer

    def __str__(self):
        return "??????:{} | ??????:{} | ??????:{}".format(self.number,self.title,self.singer)

    def play(self,sW,page,view):
        sW.setCurrentWidget(page)
        search_response = youtube.search().list(
            q="???????????????"+self.number+self.title,
            order="relevance",
            part="snippet",
            maxResults=1
        ).execute()
        view.setUrl(QUrl('https://www.youtube.com/watch?v={}?autoplay=1'.format(search_response['items'][0]['id']['videoId'])))





if __name__ == '__main__':
    karaoke = QApplication(sys.argv)
    main_window = Karaoke()
    main_window.show()
    sys.exit(karaoke.exec_())