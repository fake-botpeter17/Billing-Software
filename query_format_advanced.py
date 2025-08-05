import logging
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
from requests import post
from utils.server import get_Api
from utils.enums import QueryFormatterColumn
from utils.types import Item
from os import path
pathJoiner = path.join

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('query_formatter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QueryFormatterGUI(QMainWindow):
    Bill_Table : QTableWidget
    Query_Button :QPushButton
    Profile :QMenu
    def __init__(self) -> None:
        logger.info("Initializing QueryFormatterGUI")
        self.coordinates: tuple[int,int] = (0,0)
        self.rowManager :dict[int, Item] = dict()
        from notifypy import Notify
        super(QueryFormatterGUI, self).__init__()
        uic.loadUi(pathJoiner("Resources", "Query_Formatter.ui"), self)
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
            default_notification_icon=pathJoiner("Resources", "icofi.ico"),
            default_notification_application_name="BMS"
        )
        self.show()
        self.setup()
        press('tab')
        logger.info("QueryFormatterGUI initialization complete")
        
    def setup(self):
        logger.info("Setting up GUI components")
        self.setStyleSheet(open(pathJoiner("Resources", "Default.qss")).read())
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
        return dtype()

    def resetCellCursor(self, row, col):
        while row >= 0:
            press('up')
            row -= 1
        while col > 1:
            press('left')
            col -= 1 

    def getQuery(self):
        logger.info("Generating query from table data")
        res :list[dict] = list()
        for item in self.rowManager.values():
            if item.isValid():
                res.append(item.getObj())
        logger.info(f"Found {len(res)} valid items for query")
        self.setCellTracking(False)
        for row in self.rowManager:
            self.resetRow(row)
        self.resetCellCursor(*self.coordinates)
        self.setCellTracking(True)
        self.rowManager = dict()
        proceed = QMessageBox.question(self, "Proceed?",
                                       f"There are {len(res)} item/s detected. Upload to DB?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.Yes)
        from pyperclip import copy
        copy(str(res))
        if self.uploadItems(res) and (proceed == QMessageBox.StandardButton.Yes):
            reply = QMessageBox.question(self, "Upload Successfull",
            "The items were updated to the database successfully. Print Barcodes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                from BarcodeHelper import generatePDFs
                result = generatePDFs(res)
                if result:
                    r = QMessageBox.question(self,
                    "PDF Generated.",
                    f"The PDFs (Batch {result['batch']}) have been generated successfully! Open them?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No)

                    if r == QMessageBox.StandardButton.Yes:
                        from os import startfile
                        for file in result['paths']:
                            startfile(file)
                    else:
                        self.close()
            else:
                self.close()

    
    def uploadItems(self, items):
        logger.info(f"Attempting to upload {len(items)} items to database")
        try:
            res = post(url = get_Api() + "/updateStock", json=items)
            logger.info("Upload successful")
            return res.content
        except Exception as e:
            logger.error(f"Failed to upload items: {str(e)}\n\nItems: {items}")
            return None

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
        logger.debug(f"Cell changed at position ({row}, {col})")
        self.coordinates = row, col
        if col == QueryFormatterColumn.Id:
            # if row > 0 and row in self.rowManager:
            try:
                Item_ID = self.getText(row, col, int)
                logger.info(f"New item ID entered: {Item_ID} at row {row}")
            except ValueError:
                if self.getText(row,col) == "": return
                logger.warning(f"Invalid ID entered at row {row}")
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
                logger.debug(f"Setting name '{name}' for item at row {row}")
                self.rowManager[row].name = name
                press('tab')
                self.coordinates = row, col + 1
        elif col == QueryFormatterColumn.CostPrice:
            try:
                Rate = self.getText(row, col, float)
                if Rate < 0:
                    raise ValueError
                logger.debug(f"Setting cost price {Rate} for item at row {row}")
            except ValueError:
                if self.getText(row,col) == "": return
                logger.warning(f"Invalid cost price entered at row {row}")
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
                logger.debug(f"Setting selling price {Rate} for item at row {row}")
            except ValueError:
                if self.getText(row,col) == "": return
                logger.warning(f"Invalid selling price entered at row {row}")
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
                logger.debug(f"Setting quantity {Quantity} for item at row {row}")
            except ValueError:
                if self.getText(row,col) == "": return
                logger.warning(f"Invalid quantity entered at row {row}")
                QMessageBox.warning(self, "Invalid Quantity!", "Item Quantity must be a positive number.")
                return
            self.rowManager[row].qnty = Quantity
            press(['tab']*2) 
            self.coordinates = row + 1, QueryFormatterColumn.Id   
    
    def loadStock(self, stock :Iterable):
        self.Query_Button.setDisabled(True)
        self.Bill_Table.setColumnHidden(QueryFormatterColumn.CostPrice, True)
        s = len(stock)
        self.Bill_Table.setRowCount(s)
        self.Bill_Table.setColumnCount(6)
        self.Bill_Table.setColumnWidth(QueryFormatterColumn.Id, 250)
        self.setCellTracking(False)
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