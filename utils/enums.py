#Imports 
from enum import IntEnum

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

class QueryFormatterColumn(IntEnum):
    """Query Formatter Table Column Position"""
    Sno = 0
    Id = 1
    Name = 2
    CostPrice = 3
    SellingPrice = 4
    Qnty = 5
