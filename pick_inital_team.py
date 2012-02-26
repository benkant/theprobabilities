import sqlite3
import itertools

if __name__ == "__main__":
  RND = 0

  db_conn = sqlite3.connect("theprobabilities.db")

  Sd = {}
  Sm = {}
  Sr = {}
  Sf = {}

  cur = db_conn.cursor()
  cur.execute("SELECT id, price, previous_total FROM supercoach_2012 WHERE round = :rnd AND position = 'DEF' AND previous_total != 0", {"rnd": RND})

  for row in cur:
    

  '''
  i = 0
  for row in cur:
    i += 1
    Sd[row[0]] = row

  Sd_combinations = itertools.combinations(Sd, 9)
  
  i = 0
  for x in Sd_combinations:
    i += 1

    if i % 1000000 == 0:
      break
      #print i
    
    #print x
  '''

  db_conn.close()
