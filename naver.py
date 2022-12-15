import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton
import json
import urllib.request

client_id = "cA5YJzezze1497wfcN01"
client_secret = "zMfCdsH6Hh"
url_translate = "https://openapi.naver.com/v1/papago/n2mt"
url_detective = "https://openapi.naver.com/v1/papago/detectLangs"


def detective(str):
    data = "query=" + str
    request = urllib.request.Request(url_detective)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    response_body = response.read()
    json_object = json.loads(response_body.decode("utf-8"))
    return json_object['langCode']

def translate(k):
    k = str(k)
    word = detective(k)
    data = "source={}&target=ko&text=".format(word) + str(k)
    request = urllib.request.Request(url_translate)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        json_object = json.loads(response_body.decode("utf-8"))
        inputstring = json_object['message']['result']['translatedText']
    else:
        inputstring = "something wrong. \nError Code: {}".format(rescode)
    return inputstring

def diction(string):
    url_ask = "https://openapi.naver.com/v1/search/encyc?query=" + string
    request = urllib.request.Request(url_ask)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    response_body = response.read()
    json_object = json.loads(response_body.decode("utf-8"))
    k = ""
    for a in json_object['items']:
        k = k + 'ward: ' + a['title'] + '\n' + 'description: ' + a['description'] + '\n'
    return k

def ask(string):
    url_ask = "https://openapi.naver.com/v1/search/kin?query=" + string
    request = urllib.request.Request(url_ask)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    response_body = response.read()
    json_object = json.loads(response_body.decode("utf-8"))
    k = ""
    for a in json_object['items']:
        k = k + 'title: ' + a['title'] + '\n' + 'link: ' + a['link'] + '\n'
    return k

def shop(string):
    url_shop = "https://openapi.naver.com/v1/search/shop?query=" + string
    request = urllib.request.Request(url_shop)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    response_body = response.read()
    json_object = json.loads(response_body.decode("utf-8"))
    k = ""
    for a in json_object['items']:
        k = k + 'title: ' + a['title'] + '\n' + 'link: ' + a['link'] + '\n'
    return k

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('검색', self)
        self.btn.setCheckable(False)
        self.btn.toggle()
        self.btn.clicked.connect(self.pushbutton)

        self.label1 = QLabel("Enter your sentence:")
        self.te1 = QTextEdit()
        self.te1.setAcceptRichText(False)

        self.label2 = QLabel("Answer:")
        self.te2 = QTextEdit()
        self.te2.setAcceptRichText(False)

        self.label3 = QLabel("dictionary:")
        self.te3 = QTextEdit()
        self.te3.setAcceptRichText(False)

        self.label4 = QLabel("Link:")
        self.te4 = QTextEdit()
        self.te4.setAcceptRichText(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label1)
        vbox.addWidget(self.te1)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.te2)
        vbox.addWidget(self.label4)
        vbox.addWidget(self.te4)
        vbox.addWidget(self.label3)
        vbox.addWidget(self.te3)


        self.setLayout(vbox)

        self.setWindowTitle('Naver')
        self.resize(300, 400)
        self.show()

    def pushbutton(self):
        self.te2.clear()
        self.te3.clear()
        self.te4.clear()
        k = self.te1.toPlainText()
        cnt = k.find('//')
        if cnt != -1:
            nextcnt = k.find('//', cnt+1)
            input = diction(k[cnt + 2:nextcnt])
            k = k.replace('//', '')
            self.te3.setPlainText(input)
        elif len(k.split()) == 1:
            if detective(k) == 'ko' or detective(k) == 'en':
                input = diction(k)
                self.te3.setPlainText(input)

        if (k[-1:] == '?'):
            #ask
            k = k[:-1]
            input = ask(str(k))
            self.te4.setPlainText(input)
        elif (k[-1:] == '/'):
            #shop
            input = shop(str(k))
            k = k[:-1]
            self.te4.setPlainText(input)

        #trans
        input = translate(str(k))
        self.te2.setPlainText(input)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())