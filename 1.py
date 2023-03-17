import sys
import random
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QInputDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
import sqlite3
import math
import datetime as dt
from PyQt5.QtCore import QSize, Qt

rasdel = 0
res = 0
Number_ask = 0
v0 = 0
t = 0
a = 0
lin = 0
N = 0
M = 0
m = 0
F_r = 0
alfa = 0
rasm = 0
delta_time4 = dt.timedelta(minutes=10)
con = sqlite3.connect("Res.db")
cur = con.cursor()
name = ''
final_res = list()


class Tab(QWidget):  # Таблица
    def __init__(self):
        super(Tab, self).__init__()
        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("Результаты")
        grid_layout = QGridLayout(self)
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setRowCount(len(final_res))
        table.setHorizontalHeaderLabels(["Дата", "ФИО", "Результат"])
        table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        table.horizontalHeaderItem(2).setToolTip("Column 3 ")
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
        for i in range(len(final_res)):
            table.setItem(i, 0, QTableWidgetItem(final_res[i][1]))
            table.setItem(i, 1, QTableWidgetItem(final_res[i][2]))
            table.setItem(i, 2, QTableWidgetItem(str(final_res[i][-1])))
            table.resizeColumnsToContents()
            grid_layout.addWidget(table, 0, 0)


class KontralWork(object):  # Дизайн контольных
    def setupUi(self, Form):
        time_aut = str(self.datetime1 + delta_time4)
        self.count = 0
        Form.setObjectName("Form")
        Form.resize(526, 448)
        self.widget = QtWidgets.QLabel(Form)
        self.widget.setGeometry(QtCore.QRect(0, 20, 521, 211))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 220, 521, 131))
        self.label.setText(Get_asc())
        self.label.setObjectName("label")
        if Number_ask == 5:
            self.pixmap = QPixmap('dist/1.png')
            self.widget.setPixmap(self.pixmap)
        elif Number_ask == 15:
            self.pixmap = QPixmap('2.PNG')
            self.widget.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap('')
            self.widget.setPixmap(self.pixmap)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 370, 47, 14))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(110, 370, 271, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(420, 370, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 420, 141, 16))
        self.label_3.setObjectName("label_3")
        self.lcdNumber = QtWidgets.QLabel(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(120, 420, 121, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setText(time_aut[11:-7])
        self.retranslateUi(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lcdNumber.setAlignment(QtCore.Qt.AlignCenter)
        QtCore.QMetaObject.connectSlotsByName(Form)
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        layout.addWidget(self.label)
        layout.addWidget(self.label_2)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label_3)
        layout.addWidget(self.lcdNumber)
        self.setLayout(layout)
        cur.execute('''DELETE FROM Otvet''')
        con.commit()
        self.label.setWordWrap(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Ответ"))
        self.pushButton.setText(_translate("Form", "Ответ"))
        self.label_3.setText(_translate("Form", "Ваше время выйдет в:"))

    def Get_zadanie(self):
        self.label.setText(Get_asc())
        self.lineEdit.setText('')
        if Number_ask == 5:
            self.pixmap = QPixmap('1.png')
            self.widget.setPixmap(self.pixmap)
        elif Number_ask == 15:
            self.pixmap = QPixmap('2.PNG')
            self.widget.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap('')
            self.widget.setPixmap(self.pixmap)

    def Clic(self):
        self.count += 1
        if self.count == 10:
            self.Get_otvet()
            self.stop()
        else:
            self.Get_otvet()
            self.Get_zadanie()

    def Get_otvet(self):
        self.cor_ans = reshenie_zadach(Number_ask)
        self.datetime2 = dt.datetime.now()
        if self.datetime2 - self.datetime1 < delta_time4:
            if self.lineEdit.text():
                self.uch_ans = int(self.lineEdit.text())
                cur.execute(f'''INSERT INTO Otvet VALUES({self.count}, {self.uch_ans}, {self.cor_ans})''')
                con.commit()
            else:
                cur.execute(f'''INSERT INTO Otvet VALUES({self.count}, '', {self.cor_ans})''')
                con.commit()

        else:
            self.stop()

    def stop(self):
        self.datetime3 = dt.datetime.now()
        global res, name
        self.corr_anc = 0
        res = list(cur.execute(f'SELECT * FROM Otvet where Uc == Cr'))
        self.res = Res()
        self.res.show()
        cur.execute(
            f'''INSERT INTO Результаты(Дата, ФИО, Результат) values ('{str(self.datetime3)[:19]}', '{name}', 
            '{len(res)}')''')
        print(len(res))
        con.commit()
        self.close()


class Resalt(object):  # Результат.
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(499, 394)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(350, 320, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 30, 180, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 100, 121, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(180, 100, 61, 30))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 170, 431, 80))
        self.label_4.setObjectName("label_4")
        self.label_3.setText(str(len(res)))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.label_4.setWordWrap(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Выйти"))
        self.label.setText(_translate("Form", "Ваш результат"))
        self.label_2.setText(_translate("Form", "Правельных отвентов:"))
        self.label_4.setText(_translate("Form", "Ваш результат записан. Спросите учитель о полученной оценке"))


class Ui_Form(object):  # Диалоговое окно дизайн подготовка
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(526, 448)
        self.widget = QtWidgets.QLabel(Form)
        self.widget.setGeometry(QtCore.QRect(0, 20, 521, 211))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 220, 1680, 101))
        self.label.setText(Get_asc())
        self.label.setObjectName("label")
        if Number_ask == 5:
            self.pixmap = QPixmap('1.png')
            self.widget.setPixmap(self.pixmap)
        elif Number_ask == 15:
            self.pixmap = QPixmap('2.PNG')
            self.widget.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap('')
            self.widget.setPixmap(self.pixmap)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 320, 64, 40))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(80, 330, 271, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(400, 330, 150, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 330, 160, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(0, 360, 511, 71))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        layout.addWidget(self.label)
        layout.addWidget(self.label_2)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)
        layout.addWidget(self.pushButton_2)
        layout.addWidget(self.label_3)
        self.setLayout(layout)
        self.label.setWordWrap(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Ответ"))
        self.pushButton.setText(_translate("Form", "Ответ"))
        self.pushButton_2.setText(_translate("Form", "Новая задача"))

    def Get_zadanie(self):
        self.label.setText(Get_asc())
        self.lineEdit.setText('')
        if Number_ask == 5:
            self.pixmap = QPixmap('1.png')
            self.widget.setPixmap(self.pixmap)
        elif Number_ask == 15:
            self.pixmap = QPixmap('2.PNG')
            self.widget.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap('')
            self.widget.setPixmap(self.pixmap)

    def Get_otvet(self):
        if self.lineEdit.text() and self.lineEdit.text().isdigit():
            self.uch_ans = int(self.lineEdit.text())
            self.cor_ans = reshenie_zadach(Number_ask)
            if self.cor_ans == self.uch_ans:
                self.label_3.setText('Все верно')
            else:
                self.label_3.setText(f'Неверно! Привильный ответ: {self.cor_ans}')


class Ui_MainWindow(object):  # Главное окно дизайн
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 10, 281, 40))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 30, 300, 61))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 80, 141, 41))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 140, 250, 81))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 280, 250, 91))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 460, 350, 81))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(320, 140, 250, 81))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(320, 280, 250, 91))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(300, 80, 141, 41))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(600, 140, 250, 81))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(600, 280, 250, 91))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(460, 460, 350, 81))
        self.pushButton_8.setObjectName("pushButton_8")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(580, 80, 141, 41))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Добро пожаловать"))
        self.label_2.setText(_translate("MainWindow", "Пожалуйса выберете тему"))
        self.label_3.setText(_translate("MainWindow", "Кинематика"))
        self.pushButton.setText(_translate("MainWindow", "Режим подготовки"))
        self.pushButton_2.setText(_translate("MainWindow", "Самостоятельная работа"))
        self.pushButton_3.setText(_translate("MainWindow", "Составить таблицу с результатами "))
        self.pushButton_4.setText(_translate("MainWindow", "Режим подготовки"))
        self.pushButton_5.setText(_translate("MainWindow", "Самотоятельная работа"))
        self.label_4.setText(_translate("MainWindow", "Динамика"))
        self.pushButton_6.setText(_translate("MainWindow", "Режим подготовки"))
        self.pushButton_7.setText(_translate("MainWindow", "Самотоятельная работа"))
        self.label_5.setText(_translate("MainWindow", "Балистика"))
        self.pushButton_8.setText(_translate("MainWindow", "Отчистить таблицу с результатами"))


