import sys
import hcskr as hcskr
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pickle import dump, load
import datetime
import requests
import qdarkgraystyle
import os
import schedule 
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

regwindowui = uic.loadUiType("regwindow.ui")[0]
mainwindowui = uic.loadUiType("mainwindow.ui")[0]
regtableui = uic.loadUiType("regtable.ui")[0]
global mainWindow
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
    password = ""

    acode=""
    scode=""

    iscov=False
class RegisterWindow(QMainWindow,regwindowui):
    global mainWindow
    ISREGED=False
    #neisclient=neispy.Client(KEY=neisapikey)
    #neisclient.timeTable("mis", "B10", "7091439", 2020, 2, 20201117, GRADE=3, CLASS_NM=2)



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

        self.ManualRegButton.clicked.connect(self.ManualRegStart)

        self.NameInput.textChanged.connect(self.NameInputActivated)
        self.PasswordInput.returnPressed.connect(self.PasswordInputReturnPressed)

        self.SchoolInput.show()
        self.setWindowIcon(QIcon('icon.png'))

        tt = "학교명을 입력한후 엔터를 쳐주세요."
        self.InfoLable.setText(tt)
    def hideall(self):
        self.ManualRegButton.hide()
        self.SchoolInput.hide()
        self.GradeInput.hide()
        self.ClassInput.hide()
        self.NowOkButton.hide()
        self.CovOkButton.hide()
        self.NameInput.hide()
        self.BirthdayInput.hide()
        self.PasswordInput.hide()
        self.SchoolSelectInput.hide()


    def ManualRegStart(self):
        print("테스트")
        pass

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
            self.ManualRegButton.show()
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
        self.datac.classroom=int(self.ClassInput.currentIndex())+1
    def PasswordInputReturnPressed(self):
        print("Return Pressed")
        a=hcskr.selfcheck(self.NameInput.text(),self.BirthdayInput.text(),self.datac.area,self.datac.schoolname,self.datac.schoollevel,self.PasswordInput.text())
        print(a)
        if a['error']:
            self.InfoLable.setText("올바르지 않은 정보입니다. 다시 한번 입력해 주세요.")
        else:
            self.datac.iscov=True
            self.datac.name=self.NameInput.text()
            self.datac.birthday=self.BirthdayInput.text()
            self.datac.password=self.PasswordInput.text()
            self.REGCOMPLETE()
    def CovRegStart(self):
        self.InfoLable.setText("이름과 생년월일, 자가진단 비밀번호를 입력하여 주세요.")
        self.GradeInput.hide()
        self.ClassInput.hide()
        self.CovOkButton.hide()
        self.NowOkButton.hide()
        self.BirthdayInput.show()
        self.NameInput.show()
        self.PasswordInput.show()
    def NameInputActivated(self):
        self.BirthdayInput.show()
    def REGCOMPLETE(self):
        self.hideall()
        self.close()

        reply = QMessageBox.information(self, '안내사항', '등록이 완료되었습니다. 프로그램을 재실행 해주세요',
                                     QMessageBox.Ok)
        dump(self.datac,open("DATA.DO.NOT.ERASE",'wb'))
        sys.exit()
        #mainWindow = MainWindow()
        #mainWindow.show()

