"""Helper Module for PyQt6 GUI"""

#Imports 
from enum import IntEnum
from pathlib import Path


#Global Declaration of Column Position
class BillTableColumn(IntEnum):
    """Bill Table Column Position"""
    Sno = 0
    Id = 1
    Name = 2
    Rate = 3
    Qnty = 4
    Disc_prcnt = 5
    Disc = 6
    Price = 7


if __name__ == '__main__':
    pass