from unittest import result
from zipfile import ZipFile
import csv
from sentence_transformers import SentenceTransformer, InputExample, losses
import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, util

#Opens dataset reads data all data into array
def open_file_allLines(file_name):
	f = open(file_name, "r")
	y = f.readlines()     #Y will have the whole transcript as an array
	for i in range(0,len(y)):
		i = i +1
	f.close
	return y

#Rwturns Semantic Similarity Scentence Comparisons
def semantic(x):
	model_name="Sakil/sentence_similarity_semantic_search"
	model = SentenceTransformer(model_name)
    
	sentences = x

	#Number of scentences
	n = len(sentences)

	#Encode all sentences
	embeddings = model.encode(sentences)

	#Compute cosine similarity between all pairs
	cos_sim = util.cos_sim(embeddings, embeddings)

	#Add all pairs to a list with their cosine similarity score
	all_sentence_combinations = []

	for i in range(len(cos_sim)-1):

		for j in range(i+1, len(cos_sim)):
		
			all_sentence_combinations.append([cos_sim[i][j], i, j])

	#Compute Average score: All Scentences
	sum = 0
	total = int((n*(n-1))/2) # number of comparisons
	for score, i, j in all_sentence_combinations[0:(total)]:
		sum = sum + cos_sim[i][j]

	Average_All = sum / total

	#Compare Average Score: Only Adjacent Scentences
	sum_b = 0
	for i in range(0,n-2):
		#uncomment to check which scentences are being compared
		#print("{} \t {} \t {:.4f}".format(sentences[i], sentences[i+1], cos_sim[i][i+1]))
		sum_b = sum_b + cos_sim[i][i+1]

	Average_Adj = sum_b / (n-1)
	#print("Average Score B (Adjacent Scentences Compared): {}".format(Average_b))

	all_semantics =[Average_All, Average_Adj]
	return all_semantics


#Main

file_name = "content/DataSets.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

#Creation of empty arrays
id = [0] * 258
label = [0] * 258
Sem_All_Avg = [0] * 258
Sem_Adj_Avg = [0] * 258

count = 0
#Opens csv file read filenames from file path may need to be changed
with open('C:/Users/User/Documents/Capstone/content/DataSets/labeleddata/testlabels.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if(row["id"] == 'high_022' or row["id"] == 'low_023'):
			continue
		x = open_file_allLines("C:/Users/User/Documents/Capstone/content/DataSets/"+row["id"])
		id[count] = row["id"]
		label[count] = row["label"]
		Sem_results = semantic(x)
		Sem_All_Avg[count] = Sem_results[0]
		Sem_Adj_Avg[count] = Sem_results[1]
		count = count + 1

count = 0
#Opens empty csv and writes labeled data
with open('labeled.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'label', 'Sem_All_Avg', 'Sem_Adj_Avg']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    count = 0
    writer.writeheader()
    for at in range(len(id)):
      writer.writerow({'id': id[count], 'label': label[count],
                        'Sem_All_Avg' : Sem_All_Avg[count],
						'Sem_Adj_Avg' : Sem_Adj_Avg[count]
                        })
      count = count + 1
