import json
import sqlite3
import httplib

def insert_player(db_conn, player_dict, rnd, pos):
  player_dict['round'] = rnd
  player_dict['position'] = pos
  db_conn.execute("INSERT INTO supercoach_2012 VALUES ( :id, :first_name, :last_name, :team_id, :price, :cdid, :previous_games, :previous_average, :previous_total, :current_price, :round, :position )", player_dict)
  db_conn.commit()
  print("Inserted "+ player_dict["first_name"] +" "+ player_dict["last_name"])

def get_players(pos):
  conn = httplib.HTTPConnection("supercoach.heraldsun.com.au")
  conn.request("GET", "/service/player_lookup/position_lookup?position="+ pos)
  players = json.loads(conn.getresponse().read())

  return players

if __name__ == "__main__":
  RND = 0

  db_conn = sqlite3.connect("theprobabilities.db")

  # WARNING! @TODO NUKES DB
  db_conn.execute("DELETE FROM supercoach_2012")

  for pos in ['DEF', 'MID', 'RUC', 'FWD']:
    for player in get_players(pos):
      insert_player(db_conn, player, RND, pos)

  # done
  db_conn.close()

