#!/usr/bin/python
# -*- coding: utf-8 -*-

#creates indexes of Bible Code

__author__      = "John Dyer"
__copyright__   = "Copyright 2013"

"""
Dependencies: Python 2.7, pyquery, stemming
Usage: indexer.py -i '../browserbible/app/content/bibles/en_nasb/'
"""

import os, sys, getopt
from pyquery import PyQuery
from stemming.porter2 import stem

def main(argv):  

	path = ''
	enable_stem = False
	single_chapter = ''

	# get options
	opts, args = getopt.getopt(argv, 'i:s:c:')
	for opt, arg in opts:                
		if opt in ("-i"):      
			path = arg
		elif opt in ("-s"):      
			enable_stem = True	
		elif opt in ("-c"):      
			single_chapter = arg					
			
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
					
	
	# do indexing
	if single_chapter != '':
		single_path = path + single_chapter + '.html'
		process_chapter(single_path, index_path, enable_stem)
	
	else:
	
		# go through osis book names to keep things in order
		osis_names = ["Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal", "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"]
		
		for osis_book in osis_names:
			for chapter_num in range(1,150):
				chapter_osis = osis_book + '.' + str(chapter_num)
				chapter_path = os.path.join(path, chapter_osis + '.html')
				
				if os.path.exists(chapter_path):
					process_chapter(chapter_path, index_path, enable_stem)
				else:
					break
		
	# close all files
	cleanup_index(index_path)
			
def process_chapter(chapter_path, index_path, enable_stem) :

	# removed characters
	remove_chars = ['.',',',';','?''!','-',u'–',u'―',u'—',u'~',':','"',')','(','[',']','/','\\',"'s",u'’s',"'",u'‘',u'’',u'“',u'”', u'¿', '*', '<','>','&','{','}']

	restricted_words = ['a', 'and', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'despite', 'down', 'during', 'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'since', 'the', 'through', 'throughout', 'till', 'to', 'toward', 'under', 'underneath', 'until', 'up', 'upon', 'with', 'within', 'without']
		
	# create jQuery object
	html = open(chapter_path, 'r').read()
	jquery = PyQuery(html)
	
	print jquery.find('.chapter').attr('data-osis')
	
	# find all verses, remove all notes and verse numbers
	verses = jquery('span.verse')
	verses.find('span.note').remove()
	verses.find('span.cf').remove()
	verses.find('.v-num').remove()
	
	for verse in verses:
		v = PyQuery(verse)
		osis = v.attr('data-osis')
		text = v.text()
		
		# remove punctuation
		for s in remove_chars:
			text = text.replace(s, '')
		
		words = text.split(' ')
		
		for word in words:
			word = word.strip().lower()
			
			is_restricted = True
			try:
				restricted_words.index(word)
			except:	
				is_restricted = False
								
			if word != '' and not is_restricted and not word.isnumeric():
			
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
			
		