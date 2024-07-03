from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessioni import Connessione


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects"
        cursor.execute(query)

        for row in cursor:
            # result.append(ArtObject(row["object_id"], row["classification"], row["continent"], row["country"],
            #                         row["curator_approved"], row["dated"], row["department"], row["medium"],
            #                         row["nationality"], row["object_name"], row["restricted"], row["rights_type"],
            #                         row["role"], row["room"], row["style"], row["title"]
            #                         ))
            result.append(ArtObject(**row))  # basta fare così: i nomi degli attributi però devono essere
            # gli stessi del database

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(v1: ArtObject, v2: ArtObject):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(*)
                    from exhibition_objects eo, exhibition_objects eo2
                    where eo.exhibition_id = eo2.exhibition_id
                    and eo.object_id < eo2.object_id
                    and eo.object_id = %s
                    and eo2.object_id = %s"""
        cursor.execute(query, (v1.object_id, v2.object_id,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select eo.object_id as v1, eo2.object_id as v2, count(*) as peso
                    from exhibition_objects eo, exhibition_objects eo2  
                    where eo.exhibition_id = eo2.exhibition_id 
                    and eo.object_id < eo2.object_id 
                    group by eo.object_id, eo2.object_id 
                    order by peso desc"""
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row["v1"]],
                                      idMap[row["v2"]],
                                      row["peso"]))
        cursor.close()
        conn.close()
        return result
