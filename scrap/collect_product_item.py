from scrap.tools import clearCatID
from scrap.collect_product_by_category import CollectProductByCategory
import applogger


class CollectProductItems():

    def __init__(self, db_connection, is_rowlimited, maxrow_allowed):
        self.db = db_connection
        self.cursor = self.db._cursor
        self.is_rowlimited = is_rowlimited
        self.maxrow_allowed = maxrow_allowed
  
        self.GetItems()

    def GetItems(self):
        logger = applogger.AppLoger('info_log')

        strSQL = ("select distinct(catid) from main_category mc "
                    " union "
                    "select distinct(catid) from sub_category sc ")

        self.cursor.execute(strSQL)

        _result = self.cursor.fetchall()
    
        for raw in _result:
            string_row = clearCatID(raw)
            CollectProductByCategory(string_row, self.db, self.is_rowlimited, self.maxrow_allowed)
    
        logger.info("Finished collecting product item")
        self.db.close()