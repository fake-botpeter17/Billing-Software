import enum
from random import choice
from typing import Iterable
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QMenu,
    QPushButton,
    QTableWidget,
    QMainWindow,
    QApplication,
    QTableWidgetItem,
    QMessageBox,
    QWidget
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from pyautogui import press
from qt_helper import QueryFormatterColumn


class Item:
    def __init__(self, id: int = None, name :str = None, cost_price :int | float = None, selling_price :int | float = None, qnty : int = None) -> None:
        self.id = id
        self.name = name
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.qnty = qnty
    
    def getObj(self):
        return {'id':self.id, 'name': f'{self.name}', 'cp': self.cost_price, 'qnty': self.qnty, 'added': round(self.cost_price * 1.08, 2), 'sp': self.selling_price}

    def isValid(self) -> bool:
        return self.id and self.name and self.cost_price and self.selling_price and self.qnty

class QueryFormatterGUI(QMainWindow):
    Bill_Table : QTableWidget
    Query_Button :QPushButton
    Profile :QMenu
    def __init__(self) -> None:
        self.coordinates: tuple[int,int] = (0,0)
        self.rowManager :dict[int, Item] = dict()
        from notifypy import Notify
        super(QueryFormatterGUI, self).__init__()
        uic.loadUi("Resources/Query_Formatter.ui", self)
        aspect_ratio = 16 / 9  # aspect ratio
        min_height = 900
        min_width = int(min_height * aspect_ratio)
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(f"Query Formatter")
        icon = QIcon("icofi.ico")
        self.setWindowIcon(icon)
        self.Profile.triggered.connect(self.loadStock)
        self.notification = Notify(
            default_notification_title="Query Formatter",
            default_notification_icon="Resources/icofi.ico",
            default_notification_application_name="BMS"
        )
        self.show()
        self.setup()
        press('tab')
        
    def setup(self):
        self.setStyleSheet(open("Resources/Default.qss").read())
        self.Bill_Table.setColumnCount(6)  
        self.Bill_Table.setRowCount(50)
        self.Bill_Table.cellChanged.connect(self.handle_cell_change)
        self.Query_Button.clicked.connect(self.getQuery)

        self.Bill_Table.setColumnWidth(QueryFormatterColumn.Sno, 100)  
        self.Bill_Table.setColumnWidth(QueryFormatterColumn.Id, 150)  
        self.Bill_Table.setColumnWidth(QueryFormatterColumn.Name, 450)  
        self.Bill_Table.setColumnWidth(QueryFormatterColumn.CostPrice, 250)  
        self.Bill_Table.setColumnWidth(QueryFormatterColumn.SellingPrice, 250)  
        # self.Bill_Table.setColumnWidth(QueryFormatterColumn.Qnty, 250)

    def setBillColumn(self, row: int, column: int, value: str | int | float = ""):
        temp = QTableWidgetItem(str(value))
        temp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Bill_Table.setItem(row, column, temp)

    def getText(self, row: int, column: int, dtype : type = str) -> type:
        data = self.Bill_Table.item(row, column)  # type:ignore
        if data:
            return dtype(data.text())
        return ""

    def resetCellCursor(self, row, col):
        while row >= 0:
            press('up')
            row -= 1
        while col > 1:
            press('left')
            col -= 1 

    def getQuery(self):
        res :list[dict] = list()
        for item in self.rowManager.values():
            if item.isValid():
                res.append(item.getObj())
        print(res)
        self.setCellTracking(False)
        for row in self.rowManager:
            self.resetRow(row)
        self.setCellTracking(True)
        self.resetCellCursor(*self.coordinates)
        self.rowManager = dict()
        return res

    def setCellTracking(self, mode: bool) -> None:
        try:
            if not mode:
                self.Bill_Table.cellChanged.disconnect(self.handle_cell_change)  # type:ignore
                return
            self.Bill_Table.cellChanged.connect(self.handle_cell_change)  # type:ignore
        
        except TypeError:
            print(f"The Cell Tracking mode is already set to {mode}.")

    def resetRow(self, row: int) -> None:
        for col in range(8):
            self.setBillColumn(row, col, "")

    def handle_cell_change(self, row, col):
        # self.notification.message = f"Pressed ({row}, {col})"
        # self.notification.send(block=False)
        self.coordinates = row, col
        if col == QueryFormatterColumn.Id:
            # if row > 0 and row in self.rowManager:
            try:
                Item_ID = self.getText(row, col, int)
            except ValueError:
                QMessageBox.warning(self, "Invalid ID!", "The Item ID must be a number.")
                return
            # if Item_ID in self.
            self.rowManager[row] = Item(Item_ID)
            self.setBillColumn(row, QueryFormatterColumn.Sno, row + 1)
            press('tab')
            self.coordinates = row, col + 1
        elif col == QueryFormatterColumn.Name:
            name = self.getText(row, col)
            if name!= "":
                self.rowManager[row].name = name
                press('tab')
                self.coordinates = row, col + 1
        elif col == QueryFormatterColumn.CostPrice:
            try:
                Rate = self.getText(row, col, float)
                if Rate < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Invalid Price!", "Item Price must be a positive number.")
                return
            self.rowManager[row].cost_price = Rate
            press('tab')      
            self.coordinates = row, col + 1

        elif col == QueryFormatterColumn.SellingPrice:
            try:
                Rate = self.getText(row, col, float)
                if Rate < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Invalid Price!", "Item Price must be a positive number.")
                return
            self.rowManager[row].selling_price = Rate
            press('tab')   
            self.coordinates = row, col + 1   

        elif col == QueryFormatterColumn.Qnty:
            try:
                Quantity = self.getText(row, col, int)
                if Quantity < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Invalid Quantity!", "Item Quantity must be a positive number.")
                return
            self.rowManager[row].qnty = Quantity
            press(['tab']*2) 
            self.coordinates = row + 1, QueryFormatterColumn.Id   
    
    def loadStock(self, stock :Iterable):
        self.Bill_Table.setColumnHidden(QueryFormatterColumn.CostPrice, True)
        s = len(stock)
        self.Bill_Table.setRowCount(s)
        self.Bill_Table.setColumnCount(6)
        self.setCellTracking(False)
        print(stock[120])
        for row, item_id in enumerate(stock): #Item=> ID : Obj
            item :dict = stock[item_id]
            self.setBillColumn(row, QueryFormatterColumn.Sno, row + 1)
            self.setBillColumn(row, QueryFormatterColumn.Id, item.get('id'))
            self.setBillColumn(row, QueryFormatterColumn.Name, item.get('name'))
            self.setBillColumn(row, QueryFormatterColumn.CostPrice, item.get('cp'))
            self.setBillColumn(row, QueryFormatterColumn.SellingPrice, item.get('sp'))
            self.setBillColumn(row, QueryFormatterColumn.Qnty, item.get('qnty'))



def main():
    global app
    app = QApplication([])
    window = QueryFormatterGUI()
    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    main()