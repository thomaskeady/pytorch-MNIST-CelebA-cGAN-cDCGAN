import re
import string

### Rules for separating
# Pick the first definition (separated by '/')
# Turn - into _
# Remove parenthesis, and other punctuation
# Pick longest word



with open('data/raw/cedict_ts_u8.txt', 'r') as data:

	count = 0
	total = 0

	outFile = open('data/processed/cedict_processed.txt', 'w')

	for line in data:
		total = total + 1
		#print (line)
		line = line.split()
		#print(line[0] + '\t' + str(len(line[0])))
		if len(line[0]) == 1:

			i = 1
			while(i < len(line)):	# To skip to definition part
				if ']' in line[i]:
					count = count + 1
					chinese = line[0]

					#english = ' '.join(line[i+1:len(line)]).split('/')
					english = ' '.join(line[i+1:len(line)])

					english = english.split('/')

					english = re.sub('-', '_', english[1])
					english = re.sub('[^a-zA-Z ]', '', english)
					#print(english)
					words = english.split()
					#print(str(words))

					longest = max(words, key=len)

					#print(chinese + ' ' + longest)

					outFile.write(chinese + ' ' + longest + '\n')
					#print(chinese + ' ' + str(words) + ' ' + longest)
					#print(chinese + ' ' + longest)

					# Must be last thing in the if statement
					i = len(line)

				i = i + 1


outFile.close()

print(total)
print(count)
print ("Done!")