# Диалогвое окно самотояьельных
class AnotherWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Get_otvet)
        self.pushButton_2.clicked.connect(self.Get_zadanie)


class Res(QWidget, Resalt):  # Результат
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)


class Kontral(QWidget, KontralWork):  # Конторольная
    def __init__(self):
        self.datetime1 = dt.datetime.now()
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Clic)


class MyWidget(QMainWindow, Ui_MainWindow):  # Главное окно
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run_kin)
        self.pushButton_4.clicked.connect(self.run_din)
        self.pushButton_6.clicked.connect(self.run_bol)
        self.pushButton_2.clicked.connect(self.name_uc_kin)
        self.pushButton_5.clicked.connect(self.name_uc_din)
        self.pushButton_3.clicked.connect(self.Table)
        self.pushButton_7.clicked.connect(self.name_uc_bol)
        self.pushButton_8.clicked.connect(self.dell)

    def run_kin(self):
        global rasdel
        rasdel = 1
        self.pod = AnotherWindow()
        self.pod.show()

    def run_din(self):
        global rasdel
        rasdel = 2
        self.pod = AnotherWindow()
        self.pod.show()

    def run_bol(self):
        global rasdel
        rasdel = 3
        self.pod = AnotherWindow()
        self.pod.show()

    def name_uc_kin(self):
        global name
        fil, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                               "Введите имя и класс")
        if ok_pressed:
            name = fil
            global rasdel
            rasdel = 1
            self.kont = Kontral()
            self.kont.show()

    def name_uc_din(self):
        global name
        fil, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                               "Введите имя и класс")
        if ok_pressed:
            name = fil
            global rasdel
            rasdel = 2
            self.kont = Kontral()
            self.kont.show()

    def name_uc_bol(self):
        global name
        fil, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                               "Введите имя и класс")
        if ok_pressed:
            name = fil
            global rasdel
            rasdel = 3
            self.kont = Kontral()
            self.kont.show()

    def Table(self):
        global final_res
        final_res = list(cur.execute("""SELECT * FROM Результаты"""))
        self.lis = Tab()
        self.lis.show()

    def dell(self):
        fil, ok_pressed = QInputDialog.getText(self, "Пароль",
                                               "Введите пароль")
        if ok_pressed:
            if fil == '123456':
                cur.execute('''DELETE FROM Результаты''')
                con.commit()


