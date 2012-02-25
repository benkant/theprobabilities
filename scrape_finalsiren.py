from bs4 import BeautifulSoup
import sqlite3
import httplib

def get_final_siren_soup(season, page):
  conn = httplib.HTTPConnection("finalsiren.com")
  conn.request("GET", "/AFLPlayerStats.asp?SeasonID="+ str(season) + "&Sort=Rating%20Desc&Page="+ str(page))
  response = conn.getresponse()
  page = response.read()
  conn.close()

  soup = BeautifulSoup(page)

  return soup

def parse_player_row(player_row):
  columns = ['pos', 'num', 'player', 'mt', 'team', 'k', 'k_avg', 'h', 'h_avg', 'd', 'd_avg', 'm', 'm_avg', 'ho', 'ho_avg', 't', 't_avg', 'ff', 'fa', 'g', 'g_avg', 'b', 'sc', 'rat', 'avg']
  # create a dictionary of values
  player = {}
  i = 0
  for cell in player_row.find_all("td"):
    try:
      data = is_numeric(cell.text)
    except ValueError:
      data = cell.text

    player[columns[i]] = data
    i += 1

  return player

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

def insert_player(db_conn, player_dict, year):
  player_dict['year'] = year
  db_conn.execute("INSERT INTO final_siren VALUES ( :pos, :num, :player, :mt, :team, :k, :k_avg, :h, :h_avg, :d, :d_avg, :m, :m_avg, :ho, :ho_avg, :t, :t_avg, :ff, :fa, :g, :g_avg, :b, :sc, :rat, :avg, :year )", player_dict)
  db_conn.commit()
  print("Inserted "+ player_dict["player"] +", "+ player_dict["team"])

if __name__ == "__main__":
  YEAR = 2011
  PAGES = 13

  db_conn = sqlite3.connect("theprobabilities.db")

  # WARNING! @TODO NUKES DB
  db_conn.execute("DELETE FROM final_siren")

  for page in range(PAGES):
    page += 1

    soup = get_final_siren_soup(YEAR, page)

    stat_table = soup.find("table", { "class" : "playerstatssmall" })

    i = 0
    rows = stat_table.find_all("tr")
    for row in rows:
      # skip the header
      if i == 0:
        i += 1
        continue
      
      # skip the footer
      if i == len(rows) - 1:
        break

      player_dict = parse_player_row(row)

      insert_player(db_conn, player_dict, YEAR)

      i += 1

  # done
  db_conn.close()
