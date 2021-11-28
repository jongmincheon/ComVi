import sys
import pickle
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QListView, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import requests
from bs4 import BeautifulSoup
import random
import copy


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.left = 600
        self.top = 400
        self.width =  600
        self.height = 500
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("English")
        self.filename = 'wordlist.pickle'
        self.wordsdata = {}


        self.key = "e1f3f486-29e7-41c8-9492-8e56e44aca50"
        self.dic_url1 = "http://dic.daum.net/search.do?q={0}"
        self.dic_url2 = "https://dictionaryapi.com/api/v3/references/thesaurus/json/{0}?key={1}"
        self.dic_url3 = "https://dic.daum.net/word/view.do?wordid={0}"

    def setWidgets(self):

        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as wordlistreader:
                self.wordsdata = pickle.load(wordlistreader)
        else:
            with open(self.filename, 'wb') as wordlistwriter:
                pickle.dump(self.wordsdata, wordlistwriter)

        self.labeltitle = QLabel('ComVi', self)
        self.label1 = QLabel('영어단어 암기', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
        self.label4 = QLabel('', self)
        self.label5 = QLabel('', self)

        self.labeltitle.setFont(QFont('Arial', 28))
        self.labeltitle.setStyleSheet("color: green")
        self.label1.setFont(QFont('Serif', 22))
        self.label2.setFont(QFont('Serif', 22))
        self.label3.setFont(QFont('Serif', 22))
        self.label4.setFont(QFont('Serif', 22))
        self.label5.setFont(QFont('Serif', 22))
        self.label1.setToolTip('asdf')
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.labeltitle)
        self.vbox1.addWidget(self.label1)
        self.vbox1.addWidget(self.label2)
        self.vbox1.addWidget(self.label3)
        self.vbox1.addWidget(self.label4)
        self.vbox1.addWidget(self.label5)
        self.setLayout(self.vbox1)

        self.btn1 = QPushButton('단어 목록', self)
        self.btn2 = QPushButton('단어 맞추기', self)
        self.btn3 = QPushButton('뜻 맞추기', self)
        self.btn4 = QPushButton('문장 빈칸 퀴즈', self)

        self.btn1.setFont(QFont('Arial', 15))
        self.btn2.setFont(QFont('Arial', 15))
        self.btn3.setFont(QFont('Arial', 15))
        self.btn4.setFont(QFont('Arial', 15))

        self.btn1.setGeometry(400, 60, 150, 50)
        self.btn2.setGeometry(400, 160, 150, 50)
        self.btn3.setGeometry(400, 260, 150, 50)
        self.btn4.setGeometry(400, 360, 150, 50)

        self.btn1.clicked.connect(self.OpenWordListWindow)
        self.btn2.clicked.connect(self.OpenMod1Window)
        self.btn3.clicked.connect(self.OpenMod2Window)
        self.btn4.clicked.connect(self.OpenMod3Window)





    def OpenWordListWindow(self):
        self.wordlistwin = WordListWindow()
        self.wordlistwin.setWidgets()
        self.wordlistwin.show()

    def OpenMod1Window(self):
        self.mod1win = Mod1Window()
        self.mod1win.setWidgets()
        self.mod1win.show()

    def OpenMod2Window(self):
        self.mod2win = Mod2Window()
        self.mod2win.setWidgets()
        self.mod2win.show()

    def OpenMod3Window(self):
        self.mod3win = Mod3Window()
        self.mod3win.setWidgets()
        self.mod3win.show()
        

    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료", "종료하시겠습니까?", (QMessageBox.Yes | QMessageBox.No), QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QApplication.closeAllWindows()
        else:
            QCloseEvent.ignore()



