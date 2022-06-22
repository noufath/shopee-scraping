from multiprocessing.pool import ApplyResult
from string import Template
from flask import jsonify
import psycopg2
import requests
from db_config.db_connect import Db_Connect
import json
from scrap.tools import TextSanitize
from string import Template
import applogger
import sys
import urllib.request

class CollectProductByCategory():

    def __init__(self, _catid, db_connection, is_rowlimited, maxrow_allowed):
        self._catid = _catid
        self.url = ("https://shopee.co.id/api/v4/search/search_items?by=relevancy&limit=100"
            "&match_id={}&newest=0&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2").format(self._catid)
        self.db = db_connection

        self.is_rowlimited = is_rowlimited
        self.maxrow_allowed = maxrow_allowed

        self.SaveToDatabase(data=self.CollectProductCategory(), isRowLimited=self.is_rowlimited, maxrow_allowed=self.maxrow_allowed)
          

    def CollectProductCategory(self):
        
        UA = ("PostmanRuntime/7.29.0")

        header = {"User-Agent": UA,
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": "REC_T_ID=32aa9e74-00e4-11ec-8056-2cea7f902ae0; SPC_F=lH4ay2ZgY72WvYxBJDUImt17VLTgcHZ6; SPC_R_T_ID=OneXSIrn01CjYXxeCEVC0AyS7xfiBOAWIMq3cxUcxP1+6z7mSP1vyvD3LMx0cohM+O3bcPOMju6xYnjBnCLPVh9EXQXIaAebw4uyqFmavHzW1aQwZbXpObdXzYX5kCS3+hEfcKZoHCl5wEgRw5R4j0xXsfz7a/c4kZCpwpShgxE=; SPC_R_T_IV=N0t1bHdKWGxmd1djZTB3Tg==; SPC_SI=8JWpYgAAAABiNzhHTUtVcL6wqAAAAAAAZ1R4WmN1cEU=; SPC_T_ID=OneXSIrn01CjYXxeCEVC0AyS7xfiBOAWIMq3cxUcxP1+6z7mSP1vyvD3LMx0cohM+O3bcPOMju6xYnjBnCLPVh9EXQXIaAebw4uyqFmavHzW1aQwZbXpObdXzYX5kCS3+hEfcKZoHCl5wEgRw5R4j0xXsfz7a/c4kZCpwpShgxE=; SPC_T_IV=N0t1bHdKWGxmd1djZTB3Tg=="
        }
        test_request = requests.get(self.url, headers=header)

        
        if test_request.status_code == 200:
            logger = applogger.AppLoger('info_log')


            resp = requests.get(self.url, headers=header).content.decode("utf-8")

            _source = json.loads(resp)['items']

          
            
            list_rec = list()

            logger.info("Collecting Item by Category:")
       
           
            for data in _source:
               
                items = data['item_basic']


                # change null value to 0
                for key, val in items.items():
                    if val == 'null':
                        items.update({key: 0})

                    if val == "None":
                        items.update({key: None})
                
                    # None for jsonb data type
                    if key == 'label_ids' and val == None:
                        items.update({key: json.dumps(None)})

                    # change categoryid value using _catid's search parameter, because data got from scrap not related to master category
                    if key == 'catid':
                        items.update({key: self._catid})
            
                # create list record
                list_rec += (items['itemid'], items['shopid'], TextSanitize(items['name']), \
                    TextSanitize(items['label_ids']), items['image'], TextSanitize(items['images']), \
                    items['currency'], items['stock'], items['status'], \
                    items['ctime'], items['sold'], items['historical_sold'], \
                    items['liked'], items['liked_count'], TextSanitize(items['view_count']), \
                    TextSanitize(items['catid']), TextSanitize(items['brand']), items['cmt_count'], items['flag'], \
                    items['cb_option'], items['item_status'], items['price'], \
                    items['price_min'], items['price_max'], items['price_min_before_discount'], \
                    items['price_max_before_discount'], TextSanitize(items['hidden_price_display']), \
                    items['price_before_discount'], items['has_lowest_price_guarantee'], \
                    items['show_discount'], items['raw_discount'], TextSanitize(items['discount']), \
                    items['is_category_failed'], str(items['size_chart']),\
                    TextSanitize(str(items['item_rating'])), items['item_type'], \
                    items['reference_item_id'], items['transparent_background_image'], 
                    items['is_adult'], items['badge_icon_type'], items['shopee_verified'], \
                    items['is_official_shop'], items['show_official_shop_label'], items['show_shopee_verified_label'], \
                    items['show_official_shop_label_in_title'], items['is_cc_installment_payment_eligible'], \
                    items['is_non_cc_installment_payment_eligible'], TextSanitize(items['coin_earn_label']), items['show_free_shipping'], \
                    TextSanitize(items['preview_info']), TextSanitize(items['coin_info']), TextSanitize(items['exclusive_price_info']), TextSanitize(items['bundle_deal_id']), \
                    items['can_use_bundle_deal'], TextSanitize(items['bundle_deal_info']), TextSanitize(items['is_group_buy_item']), \
                    TextSanitize(items['has_group_buy_stock']), TextSanitize(items['group_buy_info']), items['welcome_package_type'], \
                    TextSanitize(items['welcome_package_info']), TextSanitize(items['add_on_deal_info']), items['can_use_wholesale'], \
                    items['is_preferred_plus_seller'], TextSanitize(items['shop_location']), items['has_model_with_available_shopee_stock'], \
                    TextSanitize(items['voucher_info']), items['can_use_cod'], items['is_on_flash_sale'], TextSanitize(items['spl_installment_tenure']), \
                    TextSanitize(items['is_live_streaming_price']), items['is_mart'], TextSanitize(items['pack_size'])),
          
            return list_rec
        else:
            
            logger = applogger.AppLoger('error_log')

            logger.error('Error server respon {}'.format(test_request.status_code))
            sys.exit(0)
      
        

    def SaveToDatabase(self, data, isRowLimited, maxrow_allowed):
        logger = applogger.AppLoger('info_log')
        cursor = self.db._cursor

        fields = ["itemid", "shopid", "name", "label_ids", "image", "images", "currency", "stock", "status", "ctime", "sold", "historical_sold", 
                "liked", "liked_count", "view_count", "catid", "brand", "cmt_count", "flag", "cb_option", "item_status", "price", "price_min",
                "price_max", "price_min_before_discount", "price_max_before_discount", "hidden_price_display", "price_before_discount",
                "has_lowest_price_guarantee", "show_discount", "raw_discount", "discount", "is_category_failed", "size_chart",
                "item_rating", "item_type", "reference_item_id", "transparent_background_image",
                "is_adult", "badge_icon_type", "shopee_verified", "is_official_shop", "show_official_shop_label", "show_shopee_verified_label",
                "show_official_shop_label_in_title", "is_cc_installment_payment_eligible", "is_non_cc_installment_payment_eligible", "coin_earn_label",
                "show_free_shipping", "preview_info", "coin_info",  "exclusive_price_info",  "bundle_deal_id",  "can_use_bundle_deal", "bundle_deal_info",
                "is_group_buy_item", "has_group_buy_stock", "group_buy_info", "welcome_package_type", "welcome_package_info", "add_on_deal_info", "can_use_wholesale",
                "is_preferred_plus_seller", "shop_location", "has_model_with_available_shopee_stock", "voucher_info", "can_use_cod", "is_on_flash_sale", "spl_installment_tenure",
                "is_live_streaming_price", "is_mart", "pack_size"]
        
        col = ''
        col_excluded = ''
        i = 0

        for field_name in fields:
            i += 1
            
            if i < len(fields):
                col += field_name + ", "
                col_excluded += field_name + "=EXCLUDED." + field_name + ", "
            else:
                col += field_name
                col_excluded += field_name + "=EXCLUDED." + field_name 
        
        Template_SQL = ("INSERT INTO item($fields_raw) VALUES $list_values"
            " ON CONFLICT (itemid) DO UPDATE SET $fields_excluded;\n"
        )

        # change to use mogrify for more speed saving

        '''
        for rec in data:

            strSQL = Template(Template_SQL).substitute(
                fields_raw=col, 
                list_values=rec,
                fields_excluded=col_excluded
            )

            
            self.db.execute(strSQL)
            
            logger.info('Saving data kode_produk: {0} - id_toko : {1} - nama_barang: {2}'.format(rec[0], rec[1], rec[2]))
        '''

        if data != []:
            format_string = '(' + ','.join(['%s', ]*len(data[0])) + ')\n'
            args_string = ','.join(cursor.mogrify(format_string, x).decode('utf-8') for x in data)

            strSQL = Template(Template_SQL).substitute(
                fields_raw=col, 
                list_values=args_string,
                fields_excluded=col_excluded
            )

            if isRowLimited:

                rows = self.row_count()

                if rows < maxrow_allowed:
                    try:
                        self.db.execute(strSQL)

                    except (Exception, psycopg2.DatabaseError) as error:
                    
                        logger.info("Error %s" % error)
                        self.db._connection.rollback()
                        cursor.close()

                    logger.info("Finished Collecting product item in category: {}".format(self._catid))
                    return 1
                else:
                    logger.info("row exceeded maximum row allowed")
                    sys.exit()

            else:
                try:
                    self.db.execute(strSQL)

                except (Exception, psycopg2.DatabaseError) as error:
                        
                    logger.info("Error %s" % error)
                    self.db._connection.rollback()
                    cursor.close()

                
                logger.info("Finished Collecting product item in category: {}".format(self._catid))
                return 

                    

    def row_count(self):
        # count row number
        strSQL = "SELECT reltuples::bigint AS estimate FROM pg_class WHERE oid = 'public.item'::regclass;"
        
        self.db.execute(strSQL)

        cursor = self.db._cursor
        row_numb = cursor.fetchall()

        return row_numb[0][0]