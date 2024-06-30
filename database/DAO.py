from database.DB_connect import DBConnect
from model.match import Match


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getNodi(mese):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select m.MatchID as id, m.TeamHomeID as home , m.TeamAwayID as away, t.Name as homeName, t2.Name as awayName
                    from premierleague.matches m, premierleague.teams t, premierleague.teams t2 
                    where month (m.`Date`) = %s
                    and t.TeamID = m.TeamHomeID 
                    and t2.TeamID = m.TeamAwayID  """

        cursor.execute(query, (mese,))

        for row in cursor:
            result.append(Match(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(mese, minuti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select m.MatchId as m1, m2.MatchID as m2, count( a2.PlayerID) as count
                    from premierleague.actions a , premierleague.actions a2, premierleague.matches m , premierleague.matches m2 
                    where a.MatchID < a2.MatchID 
                    and a.MatchID = m.MatchID
                    and a2.MatchID = m2.MatchID 
                    and a.PlayerID = a2.PlayerID 
                    and a2.TimePlayed > %s
                    and a.TimePlayed > %s
                    and month (m.`Date`) = month (m2.`Date`)
                    and month (m.`Date`) = %s
                    group by m.MatchId, m2.MatchID """

        cursor.execute(query, (minuti,minuti, mese))

        for row in cursor:
            result.append([row["m1"], row["m2"], row["count"]])

        cursor.close()
        conn.close()
        return result

