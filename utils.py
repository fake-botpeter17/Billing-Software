from collections.abc import Generator
from requests import Response, Timeout, get
from datetime import datetime, date
from threading import Thread
from api import get_Api

class User:
    """
    Stores the current user's info
    """
    __Name :str = str()
    __Designation :str = str()
    __UID :str = str()
    __Logging_Out :bool = False

    @classmethod
    def update(cls  : "User", uid : str, **kwargs : dict[str, str]) -> None:
        """Sets the current user info"""
        cls.__Name :str = kwargs.get("name")
        cls.__Designation :str = kwargs.get("designation")
        cls.__UID :str = uid

    @classmethod
    def getNameDesignation(cls : "User") -> tuple[str, str]:
        """Returns the current user's name and designation"""
        return cls.__Name, cls.__Designation

    @classmethod
    def isAdmin(cls : "User") -> bool:
        '''Checks if the current user is an Admin'''
        return cls.__Designation.casefold() == "Admin".casefold()

    @classmethod
    def isLoggingOut(cls : "User") -> bool:
        """Checks if the current user is logging out"""
        return cls.__Logging_Out
    
    @classmethod
    def toggleLoggingOut(cls : "User") -> None:
        """Toggles the logging out status of the current user"""
        cls.__Logging_Out = True
        cls.resetUser()

    @classmethod
    def resetUser(cls : "User") -> None:
        """Resets the current user's info"""
        cls.__Name :str = str()
        cls.__Designation :str = str()
        cls.__UID :str = str()
        cls.__Logging_Out :bool = False
        
class Bill_:
    __Bill_No_Gen :Generator
    __Bill_No :int = int()
    __Items :dict = dict()
    __Cart :dict = dict()   #{id:row}
    __Row_Lookup :dict = dict()  #{row:id}

    @staticmethod
    def getItems():
        try:
            req : Response= get(get_Api(testing=False) + "//get_stock", timeout=15)
            items_cache = req.json()
        except Timeout:
            return
        if not items_cache:
            return {}
        tmp = dict()
        for item in items_cache:
            tmp[item["id"]] = item
        return tmp

    @classmethod
    def contains(cls, item_id: int) -> bool:
        """Checks if the given item ID is in the cart"""
        return item_id in cls.__Cart

    @staticmethod
    def __Bill_Number(testing :bool = False) -> Generator:
        """Retreives the latest Bill Number"""
        Latest_Bill : int | None = get(f"{get_Api(testing)}/getLastBillNo").json()
        if not Latest_Bill:
            Latest_Bill = 10001
        for Bill_Number in range(Latest_Bill + 1, 100000):
            yield Bill_Number

    @staticmethod
    def Get_Date() -> str:
        """Returns the current date."""
        return date.today().strftime("%B %d, %Y")

    @staticmethod
    def Get_Time() -> str:
        """Returns the current time."""
        return datetime.now().time().strftime("%H:%M:%S")
    
    @classmethod
    def Init(cls : "Bill_") -> None:
        """Initializes the bill"""
        cls.__Bill_No_Gen = cls.__Bill_Number()
        cls.__Bill_No = next(cls.__Bill_No_Gen)
        Thread(target=cls.Items_Cacher).start()

    @classmethod
    def Get_Bill_No(cls : "Bill_") -> int:
        """Returns the current bill number"""
        return cls.__Bill_No

    @classmethod
    def Get_Item(cls : "Bill_", Item_ID :int) -> dict[int | str : int | str]:
        return cls.__Items.get(Item_ID)

    @classmethod
    def Increment_Bill_No(cls : "Bill_") -> None:
        """Increments the bill number"""
        cls.__Bill_No = next(cls.__Bill_No_Gen)

    @classmethod
    def getCartItems(cls : "Bill_"):
        return cls.__Cart.keys()

    @classmethod
    def getRowNumber(cls : "Bill_", Item_ID :int):
        return cls.__Cart.get(Item_ID)

    @classmethod
    def isEmpty(cls : "Bill_") -> bool:
        return len(cls.__Cart) == 0

    @classmethod
    def remove_row_item(cls : "Bill_", row_number : int) -> None:
        item = cls.__Row_Lookup.get(row_number)
        if item in cls.__Cart:
            del cls.__Cart[item]
        cls.__Row_Lookup.pop(row_number)

    @classmethod
    def isDuplicateRow(cls : "Bill_", row_number : int) -> bool:
        return row_number in cls.__Row_Lookup

    @classmethod
    def addItem(cls : "Bill_", item_id : int, row :int) -> None:
        cls.__Cart[item_id] = row
        cls.__Row_Lookup[row] = item_id

    @classmethod
    def getCart(cls : "Bill_") -> dict[int, int | str]:
        return cls.__Cart   

    @classmethod
    def nextBillPrep(cls : "Bill_"):
        cls.__Cart.clear()
        cls.__Row_Lookup.clear()
        cls.Increment_Bill_No()

    # @classmethod
    # def remove_row_item(cls : "Bill_", row_number : int) -> None:
    #     if cls.__Row_Lookup(row_number) in cls.__Cart:
    #         del cls.__Cart[cls.get_row_item(row_number)]
    #     ...

    # @classmethod
    # def get_row_item(cls: "Bill_", row_number: int) -> int:
    #     return cls.__Row_Lookup.get(row_number)

    @classmethod
    def Items_Cacher(cls : "Bill_") -> None:
        """Caches the items"""
        try:
            req : Response= get(get_Api(testing=False) + "//get_items", timeout=15)
            items_cache = req.json()
        except Timeout:
            return
        if not items_cache:
            return
        for item in items_cache:
            cls.__Items[item["id"]] = item