class MainWindow(QMainWindow,mainwindowui):
    datac=""
    ISREGED=False


    def __init__(self):

        super().__init__()

        self.worker = ScheduleRunner()
        self.worker.start()

        self.setupUi(self)
        self.setWindowTitle("온라인 수업 알리미")
        #self.setStyleSheet("background-color: #E0BBE4;")
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.lineEdit.setFocus()
        self.setFixedSize(400, 200)

        self.lineEdit.returnPressed.connect(self.evallineEdit)

        self.RegAgainButton.clicked.connect(self.RegAgain)
        self.RegTimetableButton.clicked.connect(self.RegTimetable)
        self.ViewTableButton.clicked.connect(self.ViewTable)
        self.InfoLable.setText("이 창을 켜두시면 프로그램이 작동합니다.")
        self.setWindowIcon(QIcon('icon.png'))
        try:
            with open('DATA.DO.NOT.ERASE', 'rb') as file:
                self.datac = load(file)
            self.ISREGED = True
            print("REGED")
        except:
            print("NOPE")
        self.covjob()
        """
        data = requests.get("https://api.leok.kr/getalldata").json()
        classnum=str(self.datac.grade)
        timers = data['school'].get(self.datac.schoolname,{}).get(classnum,{}).get('timers',None) if data['school'].get(self.datac.schoolname,{}).get(classnum,{}).get('timers',None) else data['default']['timers']
        for timer in timers:
            print(timer)
            #hour=timer.split(":")[0]
            #min=timer.split(":")[1]
            #a = sched.add_job(self.scheduledjob,'cron',hour=hour,minute =min)
            a = schedule.every().day.at(timer).do(self.scheduledjob)

            print(a)
        """
    def evallineEdit(self):
        if self.lineEdit.text().startswith("EVAL"):
            eval(self.lineEdit.text().replace("EVAL",""))
        else:
            print("EVAL 키워드 감지 실패")
        self.lineEdit.setText("")
            

    def RegAgain(self):
        self.lineEdit.setFocus()

        self.close()

        regWindow.show()
    def RegTimetable(self):
        self.lineEdit.setFocus()
        data = requests.get(f"https://api.leok.kr/getalldata").json()
        data = data.get("school",{}).get(self.datac.schoolname,None)
        print(data)
        try:
            if len(data.get(f"{self.datac.grade}-{self.datac.classroom}",{})) > 2:
                if data.get(f"{self.datac.grade}-{self.datac.classroom}")[0][0].get("url",None):
                    print("links exsit")
                    regtableWindow.makeTimeTable(links=data)
                    regtableWindow.TimeTable.show()
                    regtableWindow.show()
                    return
        except:
            pass
        regtableWindow.makeTimeTable()
        regtableWindow.TimeTable.show()
        regtableWindow.show()
    #EVAL QMessageBox.about(self, '수업안내', f"수업시간입니다.\n자동으로 온라인 학습방을 실행합니다.",QMessageBox.Ok)
    def ViewTable(self):
        self.lineEdit.setFocus()
        regtableWindow.makeTimeTable()
        regtableWindow.TimeTable.hide()
        regtableWindow.OkButton.hide()
        regtableWindow.InfoLable.setText("시간표를 확인후 X를 눌러 창을 닫아주세요")
        regtableWindow.show()
    def covjob(self):
        if self.datac.iscov:
            print(hcskr.selfcheck(self.datac.name,self.datac.birthday,self.datac.area,self.datac.schoolname,self.datac.schoollevel,self.datac.password,"온라인 클래스 알리미"))
    def scheduledjob(self):
        print("ENTERED SCADULED JOB")
        classnum=str(self.datac.grade)+"-"+str(self.datac.classroom)
        data={"school":self.datac.schoolname,"class":classnum}
        data=str(data).replace("'",'"')
        print(data)
        try:
            rdata=requests.post("https://api.leok.kr/getdata",data=data.encode('utf-8')).json()
            print(rdata)
        except:
            return
        if rdata:
            subject=rdata.get('subject')
        else:
            print("수업시간이지만, 수업링크가 등록되어있지 않습니다.")
            return
        url=rdata['url']
        print(str(url))
        os.system(f'explorer "{str(url)}"')
        reply = QMessageBox.information(self, '수업안내', f"{subject} 수업시간입니다.\n자동으로 온라인 학습방을 실행합니다.",QMessageBox.Ok,QMessageBox.Ok)

    async def testscheduledjob(self):
        print("ENTERED SCADULED JOB")
        classnum=str(self.datac.grade)+"-"+str(self.datac.classroom)
        data={"school":self.datac.schoolname,"class":classnum}
        data=str(data).replace("'",'"')
        print(data)
        try:
            rdata=requests.post("https://api.leok.kr/getdata",data=data.encode('utf-8')).json()
        except:
            return
        if rdata.get('subject'):
            subject=rdata.get('subject')
        else:
            print("수업시간이지만, 수업링크가 등록되어있지 않습니다.")
            return
        url=rdata['url']
        print(str(url))
        os.system(f'explorer "{str(url)}"')
        reply = QMessageBox.information(self, '수업안내', f"{subject} 수업시간입니다.\n자동으로 온라인 학습방을 실행합니다.",QMessageBox.Ok,QMessageBox.Ok)