class WordListWindow(MainWindow):
    def __init__(self):
        super().__init__()
    def setWidgets(self):
        with open(self.filename, 'rb') as wordlistreader:
            self.wordsdata = pickle.load(wordlistreader)
        self.selectedword = ''
        self.wordlistvbox = QVBoxLayout()
        self.wordinputvbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.wordlist = QListView(self)
        self.model = QStandardItemModel()

        self.wordlist.setModel(self.model)
        self.label_english_word = QLabel('English Words', self)
        self.remove_word = QPushButton('목록에서 제거하기', self)
        self.wordlistvbox.addWidget(self.label_english_word)
        self.wordlistvbox.addWidget(self.wordlist)
        self.wordlistvbox.addWidget(self.remove_word)


        self.wordinputlabel = QLabel('단어 추가', self)
        self.wordinput = QLineEdit('', self)
        self.addword = QPushButton('추가', self)
        self.wordexplanation = QLabel('', self)
        self.wordexplanation.setWordWrap(True)
        self.wordinputvbox.addWidget(self.wordinputlabel)
        self.wordinputvbox.addWidget(self.wordinput)
        self.wordinputvbox.addWidget(self.addword)
        self.wordinputvbox.addWidget(self.wordexplanation)

        self.wordinputlabel.setFont(QFont('serif', 22))
        self.wordinputlabel.setFixedSize(200, 80)
        self.wordexplanation.setAlignment(Qt.AlignTop)

        self.hbox.addLayout(self.wordlistvbox)
        self.hbox.addLayout(self.wordinputvbox)
        self.setLayout(self.hbox)
        self.UpdateWordList()

        self.addword.clicked.connect(lambda: self.PutInPickle(self.wordinput.text()))
        self.remove_word.clicked.connect(lambda: self.RemoveWord())
        self.wordlist.clicked.connect(self.ShowExplanation)

    def RemoveWord(self):
        if self.selectedword == '':
            pass
        else:
            self.wordsdata.pop(self.selectedword)
            self.UpdateWordList()
            self.selectedword = ''

    def ShowExplanation(self, index):
        self.selectedword = self.model.itemFromIndex(index).text()
        synonym_in_text = '유의어: ' + ', '.join(self.wordsdata[self.selectedword]['syns'])
        antonym_in_text = '반의어: ' + ', '.join(self.wordsdata[self.selectedword]['ants'])
        displayinfo = self.selectedword + '의 뜻: \n' + self.wordsdata[self.selectedword]['definition'] + '\n' + synonym_in_text + '\n\n' + antonym_in_text
        self.wordexplanation.setText(displayinfo)
    def UpdateWordList(self):
        self.model.clear()
        for word in self.wordsdata.keys():
            self.model.appendRow(QStandardItem(word))
        with open(self.filename, 'wb') as wordlistwriter:
            pickle.dump(self.wordsdata, wordlistwriter)

    def PutInPickle(self, word):
        if not word.isascii():
            self.wordexplanation.setText('입력하신 단어가 영단어가 아닙니다')
        elif word in self.wordsdata.keys():
            self.wordexplanation.setText('이미 목록에 있는 단어입니다.')
        else:
            worddata = self.FindWord(word)
            if worddata != 0:
                self.wordsdata[word] = worddata
                self.UpdateWordList()
                worditem = self.model.findItems(word)[0]
                wordindex = self.model.indexFromItem(worditem)
                self.ShowExplanation(wordindex)

    def FindWord(self, word):
        synonyms = []
        antonyms = []
        definition = ''
        wordid = ''
        r1 = requests.get(self.dic_url1.format(word)) # afff
        soup1 = BeautifulSoup(r1.text, "html.parser")
        definitionlists = soup1.find_all('ul', {'class':'list_search'})

        if definitionlists == []:
            self.wordexplanation.setText('단어가 존재하지 않습니다')
            return 0
        else:
            foundword = soup1.find('a', {'class': "txt_cleansch"}).text
            if foundword != word:
                self.wordexplanation.setText('단어가 존재하지 않습니다')
                return 0
            else:
                definition = definitionlists[0].text
                wordid = soup1.find('a', {'class': 'btn_wordbook btn_save'})['data-wordid']



        r2 = requests.get(self.dic_url2.format(word, self.key))
        soup2 = BeautifulSoup(r2.text, "html.parser")
        if r2.json() == []:
            synonyms = ['없음']
            antonyms = ['없음']
        elif (type(r2.json()[0]) != dict):
            synonyms = ['없음']
            antonyms = ['없음']
        elif (r2.json()[0]['meta']['id'] != word):
            synonyms = ['없음']
            antonyms = ['없음']
        else:
            if r2.json()[0]['meta']['syns'] == []:
                synonyms = ['없음']
            else:
                synonyms = r2.json()[0]['meta']['syns'][0]
            if r2.json()[0]['meta']['ants'] == []:
                antonyms = ['없음']
            else:
                antonyms = r2.json()[0]['meta']['ants'][0]

        r3 = requests.get(self.dic_url3.format(wordid))
        soup3 = BeautifulSoup(r3.text, "html.parser")
        examples = soup3.find_all('span', {'class': 'txt_example'})
        example_eng = []
        for example in examples:
            example_in_words = example.find_all('daum:word')
            one_example_words = []
            for exampleword in example_in_words:
                one_example_words.append(exampleword.text)
            one_example = " ".join(one_example_words)
            example_eng.append(one_example)

        example_meanings = soup3.find_all('span', {'class': 'mean_example'})
        example_list = []
        for i in range(len(example_meanings)):
            example_list.append([example_eng[i], example_meanings[i].text])
        datadict = {'definition': definition, 'syns': synonyms, 'ants': antonyms, 'examples': example_list}
        return datadict
    def closeEvent(self, QCloseEvent):
        pass


