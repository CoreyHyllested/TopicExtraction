#!/usr/bin/python

import glob, nltk
import string, sys, random, time, re, pprint
from nltk.collocations import *
import pprint
from nltk.tag import RegexpTagger  



#PART I
#This was a far, far more difficult task than we thought it would be.
# The goal was to download user-generated music tags and improve the signal/noise by removing non-descriptive information (e.g. Artist Name, Song, Album, etc) leaving descriptive terms.
# The tags was a mix of artists and music information (The Beatles, Abbey Road, Can't Buy Me Love), comments (<userID>'s favorite, listen to backwards), and description (indie-rock, fast, 2010s)
# Sometimes there are full sentences, but most tags consist of one or three descriptive words.  I thought this would be useful -- but it also meant a lack of context.
# The EXPECTATION was that extracting names of artists would be a largely straight-forward exercise.  We ran into numerous confounding problems, which I will detail a bit of here.

# Artist Names.
# I expected to have a difficulty with artists named after places: 'Boston', 'Kansas'.
# Names are far more diverse than we were thinking. E.g. 'Sting', 'Earth, Wind, and Fire', 'My Morning Jacket', 'Sublime', 'Blink 182'.
# To identify these as proper-nouns, the entire artist name tag must be capitalized.  Earth, wind and fire for example is NE_tagged as GPE, Noun and Noun.
# Confusingly, people were not tagged properly.  First names were properly tagged as People, but last names were usually Organizations or less commonly GPE.
# Slim Shady and Howlin' Wolf are examples that were successfully tagged as a person.  
# Variations of the artist, misspellings, and personas create diversity.  Eminem is sometimes written as Emin3m, this is curiously tagged as a PRP (Pronoun).  
# While I fully expected to have differences in capitalization, I did not expect that it would be required.


#UserNames.
# Users, such as beachbeck42, can create personal playlists by identifying songs.  Usernames should be easy to detect.
# because of their length and special charactoristics such as embedding numbers.  This proved a more difficult task because of NLTK's structure, because 
# we could not utilize the regex tagger and then backoff to the POS tagger.  We had to use write our own. 

# One thought was to try and reduce the number of words and misspellings by using the Levenshtein distance between words to reduce the changes in tagged words.  E.g. Emin3m => Eminem.
# Thus, we tried to normalize the tokens... which helped the distance metrics.  This completely destroyed the POS tagging effort as it reduced the context/information available to 
# identify 'my morning jacket' as a proper noun phrase.

# Corey used the LastFM API to download tags from a select list of artists, manually created list of ~500 popular artists.  
# Used Alex's complete list of artists and created distributions of POS tags, NE_tags.  Looked at distributions for patterns.
# Wrote a regex tagger... played with the rules for extracting PERSONS, Organizations, etc.   
# Alex helped create the idea.  Created a pickled CityListing.  Alex also used the LastFM API to download all of the artists in LastFM database.


#Comments.
# The expected 'remainder'.  One confounding problem is NLTK doesn't 'know' the word, but guesses POS based on the suffix.  'ThisTrackIsLoved' which should is tagged as a Verb,
# because of its 'ed' or 'ing' ending.

# Attempts.
# First, we identified common patterns.
# <Artist Name>
# <Song>
# <Artist> - <Song> - <album>









# tags a corpus of documents, 
def createSentCorpus(docs):
	""" Takes a corpus of documents. 
		Processes documents.  Tags words and used both NLTKs ne-tagger.  
		Then extracts entity names. 
	"""

	grammar = """
		NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
			{<NNP>+}                # chunk sequences of proper nouns
		DP: {^<JJ><.>$}
	"""
	
	cp = nltk.RegexpParser(grammar)

	for doc in docs:
		print doc
		fp = open(doc)
		doc_cntnt = fp.read()
		sentences = nltk.sent_tokenize(doc_cntnt)
		normalizd = [ word for word in sentences]	#Not actually normalizing... word.lower().strip()
		tokenized = [nltk.word_tokenize(s)  for s    in normalizd]
		pos_taged = [nltk.pos_tag(ptag)     for ptag in tokenized]
		#print 'pos-tagged', len(pos_taged)
		chunksent = [ cp.parse(pos_taged) ]
		#chunksent = nltk.batch_ne_chunk(pos_taged)

		for i in chunksent:
			print i 

		for chunk in chunksent:
			extract_en(chunk)


