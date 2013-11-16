#!/usr/bin/python

import glob, nltk
import string, sys, random, time, re, pprint
from nltk.collocations import *
import pprint
from nltk.tag import RegexpTagger  


af = open('/Users/cahylles/TopicExtraction/artistList')
artists = af.readlines()

trigrams = nltk.collocations.TrigramAssocMeasures()

wd = nltk.FreqDist()
cd = nltk.FreqDist()

def extract_en(tree, cd):
	names = []
	if hasattr(tree, 'node') and tree.node:
		if tree.node == 'ORGANIZATION':
			#print 'ORG = ' + ' '.join([child[0] for child in tree])
			names.append('ORG ' + ' '.join([child[0] for child in tree]))
			cd.inc('org')
		elif tree.node == 'PERSON':
			#print 'PERSON = ' + ' '.join([child[0] for child in tree])
			names.append('PERSON ' + ' '.join([child[0] for child in tree]))
			cd.inc('person')
		elif tree.node == 'LOCATION':
			#print 'LOCATION = ' + ' '.join([child[0] for child in tree])
			names.append('LOC ' + ' '.join([child[0] for child in tree]))
			cd.inc('location')
		elif tree.node == 'MONEY':
			#print 'MONEY= ' + ' '.join([child[0] for child in tree])
			names.append('$$$ ' + ' '.join([child[0] for child in tree]))
			cd.inc('money')
		elif tree.node == 'FACILITY':
			#print 'FACILITY = ' + ' '.join([child[0] for child in tree])
			names.append('FACILITY ' + ' '.join([child[0] for child in tree]))
			cd.inc('facility')
		elif tree.node == 'GPE':
			#print 'GPE = ' + ' '.join([child[0] for child in tree])
			names.append('GPE ' + ' '.join([child[0] for child in tree]))
			cd.inc('gpe')
		else:
			for child in tree:
				#print '\tChild = ', child
				extract_en(child, cd)
#	return set(names)

for a in artists:
	tokens = nltk.word_tokenize(a)
	tagged = nltk.pos_tag(tokens)
	tags   = [ tag for (w, tag) in tagged ]
	chunk  = nltk.chunk.ne_chunk(tagged)
	#tritags = tuple(nltk.trigrams(tags))

	#print tags, a, chunk
	
	wd.inc(tuple(tags))
	extract_en(chunk, cd)




wd.tabulate()
cd.tabulate()