def Get_asc():  # Задачник
    global Number_ask, v0, t, a, lin, N, M, F_r, m, alfa, rasm
    Number_ask = random.randrange(1, 6)
    if rasdel == 1:
        pass
    elif rasdel == 2:
        Number_ask += 10
    elif rasdel == 3:
        Number_ask += 20
    v0 = random.randrange(-500, 500)
    t = random.randrange(1, 500)
    a = random.randrange(-7, 7)
    lin = random.randrange(50, 131)
    N = random.randrange(60, 121)
    M = random.randrange(2, 11)
    m = random.randrange(1, 10001)
    F_r = random.randrange(1, 1000)
    alfa = random.randrange(20, 81)
    rasm = random.randrange(1, 10)
    ZADACHI_KIN = {
        1: f'Определить S если известно, что x0 = 0, в проекции на ось X v0 = {v0} м/с , t = {t} с, a Ускорение(a) '
           f'= {a} м/с^2. Ответ округлите до целых, написав только ответ без единиц измерений.',
        2: f'Скорость тела изменяется по закону V = {v0}t+{a}t^2, найти S({t}) = ?. Ответ округлите до целых,'
           f'написав только ответ без единиц измерений',
        3: f'За минуту человек делает {N} шагов. Определить скорость движения человека, если ширина шага {lin} см.'
           f'Ответ округлите до целых, написав только ответ без единиц измерений',
        4: f'Скорость движения тела, равная {v0} м/с, за {t} с уменьшилась в {M} раз. Определить путь, пройденный.'
           f'телом за это время, написав только ответ без единиц измерений.',
        5: f'На рисунке приведён график зависимости модуля средней скорости Vр материальной точки от времени t '
           f'при прямолинейном движении. Используя данные графика найдите путь пройденный телом за {t}. Ответ округлите '
           f'до целых, написав только ответ без единиц измерений',
        11: f'На тело массой {m} кг подействовали горизонтальной силой {F_r} Н. Какую скорость приобретет тело за {t} с'
            f'при отсутствии трения? Ответ округлите до целых, , написав только ответ без единиц измерений',
        12: f'Груз массой {M} кг подвешен на динамометре. Снизу груз тянут с силой {F_r} Н. Что показывает динамометр?'
            f'Ответ округлите до целых, написав только ответ без единиц измерений',
        13: f'Летящая пуля попадает в мешок с песком и углубляется на {lin} см.На какую глубину войдет в песок такая же'
            f'пуля, если её скорость увеличить в {M} раз? (Сила сопротивления постоянна, мешок неподвижен.)'
            f'Ответ округлите до целых, написав только ответ без единиц измерений',
        14: f'Автомобиль массой {m} кг, двигаясь равноускоренно, через {t} с достиг скорости {v0} м/с. При буксировке '
            f'трос автомобиля удлинился на 0,0{rasm} м. Определить коэффициент жесткости троса. '
            f'Ответ округлите до целых',
        15: f'Тело массой {m}кг, закреплённое на конце жёсткого невесомого стержня S длиной {lin}м, вращается в '
            f'вертикальной плоскости вокруг горизонтальной оси O, занимая последовательно положения 1, 2, 3, 4. Найдите'
            f'полную механическую энергию в положении 3.Ответ округлите до целых, написав только ответ без единиц '
            f'измерений (см.рисунок). Линейная скорость движения тела постоянна по модулю и равна {v0}м/с',
        21: f'Длина скачка блохи на столе, прыгающей под углом {alfa}° к горизонту, равна {lin}  см. Во сколько раз '
            f'высота ее. Ответ округлите до целых, написав только ответ без единиц измерений'
            f'подъема над столом превышает ее собственную  длину, составляющую 0.{rasm} мм. '
            f'Ответ округлите до целых, написав только ответ без единиц измерений',
        22: f'Камень брошен с некоторой высоты в горизонтальном направлении и упал на  Землю чере{t} с под '
            f'углом {alfa}° к вертикали. Определить начальную скорость  камня'
            f'Ответ округлите до целых, написав только ответ без единиц измерений',
        23: f'Камень, брошенный горизонтально с вышки, через {t} с упал на землю на расстоянии {lin} м от ее основания.'
            f'Чему равна скорость камня в момент  приземления?'
            f'Ответ округлите до целых',
        24: f'Камень брошен горизонтально со скоростью {v0} м/с. Через {t} с он упал на землю.С какой высоты был брошен'
            f'камень? Ответ округлите до целых, написав только ответ без единиц измерений',
        25: f'Баскетболист бросает мяч в кольцо. Скорость мяча после броска {v0} м/с и составляет {alfa}° с горизонтом.'
            f'С какой скоростью мяч попал в кольцо, если он долетел до него за {t} с.? '
            f'Ответ округлите до целых, написав только ответ без единиц измерений'
    }
    return ZADACHI_KIN[Number_ask]