def extract_en(tree):
	"""extract_en(tree)
		extracts the  named entites based on ne_chunker.  
		we started adding other fields as the ne_chunker wasn't all over the place.
	"""

	names = []

	if hasattr(tree, 'node') and tree.node:
		if tree.node == 'ORGANIZATION':
			print 'ORG = ' + ' '.join([child[0] for child in tree])
			names.append('ORG ' + ' '.join([child[0] for child in tree]))
		elif tree.node == 'DP':	#descriptive phrase
			print 'DP = ' + ' '.join([child[0] for child in tree])
			names.append('DP ' + ' '.join([child[0] for child in tree]))
		elif tree.node == 'PERSON':
			print 'PERSON = ' + ' '.join([child[0] for child in tree])
			names.append('PERSON ' + ' '.join([child[0] for child in tree]))
		elif tree.node == 'LOCATION':
			print 'LOCATION = ' + ' '.join([child[0] for child in tree])
			names.append('LOC ' + ' '.join([child[0] for child in tree]))
		elif tree.node == 'MONEY':
			print 'MONEY= ' + ' '.join([child[0] for child in tree])
			names.append('$$$ ' + ' '.join([child[0] for child in tree]))
		elif tree.node == 'FACILITY':
			print 'FACILITY = ' + ' '.join([child[0] for child in tree])
			names.append('FACILITY ' + ' '.join([child[0] for child in tree]))
		elif tree.node == 'GPE':
			print 'GPE = ' + ' '.join([child[0] for child in tree])
			names.append('GPE ' + ' '.join([child[0] for child in tree]))
		else:
			print 'Node = ', tree.node
			for child in tree:
				print '\tChild = ', child
			for child in tree:
				names.extend(extract_en(child))
	return set(names)




def isType(x, myType):
	tokens = x.split()
	if (myType == tokens[0]):
		return tokens[1:]
	return None


def tagCorpus():
	"""Pretty specific.  Opens a single file, reads all the tags.
		Used the ne_tagger.  Dumped the NE: DP (descriptive phrase), orgs, Global Political Entities, and locations.
		Use pprint.pprint to make it pretty.
	"""

	files = [ '/Users/cahylles/TopicExtraction/artistsPeriod/pages/b95ce3ff-3d05-4e87-9e01-c97b66af13d4.tags.Eminem' ]
	print len(files)
	#(chunksents, nament) = createSentCorpus(files)
	#dps  = [isType(x, 'DP')  for x in nament]
	#orgs = [isType(x, 'ORG') for x in nament]
	#gpes = [isType(x, 'GPE') for x in nament]
	#locs = [isType(x, 'LOCATION') for x in nament]

	#dp  = [x for x in dps  if x is not None]
	#org = [x for x in orgs if x is not None]
	#gpe = [x for x in gpes if x is not None]
	#loc = [x for x in locs if x is not None]

	#print 'ORGS'
	#pprint.pprint(org)
	#print 'GPE'
	#pprint.pprint(gpe)
	#print 'LOCATIONS'
	#pprint.pprint(loc)
	#print 'ORGS'
	#pprint.pprint(dp)




# This obviously takes too long when the dictionary gets large.  
# This does happen because 1) We are using a dictionary from user-generated words including user names, artist names, misspellings, short-hand  
def calcWordDistance(dictionary):
	for word in dictionary:
		for test_word in dictionary:
			levdist = nltk.metrics.edit_distance(word, test_word)
			#ratio = (float(len(dictionary)) - float(levdist)) / float(len(dictionary))
			ratio = float(abs(len(word) - len(test_word))) / float(len(dictionary))
			lendiff = abs(len(word) - len(test_word))
			length  = float(len(word)) + (float(lendiff)/2) 
			if levdist < 4 and levdist < (length * .3):
				print levdist, lendiff, (length * .3), word, test_word 


def createWordDistribution():
	"""Creating distribution of words.
		-- trying to understand the "spread" in words.  
		-- it became obvious pretty quickly, once it was working that this was NOT the way to keep going""" 

	wd = nltk.FreqDist()
	for file in files:
		document = open(file)
		sentences = document.readlines()
		for s in sentences:
			for t in nltk.word_tokenize(s):
				wd.inc(t.strip().lower())
	eDict = wd.keys()
	calcWordDistance(eDict)
	