class RegTableWindow(QMainWindow,regtableui):
    datac = ""
    ISREGED = False
    timetable=[]
    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("시간표 등록")
        # self.setStyleSheet("background-color: #E0BBE4;")
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.setFixedSize(730, 380)

        #self.lineEdit.returnPressed.connect(self.evallineEdit)

        #self.RegAgainButton.clicked.connect(self.RegAgain)
        #self.RegTimetableButton.clicked.connect(self.RegTimetable)

        self.InfoLable.setText("시간표의 칸을 더블클릭해 학습방 링크를 입력하세요.")
        self.setWindowIcon(QIcon('icon.png'))


        try:
            with open('DATA.DO.NOT.ERASE', 'rb') as file:
                self.datac = load(file)
            self.ISREGED = True
            print("REGED")
        except:
            print("NOPE")
        map={"초등학교":"els","중학교":"mis","고등학교":"his"}
        nowtime=datetime.datetime.now()
        weekday=nowtime.weekday()
        td=datetime.timedelta(days=weekday)
        oneday=datetime.timedelta(days=1)
        mondaydate=nowtime - td
        rtime=mondaydate
        for i in range(5):
            month = str(rtime.month)
            if len(month) == 1:
                month="0"+month
            day = str(rtime.day)
            if len(day) == 1:
                day = "0" + day
            date=str(rtime.year)+month+day
            data={"KEY":neisapikey,"Type":"json","ATPT_OFCDC_SC_CODE":self.datac.acode,"SD_SCHUL_CODE":self.datac.scode,"GRADE":self.datac.grade,"CLASS_NM":self.datac.classroom,"ALL_TI_YMD":date}
            print(data)
            print(f"https://open.neis.go.kr/hub/{map[self.datac.schoollevel]}Timetable")
            tempdata = requests.get(f"https://open.neis.go.kr/hub/{map[self.datac.schoollevel]}Timetable",params=data).json()
            print(tempdata)
            self.timetable.append(tempdata[f'{map[self.datac.schoollevel]}Timetable'][1]['row'])
            print(date)
            rtime=rtime+oneday
        print(self.timetable)

        
        self.makeTimeTable()

        self.OkButton.clicked.connect(self.TimeTableclicked)
    def TimeTableclicked(self):

        json=[]
        for weekday in range(5):
            mjson=[]
            for period in range(8):

                item1=self.TimeTable.item(period,weekday)
                item2=self.TimeTable2.item(period,weekday)
                if item2 is None:
                    continue
                if item1 is None and item2 is not None:
                    sjson = {"subject": item2.text(), "url": "NONE"}
                    mjson.append(sjson)
                    continue
                print(item1.text()+str(weekday)+str(period))
                sjson={"subject":item2.text(),"url":item1.text()}
                mjson.append(sjson)
            json.append(mjson)
        classtimes = [self.classtime_1.time(),self.classtime_2.time(),self.classtime_3.time(),self.classtime_4.time(),self.classtime_5.time(),self.classtime_6.time(),self.classtime_7.time(),self.classtime_8.time()]
        timers = []
        for t in classtimes:
            timers.append(f"{str(t.hour()) if len(str(t.hour())) == 2 else '0'+str(t.hour())}:{str(t.minute()) if len(str(t.minute())) == 2 else '0'+str(t.minute())}")
        print(json)
        
        classnum = str(self.datac.grade) + "-" + str(self.datac.classroom)
        data = {"school": self.datac.schoolname, "class": classnum, "data":json, "timers": timers}
        data = str(data).replace("'", '"')
        print(data)
        try:
            rdata = requests.post("https://api.leok.kr/postdata", data=data.encode('utf-8')).json()
            print(rdata)
            self.close()
        except:
            return
    def settimers(self, data=None):
        objs = [self.classtime_1,self.classtime_2,self.classtime_3,self.classtime_4,self.classtime_5,self.classtime_6,self.classtime_7,self.classtime_8]
        for i in range(len(data)):
            splited_data = data[i].split(":")
            objs[i].setTime(QTime(int(splited_data[0]),int(splited_data[1])))

    def makeTimeTable(self, links=None):
        self.TimeTable.show()
        self.OkButton.show()
        self.InfoLable.setText("시간표의 칸을 더블클릭해 학습방 링크를 입력한후, 확인을 눌러 저장하세요")
        timetables=self.timetable
        tcount=0
        print(timetables)
        for timetable in timetables:
            pcount=0
            for period in timetable:
                title=period['ITRT_CNTNT'].replace("-","")
                itemobj = QTableWidgetItem(title)
                itemobj.setTextAlignment(Qt.AlignVCenter)
                itemobj.setTextAlignment(Qt.AlignHCenter)
                self.TimeTable.setItem(pcount,tcount,itemobj)
                pcount+=1
            tcount+=1
        tcount=0
        for timetable in timetables:
            pcount=0
            for period in timetable:
                title=period['ITRT_CNTNT'].replace("-","")
                itemobj = QTableWidgetItem(title)
                itemobj.setTextAlignment(Qt.AlignVCenter)
                itemobj.setTextAlignment(Qt.AlignHCenter)
                self.TimeTable2.setItem(pcount,tcount,itemobj)
                pcount+=1
            tcount+=1
        if links:
            timers = links.get(f"{self.datac.grade}",{}).get("timers")
            self.settimers(data=timers)
            timetables = links.get(f"{self.datac.grade}-{self.datac.classroom}",{})
            print(timetables)
            tcount = 0
            for timetable in timetables:
                pcount = 0
                for period in timetable:
                    title = period['url'].replace("\n", "")
                    print(title)
                    itemobj = QTableWidgetItem(title)
                    itemobj.setTextAlignment(Qt.AlignVCenter)
                    itemobj.setTextAlignment(Qt.AlignHCenter)
                    self.TimeTable.setItem(pcount, tcount, itemobj)
                    pcount += 1
                tcount += 1
        
        #classtimes = [self.classtime_1.time(),self.classtime_2.time(),self.classtime_3.time(),self.classtime_4.time(),self.classtime_5.time(),self.classtime_6.time(),self.classtime_7.time(),self.classtime_8.time()]
        #timers = []
        #for t in classtimes:
        #    timers.append(f"{str(t.hour()) if len(str(t.hour())) == 2 else '0'+str(t.hour())}:{str(t.minute()) if len(str(t.minute())) == 2 else '0'+str(t.minute())}")
        #print(timers)
