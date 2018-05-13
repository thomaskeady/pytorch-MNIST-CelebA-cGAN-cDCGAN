import gensim


print('Loading word2vec')
model = gensim.models.KeyedVectors.load_word2vec_format('../../../GoogleNews-vectors-negative300.bin', binary=True) 
print('Done!')

vectors = model.wv

total = 0
notfound = 0

seen = {}

with open('cedict_processed.txt', 'r') as data:
	with open('cedict_vectors_v2.csv', 'w') as outputFile:
		for line in data:
			total += 1
			word = line.split()[1]
			
			if word in seen:
				seen[word] += 1
			else:
				seen[word] = 0


			try:
				v = vectors[word]

				toWrite=''

				for i in v:
					toWrite = toWrite + str(i) + ', '

				outputFile.write(word + str(seen[word]) + ', ' + toWrite + '\n')

			except Exception as e:
				#print(word + ' not found in word2vec')
				print(str(e))
				notfound += 1

print(total)
print(notfound)
print('Done!')
