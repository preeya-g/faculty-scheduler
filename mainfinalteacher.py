from PyQt5 import QtWidgets 
import sys
from PyQt5 import QtCore    
from finalteacher5 import Ui_MainWindow
from PyQt5.QtWidgets import *
from datetime import *
import time
import calendar
import pandas as pd 
from pymongo import MongoClient

class mywindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionUpload_Excel.triggered.connect(self.file_upload)
        self.ui.actionUpload_Another_Excel.triggered.connect(self.another_file)
        self.ui.actionRemove_DB.triggered.connect(self.drop_db)
        self.tab1UI()
        self.tab2UI()
        #self.ui.pushButton_2.clicked.connect(self.self_func)
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.checkBox_2.stateChanged.connect(lambda:self.disabletoggler(self.ui.checkBox_2,self.ui.timeEdit_2))
        self.ui.checkBox_2.stateChanged.connect(lambda:self.disablecombo(self.ui.checkBox_2,self.ui.comboBox_2))
        self.ui.checkBox_3.stateChanged.connect(lambda:self.disabletoggler(self.ui.checkBox_3,self.ui.timeEdit_2))
        self.ui.checkBox_4.stateChanged.connect(lambda:self.disabletoggler(self.ui.checkBox_4,self.ui.timeEdit_3))
        self.ui.checkBox_4.stateChanged.connect(lambda:self.disablecombo(self.ui.checkBox_4,self.ui.comboBox_3))
        self.ui.checkBox_5.stateChanged.connect(lambda:self.disabletoggler(self.ui.checkBox_5,self.ui.timeEdit_3))

        
        '''client = MongoClient()
        db=client.teacher
        tech=db.tech'''
    #----------disables combo
    def disablecombo(self,cb,combob):
        if cb.isChecked():
            combob.setEnabled(False)
        else:    
            combob.setEnabled(True)
   
   
    #-----------disables timetoggler
    def disabletoggler(self,cb,timee):
        if cb.isChecked():
            timee.setEnabled(False)
        else:    
            timee.setEnabled(True)
   
   
    #------quit
    def quit():
        sys.exit()
    
    
    
    #----------dbase initialization
    def dbase(self):
        global client 
        global db
        global tech
        client = MongoClient()
        db=client.teacher
        tech=db.tech

    #--------upload excel (create db)
    def file_upload(self):
            self.dbase()
            name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            print(name)
            data=pd.read_excel(name[0])
            print(data)
            data_dict = data.to_dict(orient = 'records') 
            for i in data_dict:
                i['ST']=str(i['ST'])
                i['ET']=str(i['ET'])
            result = db.tech.insert_many(data_dict)
            print('db created')
    
    
    #---------another file upload
    def another_file(self):
        self.drop_db()
        self.file_upload()
    
    #----------drop db
    def drop_db(self):
        client = MongoClient()
        client.drop_database('teacher')
        print("deleted db")
    
    #------teacher search
    def tab1UI(self):
        self.dbase()
        global names
        names=[]
        db_name=db.tech.distinct('NAME')
        #-------completer 
        for i in db_name:
            names.append(i)
        #names = ["Priya", "Rutuja", "Raja", "Aman"]
        completer = QCompleter(names)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.ui.lineEdit_2.setCompleter(completer)
        self.ui.pushButton_2.clicked.connect(self.t_display)
        self.ui.pushButton_3.clicked.connect(lambda:self.t_clear(self.ui.plainTextEdit_2))

    #---------teacher display
    def t_display(self):
        self.dbase()
        entered_name=self.ui.lineEdit_2.text()
        #self.ui.lineEdit_2.setText("")
        if not entered_name=="":

            if entered_name in names:
                self.ui.label_8.setText(" ")
                #----------time
                time=self.ui.timeEdit_2.text()      #set from timeEdit toggler
                time=time[:5]
                time=time+":00"
                

                if self.ui.checkBox_2.isChecked()==True:            #now
                #  self.ui.timeEdit_2.setEnabled(False)
                    t = datetime.time(datetime.now())
                    time=str(t)
                    my_date=date.today()
                    
                    ch=calendar.day_name[my_date.weekday()]
                    
                    if ch=='Monday':
                        day='MON'
                    elif ch=='Tuesday':
                        day='TUE'
                    elif ch=='Wednesday':
                        day='WED'
                    elif ch=='Thursday':
                        day='THU'
                    elif ch=='Friday':
                        day='FRI'
                    elif ch=='Saturday':
                        day='SAT'
                    elif ch=='Sunday':
                        day='SUN'      
                #  time="10:00"  
                    q=db.tech.find({'NAME':entered_name,'DAY':day,'ET': { "$gte":time},'ST':{"$lte":time}})
                else:
                    #--------day choice
                    choice=self.ui.comboBox_2.currentText()
                    if self.ui.checkBox_3.isChecked()==True:        #all time
                        if choice=="All":
                            q=db.tech.find({'NAME':entered_name})
                        else:        
                            q=db.tech.find({'NAME':entered_name,'DAY':choice})
                    else:
                        if choice=="All":
                            q=db.tech.find({'NAME':entered_name,'ET': { "$gte":time},'ST':{"$lte":time}})
                        else:    
                            q=db.tech.find({'NAME':entered_name,'DAY':choice,'ET': { "$gte":time},'ST':{"$lte":time}})


    
                if not q.count()==0:
                    self.ui.plainTextEdit_2.appendPlainText("Showing "+ entered_name+ "'s status- ")
                    self.ui.plainTextEdit_2.appendPlainText("DAY \t CLASS \t ROOM \t START_TIME \t END_TIME \t DIV ")
                    for cin in q:
                        self.ui.plainTextEdit_2.appendPlainText(cin['DAY']+"\t"+cin['CLASS']+"\t" +str(cin['ROOM'])+ "\t" + str(cin['ST'])+"\t"+str(cin['ET'])+"\t"+cin['DIV'])     
                else:
                    self.ui.plainTextEdit_2.appendPlainText(entered_name+' is free currently ')
                self.ui.plainTextEdit_2.appendPlainText("_"*70) 
            else:
                print("teacher does not exist")
                self.ui.label_8.setText("teacher does not exist")
        else:       
            print("enter teacher's name") 
            self.ui.label_8.setText("enter teacher's name")      
      

    def t_clear(self,textedit):
        textedit.setPlainText("")


    #------room search
    
    def tab2UI(self):
        self.dbase()
        global rooms
        rooms=[]
        db_room=db.tech.distinct('ROOM')
        
  
        #completer 
        for i in db_room:
            rooms.append(str(i))
        #names = ["Priya", "Rutuja", "Raja", "Aman"]
        completer = QCompleter(rooms)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.ui.lineEdit_3.setCompleter(completer)
        self.ui.pushButton_5.clicked.connect(self.r_display)
        self.ui.pushButton_6.clicked.connect(lambda:self.t_clear(self.ui.plainTextEdit))

    #-----room display
    def r_display(self):
        self.dbase()
        entered_room=self.ui.lineEdit_3.text()
       
       # print(type(entered_room))
        #self.ui.lineEdit_3.setText("")

        if not entered_room=="":
            int_entered_room=int(entered_room)
            if entered_room in rooms:    
                self.ui.label_7.setText("")
                #----------time
                time=self.ui.timeEdit_3.text()      #set from timeEdit toggler
                time=time[:5]
                time=time+":00"
                print(time)

                if self.ui.checkBox_4.isChecked()==True:            #now
                #  self.ui.timeEdit_2.setEnabled(False)
                    t = datetime.time(datetime.now())
                    time=str(t)
                    my_date=date.today()
                    my_date=date.today()
                    ch=calendar.day_name[my_date.weekday()]
                    
                    if ch=='Monday':
                        day='MON'
                    elif ch=='Tuesday':
                        day='TUE'
                    elif ch=='Wednesday':
                        day='WED'
                    elif ch=='Thursday':
                        day='THU'
                    elif ch=='Friday':
                        day='FRI'
                    elif ch=='Saturday':
                        day='SAT'
                    elif ch=='Sunday':
                        day='SUN'      
                    
                #  time="10:00"  
                    q=db.tech.find({"ROOM":int_entered_room,"DAY":day,"ET": { '$gte':time},"ST":{'$lte':time}})
                else:
                    #--------day choice
                    choice=self.ui.comboBox_3.currentText()
                    if self.ui.checkBox_5.isChecked()==True:        #all time
                        if choice=="All":
                            q=db.tech.find({'ROOM':int_entered_room})
                        else:        
                            q=db.tech.find({'ROOM':int_entered_room,'DAY':choice})
                    else:
                        if choice=="All":
                            q=db.tech.find({'ROOM':int_entered_room,"ET": { "$gte":time},"ST":{"$lte":time}})
                        else:    
                            q=db.tech.find({'ROOM':int_entered_room,'DAY':choice,'ET': { "$gte":time},'ST':{"$lte":time}})


    
                if not q.count()==0:
                    self.ui.plainTextEdit.appendPlainText("Showing "+ entered_room+ "'s status- ")
                    self.ui.plainTextEdit.appendPlainText("DAY \t CLASS \t NAME \t START_TIME \t END_TIME \t DIV ")
                    for cin in q:
                        self.ui.plainTextEdit.appendPlainText(cin['DAY']+"\t"+cin['CLASS']+"\t" +cin['NAME']+ "\t" + str(cin['ST'])+"\t"+str(cin['ET'])+"\t"+cin['DIV'])     
                else:
                    self.ui.plainTextEdit.appendPlainText(entered_room+' is free currently ')
                self.ui.plainTextEdit.appendPlainText("_"*70) 

            else:
                print("Check room number.Room does not exist.")
                self.ui.label_7.setText("Check room number.Room does not exist.")
        else:       
            print("Please enter Room Number")       
            self.ui.label_7.setText("Please enter Room Number")      






#----------exec
def run():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
run()


'''
#setting dropdown teacher's list
        t_names = ["Apple", "Alps", "Berry", "Cherry" ,"1"]
        completer = QCompleter(t_names)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit_2.setCompleter(completer)'''