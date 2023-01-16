#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run: wget https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt

"""
import sys
from sys import argv
import re

# s es 's ing

MAX_WORD_LENGTH = 22 # antidisestablishmentarianism is 29 but who cares
DICTITONARY_FILENAME = "google-10000-english-usa.txt" # use "/usr/share/dict/words" if offline

if len(argv) < 2:
	print('Usage: acrobat_clipboard_corrector.py copypaste_file.txt')
	exit()
	
try:
	dictFile = open(DICTITONARY_FILENAME)
except IOError:
	print(f'Error: No {DICTITONARY_FILENAME=} file found!')
	print("HINT: Run 'curl http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt > wordsEn.txt'")
	exit()

dictionary = set()
dictionary.add('furfuryl')
dictionary.add('furfural')
for line in dictFile.readlines():
	dictionary.add(re.sub('[^A-Za-z]', '', line)) 

txtFile = open(argv[-1])

for line in txtFile.readlines():
	#line = line.translate(None, ' ') # removing spaces
	line = line.replace(' ', '')

	while line:
		jump = 0
		for i in range(MAX_WORD_LENGTH, 1, -1):
			current = line[:i]
			if current.lower() in dictionary:
				jump = i
				break
		if jump == 0:
			sys.stdout.write(line[:1])
			if line[:1] in [".", ",", ":", ";", "?", "!"]:
				sys.stdout.write(" ")
			line = line[1:]
		else:
			sys.stdout.write(line[:jump] + " ")
			line = line[jump:]
	print("")