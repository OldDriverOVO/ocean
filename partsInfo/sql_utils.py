from django.db import connection

cursor = connection.cursor()


class SqlUtils():

    @classmethod
    def get_factory_parts_price(cls):
        sql = 'SELECT "parts".oem,"parts".cn_name,"pif".name,"partsInfo_factorypartsprice".price,"partsInfo_factorypartsprice".id,\
               "partsInfo_factorypartsprice".description,"partsInfo_factorypartsprice".llast_change_date,"a".first_name\
               FROM "partsInfo_factorypartsprice"\
               JOIN "partsInfo_parts" parts ON "partsInfo_factorypartsprice".oem_id = parts.oem\
               JOIN "partsInfo_factory" pif ON "partsInfo_factorypartsprice".factory_id_id = pif.id\
               LEFT JOIN auth_user a ON "partsInfo_factorypartsprice".last_change_user_id = a.id;'

        cursor.execute(sql)
        return cursor.fetchall()
