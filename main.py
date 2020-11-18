import sys
import time

import hcskr as hcskr
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pyqt5_material import apply_stylesheet,add_fonts
from PyQt5.QtGui import *
from PyQt5.QtQml import QQmlApplicationEngine
#import neispy
from pickle import dump, load
import datetime
import requests
import qdarkgraystyle
import os


form_class = uic.loadUiType("untitled.ui")[0]
global neisapikey
neisapikey="c365b5e4f4194c1aa1e9c9989fcc41b8"
os.environ['QT_API'] = 'pyqt5'
class OCNOTIFYDATA():
    school = ""
    clas=""

    schoolname = ""
    grade = ""
    classroom = ""
    schoollevel = ""


    name = ""
    area = ""
    birthday = ""

    acode=""
    scode=""

    iscov=False
class Window(QMainWindow,form_class):
    #schoolname = ""
    #school=""
    #grade=""
    #classroom=""
    #schoollevel=""
    #name=""
    #area=""
    #birthday=""
    ISREGED=False
    #neisclient=neispy.Client(KEY=neisapikey)
    #neisclient.timeTable("mis", "B10", "7091439", 2020, 2, 20201117, GRADE=3, CLASS_NM=2)


    try:
        with open('DATA.DO.NOT.ERASE', 'rb') as file:
            datac = load(file)
        ISREGED = True
        print("REGED")
    except:
        datac = OCNOTIFYDATA()
        ISREGED = False

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("자동 수업 알리미 등록")
        #self.setStyleSheet("background-color: #E0BBE4;")
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())

        self.hideall()
        self.setFixedSize(500, 460)



        self.SchoolInput.textChanged.connect(self.SchoolInputTextChanged)
        self.SchoolInput.returnPressed.connect(self.SchoolInputReturnPressed)

        self.GradeInput.activated.connect(self.GradeInputActivated)
        self.GradeInput.currentIndexChanged.connect(self.GradeInputIndexChanged)

        self.ClassInput.activated.connect(self.ClassInputActivated)
        self.ClassInput.currentIndexChanged.connect(self.ClassInputIndexChanged)

        self.SchoolSelectInput.itemDoubleClicked.connect(self.SchoolSelectDoubleClicked)

        self.NowOkButton.clicked.connect(self.REGCOMPLETE)

        self.CovOkButton.clicked.connect(self.CovRegStart)

        self.NameInput.textChanged.connect(self.NameInputActivated)
        self.BirthdayInput.returnPressed.connect(self.BirthdayInputReturnPressed)

        self.SchoolInput.show()


        tt = "학교명을 입력한후 엔터를 쳐주세요."
        self.InfoLable.setText(tt)
    def hideall(self):
        self.SchoolInput.hide()
        self.GradeInput.hide()
        self.ClassInput.hide()
        self.NowOkButton.hide()
        self.CovOkButton.hide()
        self.NameInput.hide()
        self.BirthdayInput.hide()
        self.SchoolSelectInput.hide()




    def SchoolInputReturnPressed(self):
        if self.SchoolInputTextChanged() ==1 or self.SchoolInput.text() == "":
            return
        self.datac.schoolname=self.SchoolInput.text()
        try:
            print(self.datac.schoolname)
            params={
                "KEY":neisapikey,
                "TYPE":"json",
                "SCHUL_NM":self.datac.schoolname
            }
            self.datac.school = requests.get("https://open.neis.go.kr/hub/schoolInfo",params).json()['schoolInfo'][1]['row']

        except:
            self.InfoLable.setText(f"존재하지 않는 학교입니다. 다시한번 확인후 입력해주세요")
            return
        print(self.datac.school)
        self.SchoolInput.hide()

        if len(self.datac.school) > 1:
            self.SchoolSelectInput.show()
            for sch in self.datac.school:
                self.SchoolSelectInput.addItem(f'{sch["ATPT_OFCDC_SC_NM"][:]}-{sch["SCHUL_NM"]}')
            self.InfoLable.setText(f"아래 리스트에서 본인의 학교를 골라주세요.")
            return
        else:
            self.datac.school=self.datac.school[0]
            self.ShowGradeInput()

    def SchoolSelectDoubleClicked(self):
        itemindex=self.SchoolSelectInput.currentRow()
        print(itemindex)
        self.SchoolSelectInput.hide()
        self.datac.school = self.datac.school[itemindex]
        self.ShowGradeInput()

    def SchoolInputTextChanged(self):
        if self.SchoolInput.text().startswith("학교명을 입력하세요") or self.SchoolInput.text().endswith("학교명을 입력하세요"):
            self.SchoolInput.setText("")
            return 1
        else:
            return 0

    def ShowGradeInput(self):
        self.GradeInput.show()

        self.datac.acode = self.datac.school['ATPT_OFCDC_SC_CODE']
        self.datac.scode = self.datac.school['SD_SCHUL_CODE']
        self.datac.area = self.datac.school['ATPT_OFCDC_SC_NM']
        self.datac.schoolname = self.datac.school['SCHUL_NM']
        self.datac.schoollevel = self.datac.school['SCHUL_KND_SC_NM']

        self.InfoLable.setText(f"본인의 학년을 골라주세요.")

        self.GradeInput.addItem('1학년')
        self.GradeInput.addItem('2학년')
        self.GradeInput.addItem('3학년')
        if self.datac.schoollevel == "초등학교":
            self.GradeInput.addItem('4학년')
            self.GradeInput.addItem('5학년')
            self.GradeInput.addItem('6학년')



    def GradeInputActivated(self):
        self.ClassInput.show()

    def GradeInputIndexChanged(self):
        print(self.GradeInput.currentIndex())
        self.datac.grade=int(self.GradeInput.currentIndex())+1
        params = {
            "KEY": neisapikey,
            "TYPE": "json",
            "ATPT_OFCDC_SC_CODE": self.datac.acode,
            "SD_SCHUL_CODE":self.datac.scode,
            "AY":datetime.datetime.now().year,
            "GRADE":int(self.datac.grade)
        }
        self.datac.clas = requests.get("https://open.neis.go.kr/hub/classInfo",params).json()['classInfo'][1]['row']
        self.ClassInput.clear()
        classlist = []
        for p in self.datac.clas:
            classlist.append(int(p['CLASS_NM']))
        classlist.sort()
        for p in classlist:
            self.ClassInput.addItem(f"{p}반")
        print(self.datac.clas)
    def ClassInputActivated(self):
        self.CovOkButton.show()
        self.NowOkButton.show()

    def ClassInputIndexChanged(self):
        print(self.ClassInput.currentIndex())
        self.datac.classroom=int(self.ClassInput.currentIndex())
    def BirthdayInputReturnPressed(self):
        a=hcskr.selfcheck(self.NameInput.text(),self.BirthdayInput.text(),self.datac.area,self.datac.schoolname,self.datac.schoollevel)
        if a['error']:
            self.InfoLable.setText("올바르지 않은 정보입니다. 다시 한번 입력해 주세요.")
        else:
            self.datac.iscov=True
            self.datac.name=self.NameInput.text()
            self.datac.birthday=self.BirthdayInput.text()
            self.REGCOMPLETE()
    def CovRegStart(self):
        self.InfoLable.setText("이름과 생년월일을 입력하여 주세요.")
        self.GradeInput.hide()
        self.ClassInput.hide()
        self.CovOkButton.hide()
        self.NowOkButton.hide()
        self.BirthdayInput.show()
        self.NameInput.show()
    def NameInputActivated(self):
        self.BirthdayInput.show()
    def REGCOMPLETE(self):
        self.hideall()
        self.close()

        reply = QMessageBox.information(self, '안내사항', '등록이 완료되었습니다.',
                                     QMessageBox.Ok)
        dump(self.datac,open("DATA.DO.NOT.ERASE",'wb'))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = QStyleFactory.create('Fusion')
    app.setStyle(s)
    myWindow = Window()

    try:
        with open('DATA.DO.NOT.ERASE', 'rb') as file:
            datac = load(file)
        ISREGED = True
        print("REGED")
    except:
        datac = OCNOTIFYDATA()
        ISREGED = False

    if not ISREGED:
        myWindow.show()
    #apply_stylesheet(app, theme='dark_teal.xml')
    app.exec_()
