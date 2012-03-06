import sqlite3
import itertools
from operator import itemgetter

# compute for data retrieved in round n
RND = 0

# salary cap constraint
SALARY_CAP = 10000000

# position constraint
Nd = 9
Nm = 8
Nr = 4
Nf = 9

# set of all players from each position ordered by value
Sd = []
Sm = []
Sr = []
Sf = []

# set of players chosen for the team from each position ordered by value
Td = []
Tm = []
Tr = []
Tf = []

# cost of T[d,m,r,f]
Cd = Cm = Cr = Cf = 0

def exceed_cap(player_set, test_idx):
  ''' returns true if the passed parameter added to the current total
  cost will exceed SALARY_CAP
  '''
  #print("Testing: "+ str(test_idx) +" "+ str(player_set[test_idx]["price"]) +" with "+ str(Cd + Cm + Cr + Cf))
  return Cd + Cm + Cr + Cf + player_set[test_idx]["price"] > SALARY_CAP

if __name__ == "__main__":

  db_conn = sqlite3.connect("theprobabilities.db")

  cur = db_conn.cursor()

  # populate S[d,m,r,f]
  for pos in ['DEF', 'MID', 'RUC', 'FWD']:
    # @TODO: is previous_total the correct field to use?
    cur.execute("SELECT id, price, previous_total FROM supercoach_2012 WHERE round = :rnd AND position = :pos AND previous_total != 0 ORDER BY previous_total DESC", {"pos": pos, "rnd": RND})

    for row in cur:
      player = {"id": row[0], "price": row[1], "value": row[2]}
      if pos == 'DEF':
        Sd.append(player)
      elif pos == 'MID':
        Sm.append(player)
      elif pos == 'RUC':
        Sr.append(player)
      elif pos == 'FWD':
        Sf.append(player)

  #### be greedy
  
  # keep going until all positions are filled
  done = False

  # next position
  next_pos = 'DEF'

  # last player picked from S[d,m,r,f]
  Pd = Pm = Pr = Pf = 0

  while not done:
    # Defence
    if next_pos == 'DEF':
      if len(Td) < Nd:
        # test next player doesn't blow the salary cap
        test_idx = Pd + 1
        while test_idx < len(Sd) and exceed_cap(Sd, test_idx):
          test_idx = test_idx + 1
          
        if not exceed_cap(Sd, test_idx):
          # we can afford this player, add them to the team
          Pd = test_idx
          Td.append(Sd[Pd]["id"])
          Cd = Cd + Sd[Pd]["price"]

      next_pos = 'MID'

    # Midfield
    elif next_pos == 'MID':
      if len(Tm) < Nm:
        test_idx = Pm + 1
        while test_idx < len(Sm) and exceed_cap(Sm, test_idx):
          test_idx = test_idx + 1

        if not exceed_cap(Sm, test_idx):
          # we can afford this player, add them to the team
          Pm = test_idx
          Tm.append(Sm[Pm]["id"])
          Cm = Cm + Sm[Pm]["price"]

      next_pos = 'RUC'

    # Ruck
    elif next_pos == 'RUC':
      if len(Tr) < Nr:
        test_idx = Pr + 1
        while test_idx < len(Sr) and exceed_cap(Sr, test_idx):
          test_idx = test_idx + 1

        if not exceed_cap(Sr, test_idx):
          # we can afford this player, add them to the team
          Pr = test_idx
          Tr.append(Sr[Pr]["id"])
          Cr = Cr + Sr[Pr]["price"]
        
      next_pos = 'FWD'

    # Forward
    elif next_pos == 'FWD': 
      if len(Tf) < Nf:
        test_idx = Pf + 1
        while test_idx < len(Sf) and exceed_cap(Sf, test_idx):
          test_idx = test_idx + 1

        if not exceed_cap(Sf, test_idx):
          # we can afford this player, add them to the team
          Pf = test_idx
          Tf.append(Sf[Pf]["id"])
          Cf = Cf + Sf[Pf]["price"]
  
      next_pos = 'DEF'
    
    done = (len(Td) == Nd) and (len(Tm) == Nm) and (len(Tr) == Nr) and (len(Tf) == Nf)

  # output results
  print("Defence: "+ str(Cd))
  print(Td)

  print("Midfield: "+ str(Cm))
  print(Tm)

  print("Ruck: "+ str(Cr))
  print(Tr)
 
  print("Forward: "+ str(Cf))
  print(Tf)

  print("Total cost: " + str(Cd + Cm + Cr + Cf))
  
  db_conn.close()
