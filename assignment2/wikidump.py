#!/usr/bin/python

import nltk
import cPickle, string, numpy, getopt, sys, random, time, re, pprint
import wikirandom
from nltk.corpus import conll2000

corpus = []
corpus.append(nltk.pos_tag(nltk.word_tokenize("The Stones Roses and New Order both kicked off reunion tours last year, and Wu-Tang Clan are at work on a new album to mark their twentieth anniversary.")))
corpus.append(nltk.pos_tag(nltk.word_tokenize("Rumors about this year's Coachella headliners had been swirling for weeks, with the Rolling Stones and Daft Punk among the acts speculated to be performing at the festival.")))

print nltk.batch_ne_chunk(corpus)



def getArticles(nr = 5):
	""" Downloads and analyzes a bunch of random Wikipedia articles """
	(docs, names) = wikirandom.get_random_wikipedia_articles(nr)
	return (docs, names)


def getSentChunks(d, n):
	chunks = []
	nament = []
	i = 0

	for doc in d:
		sentences = nltk.sent_tokenize(doc)
		tokenized = [nltk.word_tokenize(s)  for s    in sentences]
		pos_taged = [nltk.pos_tag(ptag)     for ptag in tokenized]
		chunksent = nltk.batch_ne_chunk(pos_taged)
		chunks.append(chunksent)
		print "calling extract_en on " + n[i]
		for chunk in chunksent:
			nament.extend(extract_en(chunk))
		i = i + 1


	return (chunks, nament)
	#	print chunked_sentences




def extract_en(tree):
	names = []

	print "has size", len(tree)
	if hasattr(tree, 'node') and tree.node:
		if tree.node == 'NNP':
			print 'NNP = ' + ' '.join([child[0] for child in tree])
			names.append('NNP '.join(' '.join([child[0] for child in tree])))
		elif tree.node == 'ORGANIZATION':
			print 'ORG = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		elif tree.node == 'PERSON':
			print 'PERSON = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		elif tree.node == 'LOCATION':
			print 'LOCATION = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		elif tree.node == 'TIME':
			print 'TIME = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		elif tree.node == 'MONEY':
			print 'CASH MONEY= ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		elif tree.node == 'FACILITY':
			print 'FACILITY = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		elif tree.node == 'GPE':
			print 'GPE = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
		else:
			print tree.node
			#print 'tree has no node'
			for child in tree:
				names.extend(extract_en(child))
	return names


(docs, names) = getArticles()

print "begin chunking documents"
(c, ne) = getSentChunks(docs, names)
print "show what we got"
for x in ne:
	print x




if __name__ == "__main__":
	print "Called directly"
else:
	print "other"