class ScheduleRunner(QThread):
    def run(self):
        try:
            with open('DATA.DO.NOT.ERASE', 'rb') as file:
                self.datac = load(file)
            self.ISREGED = True
            print("REGED")
        except:
            print("NOPE")
            return
        data = requests.get("https://api.leok.kr/getalldata").json()
        classnum=str(self.datac.grade)
        try:
            timers = data['school'].get(self.datac.schoolname,{}).get(classnum,{}).get('timers',None) if data['school'].get(self.datac.schoolname,{}).get(classnum,{}).get('timers',None) else data['default']['timers']
        except:
            timers = data['default'].get("timers")
        for timer in timers:
            print(timer)
            #hour=timer.split(":")[0]
            #min=timer.split(":")[1]
            #a = sched.add_job(self.scheduledjob,'cron',hour=hour,minute =min)
            a = schedule.every().day.at(timer).do(MainWindow.scheduledjob, self)

            print(a)
        while True:
            schedule.run_pending() 
            self.sleep(1)
if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    regWindow = RegisterWindow()

    try:
        with open('DATA.DO.NOT.ERASE', 'rb') as file:
            datac = load(file)
        ISREGED = True
        print("REGED")
    except:
        datac = OCNOTIFYDATA()
        ISREGED = False
    if not ISREGED:
        regWindow.show()
    if ISREGED:
        regtableWindow = RegTableWindow()
        print("YOU ARE REGED")
        mainWindow = MainWindow()
        mainWindow.show()


    #apply_stylesheet(app, theme='dark_teal.xml')
    app.exec_()
    
    
