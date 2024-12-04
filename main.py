import io
import sys
import sqlite3 as sq
from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QApplication, QMainWindow

with open('main.ui') as file:
    ui_text = file.read()
    template = ui_text

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.connection = sq.connect('coffee.sqlite')
        self.cur = self.connection.cursor()
        query = f'''SELECT ID, a AS 'Название сорта', b AS 'Степень обжарки', c AS 'Молотый/в зернах', d AS 'описание вкуса', 'e' AS 'Цена', f AS 'Обьем упаковки'  FROM coffee'''

        self.res = self.cur.execute(query).fetchall()
        self.tableWidget.setColumnCount(len(self.res[0]))
        self.tableWidget.setRowCount(0)
        column_names = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())