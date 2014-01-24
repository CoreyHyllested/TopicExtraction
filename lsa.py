from numpy import zeros
from scipy.linalg import svd
#following needed for TFIDF
from math import log
from numpy import asarray, sum

titles = [ "The Neatest Little Guide to Stock Market Investing by Corey Hyllested",
           "Investing For Dummies, 4th Edition by Corey Hyllested",
           "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
           "The Little Book of Value Creation with Investing",
           "Value Investing: From Graham to Buffett and Beyond",
           "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
           "Investing in Real Estate, 5th Edition",
           "Stock Investing For Dummies and Morons",
           "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"
          ]

stopwords = ['and','edition','for','in','little','of','the','to']
ignorechars = ''',:'!'''

class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0        

    def parse(self, doc):
        print "Adding doc", self.dcount, doc
        words = doc.split();
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
                print "\tadding doc", self.dcount, "to word,", w, ", doc list", self.wdict[w]
            else:
                self.wdict[w] = [self.dcount]
                print "\tadding doc", self.dcount, "to word,", w, ", doc list", self.wdict[w]
        self.dcount += 1      

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
		#create (words_greater_than_one X docCount) matrix 
		# 		doc0	doc1	doc2	doc3	doc4	doc5	doc6	doc7	
		# w0 
		# w1 
		# w2
		# w3
		# w4 
		# ...

        print "matrix = ", len(self.keys), '(words) x ', self.dcount, "(document) matrix"
        self.A = zeros([len(self.keys), self.dcount])
        for word_idx, key in enumerate(self.keys):		#for each word
            for doc in self.wdict[key]:					#for each document
                self.A[word_idx, doc] += 1				#just add one, not the number of times it appears

    def calc(self):
        self.U, self.S, self.Vt = svd(self.A)
        uRows, uCols = self.U.shape
        sRows = self.S.shape
        vRows, vCols = self.Vt.shape
        print "U = ??? Matrix", uRows, 'x', uCols
        print "S = ??? Matrix", sRows
        print "V = ??? Matrix", vRows, 'x', vCols

    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)        
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def printA(self):
        print 'Here is the count matrix'
        print self.A

    def printSVD(self):
        print 'Here are the singular values, per document', len(self.S)
        print self.S
        print 'Here are the first 3 columns of the U matrix'
        print -1*self.U[:, 0:3]
        print 'Here are the first 3 rows of the Vt matrix'
        print -1*self.Vt[0:3, :]


mylsa = LSA(stopwords, ignorechars)

for t in titles:
    mylsa.parse(t)

mylsa.build()
#mylsa.TFIDF()
mylsa.printA()
mylsa.calc()
mylsa.printSVD()
