import pandas as pd

if __name__ == "__main__":

  file_name = "DT_Data_CakeVsMuffin_v012_TEST.csv"
  data = pd.read_csv(file_name)

  for index, row in data.iterrows():
    
   if row[Flour] < 5.997999999999999:
      if row[Oils] < 4.196000000000001:
         if row[Flour] < 3.806:
            if row[Proteins] < 3.702:
               return Muffin
            else:  # if row['Proteins'] >= ('Proteins', 3.702)
               return CupCake
         else:  # if row['Flour'] >= ('Flour', 3.806)
            return Muffin
      else:  # if row['Oils'] >= ('Oils', 4.196000000000001)
         return CupCake
   else:  # if row['Flour'] >= ('Flour', 5.997999999999999)
      if row[Oils] < 10.574000000000002:
         return Muffin
      else:  # if row['Oils'] >= ('Oils', 10.574000000000002)
         if row[Flour] < 9.87:
            return CupCake
         else:  # if row['Flour'] >= ('Flour', 9.87)
            if row[Proteins] < 2.8:
               return Muffin
            else:  # if row['Proteins'] >= ('Proteins', 2.8)
               return Muffin
