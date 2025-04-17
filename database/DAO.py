from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNerc():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query ="""SELECT *
                    FROM Nerc"""
            cursor.execute(query)

            for row in cursor:
                res.append(Nerc(row["id"], row["value"]))

            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getAllEvents(nerc):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
            return res
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM PowerOutages po
                        WHERE po.nerc_id = %s
                        ORDER BY po.date_event_began
            """# order perchè voglio poi verificare la differenza tra evento più recente e quello più vecchio -> devo avere tutto ordianto
            cursor.execute(query, (nerc.id,)) #ATTENTA, prendo nerc id per semplicita -> nerc è un oggetto

            for row in cursor:
                res.append(
                    Event(row["id"], row["event_type_id"],
                        row["tag_id"], row["area_id"],
                        row["nerc_id"], row["responsible_id"],
                        row["customers_affected"], row["date_event_began"],
                        row["date_event_finished"], row["demand_loss"]))

            cursor.close()
            cnx.close()
        return res