class Mod1Window(MainWindow):
    def __init__(self):
        super().__init__()
        with open(self.filename, 'rb') as wordlistreader:
            self.wordsdata = pickle.load(wordlistreader)
        self.Selectenglishdata()


    def Selectenglishdata(self):
        self.selectedenglishword = random.choice(list(self.wordsdata.keys()))  # 딕셔너리들 중 하나 선택
        self.selecteddefinition = self.wordsdata[self.selectedenglishword]['definition']        #definition 키 value

    def setWidgets(self):
        self.Wordshowlabel = QLabel(self.selectedenglishword, self)
        self.Wordtypeinput = QLineEdit('', self)
        self.Wordcheckbtn = QPushButton('입력', self)
        self.Mod1vbox = QVBoxLayout(self)

        self.Wordtypeinput.setFixedSize(500, 50)
        self.Wordshowlabel.setFixedHeight(200)
        self.Wordshowlabel.setFont(QFont('serif', 22))
        self.Wordcheckbtn.setFixedSize(200, 50)
        self.Wordcheckbtn.setFont(QFont('serif', 16))
        self.Mod1vbox.setAlignment(Qt.AlignCenter)
        self.Mod1vbox.setAlignment(Qt.AlignVCenter)

        self.Mod1vbox.addWidget(self.Wordshowlabel)
        self.Mod1vbox.addWidget(self.Wordtypeinput)
        self.Mod1vbox.addWidget(self.Wordcheckbtn)
        self.Wordcheckbtn.clicked.connect(self.WordJudgement)

    def WordJudgement(self):
        self.englishworddata = self.selecteddefinition
        self.typeword = self.Wordtypeinput.text()
        if self.typeword in self.englishworddata:
            QMessageBox.about(self, 'MessageBox', '정답입니다!')
            self.Selectenglishdata()
            self.Wordshowlabel.setText(self.selectedenglishword)
            self.Wordtypeinput.clear()
        else:
            QMessageBox.about(self, 'MessageBox', '틀렸습니다 다시 시도해 주세요')
            self.Wordtypeinput.clear()
            pass

    def closeEvent(self, QCloseEvent):
        pass


