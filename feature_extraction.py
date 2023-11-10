
from zipfile import ZipFile
import csv
import pandas as pd

#Opens dataset reads data into array and removes therapist conversations
def open_file(file_name):
  f = open(file_name, "r")
  x = f.readlines()
  print(x)
  f.close
  for a in x:
    if(a[0] == 'T'):
      x.remove(a)
  print(len(x) )
  print(x)
  return x

#Gets word count from array of strings
def w_count(x):
  wcount = 0

  t_wcount = 0
  c_wcount=0

  t_sentences = 0
  c_sentences = 0

  for sentence in x:
    wcount = wcount + len(sentence.split()) - 1
    if sentence[0] == 'C':
      c_wcount= c_wcount + len(sentence.split()) - 1  
      c_sentences+=1
    else:
      t_wcount= t_wcount + len(sentence.split()) - 1  
      t_sentences+=1


  print(f"t_sentences: {t_sentences}")
  print(f"c_sentences: {c_sentences}")
  print(f"x: {len(x)}")

  wcount = wcount / len(x)
  c_wcount = c_wcount / c_sentences
  t_wcount = t_wcount / t_sentences

  print(wcount)
  print(f"Client Words/Turn: {c_wcount}")
  print(f"Therapist Words/Turn: {t_wcount}")
  return wcount

file_name = "content/DataSets.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

#Creation of empty arrays
id = [0] * 258
label = [0] * 258
Sent = [0] * 258
Length = [0] * 258

T_avg_Length = [0] * 258
C_avg_Length = [0] * 258

count = 0
#Opens csv file read filenames from file path may need to be changed
with open('DataSets/labeleddata/testlabels.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if(row["id"] == 'high_022' or row["id"] == 'low_023'):
        continue
      x = open_file("DataSets/"+row["id"])
      id[count] = row["id"]
      label[count] = row["label"]
      Length[count] = w_count(x)
      count = count + 1

#Opens empty csv and writes labeled data
with open('labeled.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'label','Sent','Length']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    count = 0
    writer.writeheader()
    for at in range(len(id)):
      writer.writerow({'id': id[count], 'label': label[count], 'Sent': Sent[count],'Length': Length[count]})
      count = count + 1