if __name__ == "__main__":
	#files = glob.glob('/Users/cahylles/TopicExtraction/artists/pages/*')
	files = [ '/Users/cahylles/TopicExtraction/artists/pages/b95ce3ff-3d05-4e87-9e01-c97b66af13d4.tags.Eminem' ]
	files = [ '/Users/cahylles/Desktop/LCS.artists' ]


	# Examples, to test out.  Basically test cases.
	sentences2 = []
	sentences2.append('slim-shady')
	sentences2.append('slimshady')
	sentences2.append('slim shady')
	sentences2.append('slimmutherfukashady')
	sentences2.append('rap genius')
	sentences2.append('suicidal')
	sentences2.append('one of his best by far')
	sentences2.append('socially conscious')
	sentences2.append('Capt America')
	sentences2.append('Mr. Mathers')
	sentences2.append('new')
	sentences2.append('psixaos - loved tracks')
	sentences2.append('DeanMarkTaylorLoved')
	sentences2.append('G-Unit')
	sentences2.append('borrowed nostalgic song')
	sentences2.append('mixtape')
	sentences2.append('davaho53')
	sentences2.append('baunsowanie')
	sentences2.append('emin3em')
	sentences2.append('Eminem - Model')
	sentences2.append('Eminem - The Blind New')
	sentences2.append('Eminem - Role Models')
	sentences2.append('Emin3m - Role Models')
	sentences2.append('Dylan and Friends')
	sentences2.append(':D')
	sentences2.append('laecheln')
	sentences2.append('old rock')
	sentences2.append('fav')
	sentences2.append('guitars')
	sentences2.append('folk rock')
	sentences2.append('indie-rock')
	sentences2.append('yellow')
	sentences2.append('cheerful')

	#wd = createWordDistribution()


	grammar = r"""
		#Look for full sentences first. 
		DESC_TAG: {^<JJ|JJR|JJS>$}				# Single adjective, likely describing the music or artist.
		DESC_TAG: {^<RB|RBS><JJ|JR|JJS>$}		# Single adverb-adjective:  Descriptive combo	

		OBJ: {^<NN|NNS>+$}						# Single noun 
		OBJ: {^<JJ|JJR|JJS>?<NN|NNS>+$}			# adjective - Noun set

		PNE: {^<DT>?<VBZ|JJ|JR|JJR|JJS>?<NP|NNP|NNPS>+$}						# Proper Noun set
		NE:  {^<DT>?<CC|JJ|JR|JJR|JJS|NP|NNP|NNPS|PRP>+$}	# Proper w/ description Noun Set 

		MUZ: {^<DT>?<JJ|JJR|NP|NNP><--|:><DT>?<JJ|JJR|JJS|NP|NNS|NNP>+$}											#<NE> - <NE>

		CMNT: {<CD><IN><PRP|PRP$><JJ|JJS|JJR>}
		NP: {<DT|JJ|NN.*>+}				# Chunk sequences of DT, JJ, NN
		
	"""

		#PP: {<IN><NP>}               # Chunk prepositions followed by NP
		#VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
		#CLAUSE: {<NP><VP>}           # Chunk NP, VP

	cp = nltk.RegexpParser(grammar)
	desc  = []
	ne  = []
	etc = []
	obj = []
	muz = []



	#Tried building a tagger that would backoff from POS tagging to utilize a regex identifying user strings.
	#patterns = [ (r'^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$', 'USER'), ]
	#regexp_tagger = RegexpTagger(patterns) #, backoff=nltk.pos_tag)
	


	for s in sentences2:
		tokens = nltk.word_tokenize(s)
		#print '\t', tokens, len(tokens)
		tagged = nltk.pos_tag(tokens)
		#ne_tag = nltk.batch_ne_chunk(tokens)

		tree = cp.parse(tagged)
		print s, tagged

		for subtree in tree.subtrees():
			if subtree.node == 'DESC_TAG': 
				desc.append((s, subtree))
			# if subtree is PROPER NOUN ENTITY (plural or not).
			elif subtree.node == 'PNE' or subtree.node == 'NE': 
				ne.append((s, subtree))
			elif subtree.node == 'MUZ':
				muz.append((s, subtree))
			elif subtree.node == 'OBJ':
				obj.append((s, subtree))
			else:
				etc.append(subtree)



	for (d, subtree) in desc:
		print "Desc:\t", d, '\t', subtree
		#likely to maintain full sentences.  Come back and check if this guess it true.

	for (obj, subtree) in obj:
		print "OBJ:\t", obj, '\t', subtree 
		#We should post-process the 'objects'.  Treat this as first pass.  usernames prob. exist here, use regex.

	for (ne, subtree) in ne:
		print "NE:\t", ne, '\t', subtree
	
	for (mz, subtree) in muz:
		print "MUSIC:\t", mz, '\t', subtree
		#Combine with NE?  Kinda the same thing?





	
	
# PART III.
#  We didn't setup anything to record the precision and recall.
# I would suggest that this project has been a great learning experience, but a failure in terms of producing quality results.
# The precision is particularly bad as noted above.  The user-generated mistakes (spelling, capitaization, punctuation) do not provide enough context.  
# Recall is probably reasonable, but with poor precision.... our F-score would be low.









