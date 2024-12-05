import io
import sys
import sqlite3 as sq

from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QMessageBox
from PyQt6.QtWidgets import QApplication, QMainWindow


with open('main.ui', encoding='utf-8') as file:
    f = file.read()
    template = f

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.connection = sq.connect('coffee.sqlite')
        self.cur = self.connection.cursor()
        self.add.clicked.connect(self.add_handler)
        self.edit.clicked.connect(self.edit_handler)
        self.update_table()

    def update_table(self):
        query = f'''SELECT ID, a AS 'Название сорта', b AS 'Степень обжарки', c AS 'Молотый/в зернах', d AS 'описание вкуса', e AS 'Цена', f AS 'Обьем упаковки'  FROM coffee'''

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

    def add_handler(self):
        window = Window(self, mode='add')
        window.show()
        window.exec()
        self.update_table()

    def edit_handler(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))  # ряд с нуля
        ids = [self.tableWidget.item(i, 0).text() for i in rows]  # id
        self.lst = []
        if rows:
            for i in enumerate(self.cur.execute(f'SELECT * FROM coffee WHERE ID = {"".join(ids)}')):
                for index, value in enumerate(i):
                    self.lst = value
            window = Window(self, id=ids, query=self.lst, mode='edit')
            window.show()
            window.exec()
            self.update_table()
        else:
            QMessageBox.warning(self, '', 'Вы не выбрали строку')
            self.lst = None


with open('addEditCoffeeForm.ui', encoding='utf-8') as file:
    f = file.read()
    tempalate2 = f


class Window(QDialog):
    def __init__(self, parent, id=None, mode=None, query=None):
        super().__init__()
        f = io.StringIO(tempalate2)
        uic.loadUi(f, self)
        self.query = query
        self.cancel.clicked.connect(self.reject)
        self.connection = sq.connect('coffee.sqlite')
        self.cur = self.connection.cursor()
        if mode == 'edit':
            self.id = ''.join(id)
            self.save.clicked.connect(self.edit_method)
            self.get_plain()
        if mode == 'add':
            self.save.clicked.connect(self.add_method)

    def edit_method(self):
        self.updated = []
        for i in range(1, 7):
            editText = getattr(self, f'plainTextEdit_{i}', None)
            self.updated.append(editText.toPlainText())
        self.cur.execute(f'UPDATE coffee SET a = ?, b = ?, c = ?, d = ?, e = ?, f = ? WHERE ID = {self.id}',
                         (*self.updated,))
        self.connection.commit()
        self.accept()

    def get_plain(self):
        for index, value in enumerate(self.query):
            if index > 0:
                editText = getattr(self, f'plainTextEdit_{index}', None)
                editText.setPlainText(value)

    def add_method(self):
        self.updated = []
        for i in range(1, 7):
            editText = getattr(self, f'plainTextEdit_{i}', None)
            self.updated.append(editText.toPlainText())
        self.cur.execute('INSERT INTO coffee(a, b, c, d, e, f) VALUES(?, ?, ?, ?, ?, ?)', (*self.updated,))
        self.connection.commit()
        self.accept()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())