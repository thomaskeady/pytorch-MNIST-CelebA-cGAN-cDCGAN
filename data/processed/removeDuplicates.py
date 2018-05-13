#!/usr/bin/env python3

inputData = "cj5-20902-cleaned.txt"
outputFile = "cj5-20902-cleaned-noDups.txt"

with open(inputData) as d:
    seen = set()
    duplicates = list()

    for line in d:
        if line in seen:
            duplicates.append(line)
        else:
            seen.add(line)

    #print("Writing duplicate-free list to " + outputFile)

    # cj5-20902-cleaned.txt has no duplicates, yay!
    ui = input(str(len(duplicates)) + " dupliacates found. Would you like to print them? [y/n] ")

    if 'y' in ui:
        for e in duplicates:
            print(e)

print ("Done removing duplicates!")