def reshenie_zadach(number):  # Решебник
    if number == 1:
        ans = (v0 * t) + ((a * (t ** 2)) / 2)
    elif number == 2:
        ans = (v0 * t) + ((a * (t ** 2)) / 2)
    elif number == 3:
        ans = (N * (lin / 100)) / 60
    elif number == 4:
        ans = ((v0 * t + v0 / M * t) / 2)
    elif number == 5:
        ans = 2 * t + (2 ** 2 * t / 2)
    elif number == 11:
        ans = (F_r / m) * t
    elif number == 12:
        ans = m * 10 + F_r
    elif number == 13:
        ans = lin * (M ** 2)
    elif number == 14:
        ans = m * v0 / rasm * 0.01 * t
    elif number == 15:
        ans = m * ((v0 ** 2 / 2) + 10 * 2 * lin)
    elif number == 21:
        ans = (lin * math.tan(math.radians(alfa))) / 4 * rasm
    elif number == 22:
        ans = t * 10 * math.tan(math.radians(alfa))
    elif number == 23:
        ans = ((lin ** 2 / t ** 2) + 10 * t ** 2) ** 0.5
    elif number == 24:
        ans = t * 10 * math.tan(math.radians(alfa))
    elif number == 25:
        ans = (v0 ** 2 * math.cos(math.radians(alfa)) ** 2 + (v0 * math.sin(math.radians(alfa)) - 10 * t) ** 2) ** 0.5
    if math.fabs((ans - int(ans))) >= 0.5:
        if int(ans) > 0:
            return int(ans) + 1
        return int(ans) - 1
    return int(ans)


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 16pt;} QPushButton{font-size: 16pt;} QPushButton{background-color:#BCB8B8} "
                      "QPushButton{border-radius: 10px}")
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
