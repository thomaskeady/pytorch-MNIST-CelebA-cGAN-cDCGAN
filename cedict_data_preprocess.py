import re
import string

### Rules for separating
# Pick the first definition (separated by '/')
# Of those, remove anything in parenthesis
#	(unless only thing is in parenthesis, in which case strip parenthesis)
# then take longest word (is this the best move?)
# 	Look into phrase2vec



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
			while(i < len(line)):
				if ']' in line[i]:
					count = count + 1
					#print(total)
					#print(line[i])
					#print(' '.join(line[i+1:len(line)]))
					chinese = line[0]
					#english = ' '.join(line[i+1:len(line)]).split('/')
					english = ' '.join(line[i+1:len(line)])
					#english = english.split('/')[1]	# Take first definition only
					#if "(" in english:
					#	print(chinese + '\t' + str(english))
					#print(chinese + '\t' + str(english))

					english = english.split('/')

					#print(chinese + '\t' + str(english[1]))

					words = english[1].split()	# Take the first definition
					#print(chinese + '\t' + str(words))

					longest = ''

					# Delete parenthesis if theres more than one word
					if len(words) > 1:
						toRemove = -1;

						for i in range(len(words)-1):
							if '(' in words[i] or ')' in words[i]:
								#words.remove(words[i])
								toRemove = i

							words[i] = re.sub(r'\W', '', words[i])

						words.remove(words[toRemove])


						longest = max(words, key=len)	# This takes the first if multiple with same length

					else:	# If just one, remove parenthesis if they exist
						if '(' in words[0] or ')' in words[0]:
							longest = words[0][1:len(words[0])-1]
						else:
							longest = words[0]

						longest = re.sub(r'\W', '', longest)


					#longest = max(words, key=len)	# This takes the first if multiple with same length

					#print(str(words) + ' ' + longest)

					outFile.write(chinese + ' ' + longest + '\n')
					print(chinese + ' ' + str(words) + ' ' + longest)

					# Must be last thing in the if statement
					i = len(line)

				i = i + 1


outFile.close()

print(total)
print(count)
print ("Done!")
