#!/usr/bin/python
# -*- coding: utf-8 -*-

#creates indexes of Bible Code

__author__      = "John Dyer"
__copyright__   = "Copyright 2013"

import os, sys, getopt
from pyquery import PyQuery
from stemming.porter2 import stem

def main(argv):  

	path = ''
	enable_stem = False

	# get options
	opts, args = getopt.getopt(argv, 'i:s:')
	for opt, arg in opts:                
		if opt in ("-i"):      
			path = arg
		elseif opt in ("-s"):      
			enable_stem = True		
			
	if path == '':
		print 'no path defined'
		exit()
		
	# create index path	
	index_path = path + '/index/'
	if not os.path.exists(index_path): 
		os.makedirs(index_path)
	else:
		#delete all exising files
		for the_file in os.listdir(index_path):
			file_path = os.path.join(index_path, the_file)
			os.unlink(file_path)			
	
	#demo chapter
	#process_chapter(path + 'Gen.1.html', index_path)
	#
			
	#exit()
	
	# go through all files
	'''
	for the_file in os.listdir(path):
		if the_file.endswith(".html") and not the_file.endswith("index.html"):
			chapter_path = 	os.path.join(path, the_file)
			process_chapter(chapter_path, index_path);
	'''
	# go through osis book names
	osis_names = ["Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal", "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"]
	
	for osis_book in osis_names:
		for chapter_num in range(1,150):
			chapter_osis = osis_book + '.' + str(chapter_num)
			chapter_path = os.path.join(path, chapter_osis + '.html')
			
			if os.path.exists(chapter_path):
				process_chapter(chapter_path, index_path)
			else:
				break
	
	
	
	# close all files
	cleanup_index(index_path)
			
def process_chapter(chapter_path, index_path) :
	html = open(chapter_path, 'r').read()
	jquery = PyQuery(html)
	
	print jquery.find('.chapter').attr('data-osis')
	
	verses = jquery('span.verse')
	verses.find('span.note').remove()
	verses.find('span.cf').remove()
	verses.find('.v-num').remove()			
	
	for verse in verses:
		v = PyQuery(verse)
		osis = v.attr('data-osis')
		text = v.text()
		
		#remove all punctuation
		text = text.replace('.','').replace(',','').replace(';','').replace('?','').replace('!','').replace('-','').replace(u'–','').replace(u'―','').replace(u'—','').replace(u'~','').replace(':','').replace('"','').replace(')','').replace('(','').replace('[','').replace(']','').replace('/','').replace("'s",'').replace(u'’s','').replace("'",'').replace(u'‘','').replace(u'’','').replace(u'“','').replace(u'”','')
		
		words = text.split(' ')
		
		for word in words:
			word = word.strip().lower()
						
			if word != '' and not word.isnumeric():
			
				# stemmer?
				if enable_stem:
					word = stem(word)
			
				word_path = index_path + word + '.json'
				
				# check for file
				if os.path.exists(word_path):
					f = open(word_path,'a')
					f.write(',"' + osis + '"')
					f.close()
				else:
					f = open(word_path,'a')
					f.write('["' + osis + '"')
					f.close()				
			
		
		# print osis + ' ' + str(words.count())



def cleanup_index(index_path) :
	for the_file in os.listdir(index_path):
		file_path = os.path.join(index_path, the_file)
		
		f = open(file_path,'a')
		f.write(']')
		f.close()			
			
if __name__ == "__main__":
    main(sys.argv[1:])
			
		