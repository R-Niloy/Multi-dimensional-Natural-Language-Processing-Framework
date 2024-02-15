
from zipfile import ZipFile
import csv
import numpy as np
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
def meanw_countT(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'T':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(df)
  print(f"Therapist Words/Turn: {df['Word Count'].mean()}")
  return (df['Word Count'].mean())

def stdw_countT(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'T':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(df)
  print(f"STD Therapist Words/Turn: {df['Word Count'].std()}")
  return (df['Word Count'].std())

def skeww_countT(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'T':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(df)
  print(f"skew Therapist Words/Turn: {df['Word Count'].skew()}")
  return (df['Word Count'].skew())

def kurtw_countT(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'T':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(df)
  print(f"kurt Therapist Words/Turn: {df['Word Count'].kurt()}")
  return (df['Word Count'].kurt())

#Gets Average words/turn Client
def meanw_countC(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'C':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(f"Client Words/Turn: {df['Word Count'].mean()}")
  return df['Word Count'].mean()

def stdw_countC(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'C':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(f"std Client Words/Turn: {df['Word Count'].std()}")
  return df['Word Count'].std()

def skeww_countC(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'C':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(f"skew Client Words/Turn: {df['Word Count'].skew()}")
  return df['Word Count'].skew()

def kurtw_countC(y):
  df = pd.DataFrame(columns = ['Word Count'])
  for sentence in y:
    if sentence[0] == 'C':
      df.loc[len(df)] = [len(sentence.split()) - 1]
  print(f"kurt Client Words/Turn: {df['Word Count'].kurt()}")
  return df['Word Count'].kurt()

#Returns turns taken by therapist
def T_turns(y):
  t_sentences = 0

  for sentence in y:
    if sentence[0] == 'T':
      t_sentences+=1

  print(f"t_sentences: {t_sentences}")
  return t_sentences
#returns turns taken by client
def C_turns(y):
  c_sentences = 0

  for sentence in y:
    if sentence[0] == 'C':
      c_sentences+=1

  print(f"t_sentences: {c_sentences}")
  return c_sentences

#returns ratio of turns T/C 
def ratio_turns(y):
  c_sentences = 0
  t_sentences = 0

  for sentence in y:
    if sentence[0] == 'C':
      c_sentences+=1
    else:
      t_sentences+=1

  ratio = t_sentences/c_sentences
  print(f"t_sentences: {c_sentences}")
  return ratio

#ratio of WPT_T  /  WPT_C
def ratio_words(y):
  ratio = meanw_countT(y)/meanw_countC(y)
  return ratio


file_name = "content/DataSets.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

#Creation of empty arrays
id = [0] * 257
label = [0] * 257
T_avg_Length = [0] * 257
T_std_Length = [0] * 257
T_skew_Length = [0] * 257
T_kurt_Length = [0] * 257


C_avg_Length = [0] * 257
C_std_Length = [0] * 257
C_skew_Length = [0] * 257
C_kurt_Length = [0] * 257

T_turns_arr = [0] * 257
C_turns_arr = [0] * 257
ratio_turns_arr = [0] * 257
ratio_words_arr = [0] * 257

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
      T_avg_Length[count] = meanw_countT(y)
      T_std_Length[count] = stdw_countT(y)
      T_skew_Length[count] = skeww_countT(y)
      T_kurt_Length[count] = kurtw_countT(y)

      C_avg_Length[count] = meanw_countC(y)
      C_std_Length[count] = stdw_countC(y)
      C_skew_Length[count] = skeww_countC(y)
      C_kurt_Length[count] = kurtw_countC(y)

      T_turns_arr[count] = T_turns(y)
      C_turns_arr[count] = C_turns(y)
      ratio_turns_arr[count] = ratio_turns(y)
      ratio_words_arr[count] = ratio_words(y)
      count = count + 1

count = 0
#Opens empty csv and writes labeled data
with open('labeled.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'label', 'Mean_T_Words/Turn', 'STD_T_Words/Turn', 'Skew_T_Words/Turn', 'Kurt_T_Words/Turn', 'Mean_C_Words/Turn',
                  'STD_C_Words/Turn', 'Skew_C_Words/Turn', 'Kurt_C_Words/Turn','T_Turns', 'C_Turns','Ratio of turns','T and C WPT Ratio']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    count = 0
    writer.writeheader()
    for at in range(len(id)):
      writer.writerow({'id': id[count], 'label': label[count],
                        'Mean_T_Words/Turn': T_avg_Length[count], 
                        'STD_T_Words/Turn': T_std_Length[count], 
                        'Skew_T_Words/Turn': T_skew_Length[count], 
                        'Kurt_T_Words/Turn': T_kurt_Length[count], 

                        'Mean_C_Words/Turn': C_avg_Length[count], 
                        'STD_C_Words/Turn': C_std_Length[count], 
                        'Skew_C_Words/Turn': C_skew_Length[count], 
                        'Kurt_C_Words/Turn': C_kurt_Length[count], 

                        'T_Turns': T_turns_arr[count], 
                        'C_Turns': C_turns_arr[count], 
                        'Ratio of turns': ratio_turns_arr[count],
                        'T and C WPT Ratio': ratio_words_arr[count]
                        })
      count = count + 1
