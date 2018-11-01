from django.db import connection

cursor = connection.cursor()


class SqlUtils():

    @classmethod
    def get_factory_parts_price(cls, oem=None, factory_id=None):
        sql = 'SELECT "parts".oem,"parts".cn_name,"pif".name,"partsInfo_factorypartsprice".price,"partsInfo_factorypartsprice".id,\
               "partsInfo_factorypartsprice".description,"partsInfo_factorypartsprice".llast_change_date,"a".first_name,pif.id\
               FROM "partsInfo_factorypartsprice"\
               JOIN "partsInfo_parts" parts ON "partsInfo_factorypartsprice".oem_id = parts.oem\
               JOIN "partsInfo_factory" pif ON "partsInfo_factorypartsprice".factory_id_id = pif.id\
               LEFT JOIN auth_user a ON "partsInfo_factorypartsprice".last_change_user_id = a.id'

        if oem:
            sql += " WHERE parts.oem = '" + oem + "';"
        elif factory_id:
            sql += " WHERE pif.id = " + factory_id + ";"
        else:
            sql += ';'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def get_customer_parts_price(cls, oem=None, customer_id=None):
        sql = 'SELECT "parts".oem,\
                    "parts".cn_name,\
                    "pic".nick_name,\
                    "partsInfo_customerpartsprice".price,\
                    "partsInfo_customerpartsprice".id,\
                    "partsInfo_customerpartsprice".description,\
                    "partsInfo_customerpartsprice".last_change_date,\
                    "a".first_name,\
                     pic.id\
            FROM "partsInfo_customerpartsprice"\
            JOIN "partsInfo_parts" parts ON "partsInfo_customerpartsprice".oem_id = parts.oem\
            JOIN "partsInfo_customer" pic ON "partsInfo_customerpartsprice".customer_id_id = pic.id\
            JOIN auth_user a ON "partsInfo_customerpartsprice".last_change_user_id = a.id'

        if oem:
            sql += " WHERE parts.oem = '" + oem + "';"
        elif customer_id:
            sql += " WHERE pic.id = " + customer_id + ";"
        else:
            sql += ';'
        cursor.execute(sql)
        return cursor.fetchall()
