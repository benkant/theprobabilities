from bs4 import BeautifulSoup
import sqlite3
import httplib

def is_numeric(lit):
  'Return value of numeric literal string or ValueError exception'
 
  # Handle '0'
  if lit == '0': return 0
  # Hex/Binary
  litneg = lit[1:] if lit[0] == '-' else lit
  if litneg[0] == '0':
    if litneg[1] in 'xX':
      return int(lit,16)
    elif litneg[1] in 'bB':
      return int(lit,2)
    else:
      try:
        return int(lit,8)
      except ValueError:
        pass
 
  # Int/Float/Complex
  try:
    return int(lit)
  except ValueError:
    pass
  try:
    return float(lit)
  except ValueError:
    pass
  return complex(lit)

def get_footywire_soup(rnd):
  conn = httplib.HTTPConnection("www.footywire.com")
  conn.request("GET", "/afl/footy/supercoach_round?round="+ str(rnd) +"&p=&s=T")
  response = conn.getresponse()
  page = response.read()
  conn.close()

  soup = BeautifulSoup(page)

  return soup

def parse_player_row(player_row):
  columns = ['rank', 'player', 'team', 'price', 'score', 'value']
  # create a dictionary of values
  player = {}
  i = 0
  for cell in player_row.find_all("td"):
    try:
      data = is_numeric(cell.text)
    except ValueError:
      data = cell.text.replace("(Injured)", "").replace("(Suspended)", "").rstrip()

    player[columns[i]] = data
    i += 1

  return player

def insert_player(db_conn, player_dict, rnd):
  player_dict['round'] = rnd
  db_conn.execute("INSERT INTO footywire_sc_2011 VALUES ( :player, :team, :score, :round)", player_dict)
  db_conn.commit()
  print("Inserted "+ player_dict["player"] +", "+ player_dict["team"])

if __name__ == "__main__":
  ROUNDS = 24
  db_conn = sqlite3.connect("theprobabilities.db")

  # WARNING! @TODO NUKES DB
  db_conn.execute("DELETE FROM footywire_sc_2011")

  for rnd in range(ROUNDS):
    rnd += 1

    soup = get_footywire_soup(rnd)

    stat_table = soup.find_all("td", { "class" : "tabbdr" })[0]
    stat_td = stat_table.find_next_siblings("td")

    i = 0
    rows = stat_td[0].find_all("tr")
    for row in rows:
      # skip the header
      if i == 0:
        i += 1
        continue
      
      player_dict = parse_player_row(row)

      insert_player(db_conn, player_dict, rnd)

      i += 1

  # done
  db_conn.close()


