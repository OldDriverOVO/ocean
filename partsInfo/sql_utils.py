from django.db import connection

cursor = connection.cursor()


class SqlUtils():

    @classmethod
    def get_factory_parts_price(cls, oem=None, factory_id=None, factory_q=None, parts_q=None):

        sql = 'SELECT "parts".oem,"parts".cn_name,"pif".name,"partsInfo_factorypartsprice".price,"partsInfo_factorypartsprice".id,\
               "partsInfo_factorypartsprice".description,"partsInfo_factorypartsprice".llast_change_date,"a".first_name,pif.id\
               FROM "partsInfo_factorypartsprice"\
               JOIN "partsInfo_parts" parts ON "partsInfo_factorypartsprice".oem_id = parts.oem\
               JOIN "partsInfo_factory" pif ON "partsInfo_factorypartsprice".factory_id_id = pif.id\
               LEFT JOIN auth_user a ON "partsInfo_factorypartsprice".last_change_user_id = a.id'

        if oem and not factory_q:
            sql += " WHERE parts.oem = '" + oem + "';"
        elif oem and factory_q:
            sql += " WHERE parts.oem = '" + oem + "' AND pif.name LIKE '%" + factory_q + "%';"
        elif factory_id and not parts_q:
            sql += " WHERE pif.id = " + factory_id + ";"
        elif factory_id and parts_q:
            sql += " WHERE pif.id = " + factory_id + " AND (parts.oem LIKE '%" + parts_q + "%' OR parts.cn_name LIKE '%" + parts_q + "%');"
        elif factory_q and parts_q:
            sql += " WHERE pif.name LIKE '%" + factory_q + "%' AND (parts.oem LIKE '%" + parts_q + "%' OR parts.cn_name LIKE '%" + parts_q + "%');"
        elif factory_q and not parts_q:
            sql += " WHERE pif.name LIKE '%" + factory_q + "%';"
        elif parts_q and not factory_q:
            sql += " WHERE parts.oem LIKE '%" + parts_q + "%' OR parts.cn_name LIKE '%" + parts_q + "%';"
        else:
            sql += ';'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def get_customer_parts_price(cls, oem=None, customer_id=None,customer_q=None, parts_q=None):
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

        if oem and not customer_q:
            sql += " WHERE parts.oem = '" + oem + "';"
        elif oem and customer_q:
            sql += " WHERE parts.oem = '" + oem + "' AND pic.nick_name LIKE '%" + customer_q + "%';"
        elif customer_id and not parts_q:
            sql += " WHERE pic.id = " + customer_id + ";"
        elif customer_id and parts_q:
            sql += " WHERE pic.id = " + customer_id + " AND (parts.oem LIKE '%" + parts_q + "%' OR parts.cn_name LIKE '%" + parts_q + "%');"
        elif customer_q and parts_q:
            sql += " WHERE pic.nick_name LIKE '%" + customer_q + "%' AND (parts.oem LIKE '%" + parts_q + "%' OR parts.cn_name LIKE '%" + parts_q + "%');"
        elif customer_q and not parts_q:
            sql += " WHERE pic.nick_name LIKE '%" + customer_q + "%';"
        elif parts_q and not customer_q:
            sql += " WHERE parts.oem LIKE '%" + parts_q + "%' OR parts.cn_name LIKE '%" + parts_q + "%';"
        else:
            sql += ';'
        cursor.execute(sql)
        return cursor.fetchall()
