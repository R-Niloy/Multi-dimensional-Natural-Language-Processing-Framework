
from zipfile import ZipFile
import csv
import pandas as pd
#NOTe  TO SELF RESEARCH BASIC TRANSCIPT based CLASSIFCIATION MODELS FOR OTHER TOPICS FOR MORE FEATURE IDEAS.


#Opens dataset reads data into array and removes therapist conversations
def open_file(file_name):
  f = open(file_name, "r")
  x = f.readlines()
  f.close
  for a in x:
    if(a[0] == 'T'):
      x.remove(a)
  return x

#Opens dataset reads data all data into array
def open_file_allLines(file_name):
  f = open(file_name, "r")
  y = f.readlines()     #Y will have the whole transcript as an array
  f.close
  return y

#Gets Average words/turn Therapist
def w_countT(y):
  wcount = 0

  t_wcount = 0
  t_sentences = 0

  for sentence in y:
    if sentence[0] == 'T':
      t_wcount= t_wcount + len(sentence.split()) - 1  
      t_sentences+=1

  print(f"t_sentences: {t_sentences}")

  t_wcount = t_wcount / t_sentences

  print(f"Therapist Words/Turn: {t_wcount}")
  return t_wcount

#Gets Average words/turn Client
def w_countC(y):
  c_wcount = 0
  c_sentences = 0

  for sentence in y:
    if sentence[0] == 'C':
      c_wcount= c_wcount + len(sentence.split()) - 1  
      c_sentences+=1

  print(f"c_sentences: {c_sentences}")

  c_wcount = c_wcount / c_sentences

  print(c_wcount)
  print(f"Client Words/Turn: {c_wcount}")
  return c_wcount

#Returns turns taken by therapist
def T_turns(y):
  t_sentences = 0

  for sentence in y:
    if sentence[0] == 'T':
      t_sentences+=1

  print(f"t_sentences: {t_sentences}")
  return t_sentences

#Returns turns taken by Client
def C_turns(y):
  c_sentences = 0

  for sentence in y:
    if sentence[0] == 'C':
      c_sentences+=1

  print(f"t_sentences: {c_sentences}")
  return c_sentences

file_name = "content/DataSets.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

#Creation of empty arrays
id = [0] * 257
label = [0] * 257
T_avg_Length = [0] * 257
C_avg_Length = [0] * 257
T_turns_arr = [0] * 257
C_turns_arr = [0] * 257

count = 0
#Opens csv file read filenames from file path may need to be changed
with open('DataSets/labeleddata/testlabels.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if(row["id"] == 'high_022' or row["id"] == 'low_023'):
        continue
      x = open_file("DataSets/"+row["id"])
      y = open_file_allLines("DataSets/"+row["id"])
      id[count] = row["id"]
      label[count] = row["label"]
      T_avg_Length[count] = w_countT(y)
      C_avg_Length[count] = w_countC(y)
      T_turns_arr[count] = T_turns(y)
      C_turns_arr[count] = C_turns(y)
      count = count + 1

count = 0
print(T_avg_Length)
#Opens empty csv and writes labeled data
with open('labeled.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'label', 'T_Words/Turn', 'C_Words/Turn', 'T_Turns', 'C_Turns']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    count = 0
    writer.writeheader()
    for at in range(len(id)):
      writer.writerow({'id': id[count], 'label': label[count], 'T_Words/Turn': T_avg_Length[count], 'C_Words/Turn': C_avg_Length[count], 'T_Turns': T_turns_arr[count], 'C_Turns': C_turns_arr[count]})
      count = count + 1
