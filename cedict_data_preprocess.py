



with open('data/raw/cedict_ts_u8.txt', 'r') as data:

	count = 0
	total = 0

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
					print(total)
					#print(line[i])
					#print(' '.join(line[i+1:len(line)]))
					chinese = line[0]
					english = ' '.join(line[i+1:len(line)]).split('/')
					#english = english.split('/')[1]	# Take first definition only
					print(chinese + '\t' + str(english))

					# Must be last thing in the if statement
					i = len(line)

				i = i + 1


print(total)
print(count)
print ("Done!")
