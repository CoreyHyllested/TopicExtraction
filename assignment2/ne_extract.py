import nltk, re, pprint
from nltk.corpus import conll2000 #sz = 8936


# pick one of three types: NP 
# Develop a simple chunker using the regular expression chunker nltk.RegexpParser. 
np_grammar = r"""
  NP:	{<NN|NNP|NP|NP\$>*<JJ>*<AT|IN-TL|JJ|JJ-TL|VBG-TL|NN|NN-TL|NP|NP-TL|NNP|NNS|NP\$>+<IN>?<DET|AT|JJ>*<NN|NP|NNP|NNS|NP\$|NN-TL|NP-TL|IN-TL>+}			# Noun-noun
  		{<AT|JJ|PP>?<JJ>*<NR|NN|NNP|NNS|NP|NP\$>+}			 # chunk determiner/possessive, adjectives and nouns
"""
		#{<AT|DET|PP>?<JJ>*<NN|NN\$>}   # chunk determiner/possessive, adjectives and nouns
  		#{<DET>?<NN|NNP|NP\$>}
#"""


cp = nltk.RegexpParser(np_grammar)

train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
#test_sents  = conll2000.chunked_sents('test.txt',  chunk_types=['NE'])
corpus = train_sents
#corpus.append(nltk.pos_tag(nltk.word_tokenize("They refuse to permit us to obtain the refuse permit")))
#corpus.append(nltk.pos_tag(nltk.word_tokenize("The jumping blind cow ate it.")))
#corpus.append(nltk.pos_tag(nltk.word_tokenize("Who is playing there plays everywhere.")))
#corpus.append(nltk.pos_tag(nltk.word_tokenize("The clown attacking gently needs a shave.")))
#corpus.append(nltk.pos_tag(nltk.word_tokenize("My favorite sauce is getting gamed by the system.")))


print 


for sent in corpus: 
	tree = cp.parse(sent)
	print sent
	ns = []
	for (w,tag)  in sent:
		ns.append(w)
	
	for subtree in tree.subtrees():
#		print '\n', ' '.join(ns), '\n', sent
		if subtree.node == 'CHUNK': print subtree


def extract_en(tree):
	names = []

	print "has size", len(tree)
	if hasattr(tree, 'node') and tree.node:
		if tree.node == 'NE':
			print 'NE = ' + ' '.join([child[0] for child in tree])
			names.append(' '.join([child[0] for child in tree]))
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


#test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
#print cp.evaluate(test_sents)