class Mod2Window(MainWindow):
    def __init__(self):
        super().__init__()
        with open(self.filename, 'rb') as wordlistreader:
            self.wordsdata = pickle.load(wordlistreader)
        self.Selectenglishdata()


    def Selectenglishdata(self):
        self.selectedenglishword = random.choice(list(self.wordsdata.keys()))  # 딕셔너리들 중 하나 선택
        self.selecteddefinition = self.wordsdata[self.selectedenglishword]['definition']        #definition 키 value

    def setWidgets(self):
        self.Wordshowlabel = QLabel(self.selecteddefinition, self)
        self.Wordtypeinput = QLineEdit('', self)
        self.Wordcheckbtn = QPushButton('입력', self)
        self.Mod1vbox = QVBoxLayout(self)

        self.Wordtypeinput.setFixedSize(500, 50)
        self.Wordshowlabel.setFixedHeight(200)
        self.Wordshowlabel.setFont(QFont('serif', 22))
        self.Wordcheckbtn.setFixedSize(200, 50)
        self.Wordcheckbtn.setFont(QFont('serif', 16))
        self.Mod1vbox.setAlignment(Qt.AlignCenter)
        self.Mod1vbox.setAlignment(Qt.AlignVCenter)

        self.Mod1vbox.addWidget(self.Wordshowlabel)
        self.Mod1vbox.addWidget(self.Wordtypeinput)
        self.Mod1vbox.addWidget(self.Wordcheckbtn)
        self.Wordcheckbtn.clicked.connect(self.WordJudgement)

    def WordJudgement(self):
        self.englishworddata = self.selectedenglishword
        self.typeword = self.Wordtypeinput.text()
        if self.typeword == self.englishworddata:
            QMessageBox.about(self, 'MessageBox', '정답입니다!')
            self.Selectenglishdata()
            self.Wordshowlabel.setText(self.selecteddefinition)
            self.Wordtypeinput.clear()
        else:
            QMessageBox.about(self, 'MessageBox', '틀렸습니다 다시 시도해 주세요')
            self.Wordtypeinput.clear()
            pass

    def closeEvent(self, QCloseEvent):
        pass


class Mod3Window(MainWindow):
    def __init__(self):
        super().__init__()
        with open(self.filename, 'rb') as wordlistreader:
            self.wordsdata = pickle.load(wordlistreader)
        self.Selectenglishdata()


    def Selectenglishdata(self):
        self.selectedenglishword = random.choice(list(self.wordsdata.keys()))  # 딕셔너리들 중 하나 선택
        self.selectedexamples = self.wordsdata[self.selectedenglishword]['examples'][0][0]        #examples 키 value
        self.examplesdefinition = self.wordsdata[self.selectedenglishword]['examples'][0][1]
        if self.selectedenglishword in self.selectedexamples:
            self.blankexamples = self.selectedexamples.replace(self.selectedenglishword, '_', 7)

    def setWidgets(self):
        self.Wordshowlabel = QLabel(self.blankexamples, self)
        self.Definitionlabel = QLabel(self.examplesdefinition, self)
        self.Wordtypeinput = QLineEdit('', self)
        self.Wordcheckbtn = QPushButton('입력', self)
        self.Mod1vbox = QVBoxLayout(self)

        self.Wordtypeinput.setFixedSize(500, 50)
        self.Wordshowlabel.setFixedHeight(50)
        self.Wordshowlabel.setFont(QFont('serif', 16))
        self.Definitionlabel.setFixedHeight(50)
        self.Definitionlabel.setFont(QFont('serif', 16))
        self.Wordcheckbtn.setFixedSize(200, 50)
        self.Wordcheckbtn.setFont(QFont('serif', 16))
        self.Mod1vbox.setAlignment(Qt.AlignCenter)
        self.Mod1vbox.setAlignment(Qt.AlignVCenter)

        self.Mod1vbox.addWidget(self.Wordshowlabel)
        self.Mod1vbox.addWidget(self.Definitionlabel)
        self.Mod1vbox.addWidget(self.Wordtypeinput)
        self.Mod1vbox.addWidget(self.Wordcheckbtn)
        self.Wordcheckbtn.clicked.connect(self.WordJudgement)

    def WordJudgement(self):
        self.englishworddata = self.selectedenglishword
        self.typeword = self.Wordtypeinput.text()
        if self.typeword == self.englishworddata:
            QMessageBox.about(self, 'MessageBox', '정답입니다!')
            self.Selectenglishdata()
            self.Wordshowlabel.setText(self.blankexamples)
            self.Definitionlabel.setText(self.exampledefinition)
            self.Wordtypeinput.clear()
        else:
            QMessageBox.about(self, 'MessageBox', '틀렸습니다 다시 시도해 주세요')
            self.Wordtypeinput.clear()
            pass


    def closeEvent(self, QCloseEvent):
        pass




if __name__ == '__main__':


    app = QApplication(sys.argv)
    win = MainWindow()
    win.setWidgets()
    win.show()
    app.exec_()
