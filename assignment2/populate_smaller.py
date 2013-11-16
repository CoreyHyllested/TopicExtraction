#!/usr/bin/python

import re
import os
import os.path
import sys
import uuid
import time
import urllib2
import httplib
import threading
import datetime
import Queue
import random
import pylast
from pylast import *

VER = 0.9
DBG = 1

done  = False

# My LastFM Registered API KEYS
API_KEY="4adc88d5ff43f98ff32975c3ad88d5d8" 
API_SEC="769d2ab77e3ee02b4ee87ef398f96dcb"
MD5_HSH="0297ffdf611478bb441be741b266f964"
USRNAME="cahylles"

lfm  = get_lastfm_network(api_key=API_KEY, api_secret=API_SEC,username=USRNAME, password_hash=MD5_HSH) 


def trace(x):
	if (DBG):
		print (str(x))
		

def createDirs(path):
	if (os.path.exists(path + "/pages/") == False):
		os.makedirs(path + "/pages/")
	return 






class ThreadPopulate(threading.Thread):
	""" ThreadPopulate (path, q_last_dl)
	The 'path' identifies where to lay the files on the filesystem.
	The 'q_last_dl' will be populated with artists that LastFM (or any othe service should download
	
	Currently, the file used to identify artists is hardcoded.  See filp below.  """

	def __init__(self, path, queue_last_dl):
		threading.Thread.__init__(self)
		self.q_last_dl = queue_last_dl
		self.name = "Populate list w/ random" 
		self.path = path


	def run(self):
		sample_list = []
		filp = open("/Users/cahylles/Desktop/artists", 'r')
		unique_list = filp.readlines()
		filp.close()
		
		
		for x in sample_list:
			band = x.split('/')[-1].replace('-', ' ').strip();

			# for concerts.better
			artstFM = band
			
			self.q_last_dl.put (artstFM)
			trace("queueing " + str(artstFM) + " for tag download") 





class ThreadLastFM(threading.Thread):
	""" ThreadLastFM() downloads tags for each artists in queue_dl.
	They are written to PATH/pages/.
	The hash is the MusicBrainzID. """

	def __init__(self, path, queue_dl, lfm):
		threading.Thread.__init__(self)
		self.name = "Download" 
		self.path = path
		self.q_dl = queue_dl
		self.fm   = lfm

		createDirs(path)
	

	def __createTagfile__(self, artistFM):
		mbid = artistFM.get_mbid()
		tagfile = None

		if (not os.path.exists(self.path + "/pages/" + str(mbid) + ".tags." + str(artistFM))):
			tagfile = open(self.path + "/pages/" + str(mbid) + ".tags." + str(artistFM), 'w')
			trace("tagfile = " + self.path + "/pages/" + str(mbid) + ".tags." + str(artistFM))
		else:
			trace ("tagfile exists for " + artistFM.get_name())

		return (mbid, tagfile)

		
	def run(self):
		while (not self.q_dl.empty()):
			tagfile = None

			artist = self.q_dl.get_nowait()
			trace("download " + str(artist) + ", " + str(self.q_dl.qsize()) + " in the q")

			try:
				artistFM = self.fm.get_artist(artist)
				(mbid, tagfile) = self.__createTagfile__(artistFM)
				if (tagfile == None):
					continue

				tags = artistFM.get_top_tags()
				trks = artistFM.get_top_tracks()

				tags_artist = []
				tags_tracks = []

				for (tag, weight) in tags:
					writeTag = tag.get_name()   #.replace(' ', '_')
					#print writeTag, " ", int(weight)
					
					try: 
						if ( int(weight) == 0):
							weight = 1
					except TypeError:
						print ("we got type error on weight")

					for i in range(int(weight)):
						tags_artist.append(writeTag.encode('utf-8'))

				for x in trks:
					(track, weight) = x
					tags = track.get_top_tags()
					for (tag, weight) in tags:

						#don't bother with the last zero-strength tags for songs
						try:
							writeTag = tag.get_name()   #.replace(' ', '_')
							if (int(weight) < -10):
								print "can't happen"
						except TypeError:
							print "read " + str(artist)  + "\t" + str(track)

						for i in range(int(weight)):
							tags_tracks.append(writeTag.encode('utf-8'))


				totaltags = set(tags_artist + tags_tracks)
				if (len(totaltags) > 0):
					tagfile.write('.\n'.join(totaltags))


			except pylast.WSError, e:
				#retry
				print "WS Error \"", str(artist), "\" ", e
			except pylast.MalformedResponseError, e:
				print e, "\"", str(artist), "\""
			except Exception as err:
				print "GeneralException", type(err), err, err.args
			finally:
				if (tagfile != None):
					tagfile.close()


		
def main():

	if (len(sys.argv) != 2):
		print "no!"
		sys.exit(0)

	path = os.path.abspath(sys.argv[1])
	q_l_download = Queue.Queue() 
	q_html2txt = Queue.Queue() 
	pop = ThreadPopulate(path, q_l_download)
	pop.start()
	pop.join()

	thrdLastFM1 = ThreadLastFM(path, q_l_download, lfm)
	thrdLastFM1.start()

	thrdLastFM2 = ThreadLastFM(path, q_l_download, lfm)
	thrdLastFM3 = ThreadLastFM(path, q_l_download, lfm)
	thrdLastFM4 = ThreadLastFM(path, q_l_download, lfm)
	thrdLastFM5 = ThreadLastFM(path, q_l_download, lfm)
	thrdLastFM6 = ThreadLastFM(path, q_l_download, lfm)

	thrdLastFM2.start()
	thrdLastFM3.start()
	thrdLastFM4.start()
	thrdLastFM5.start()
	thrdLastFM6.start()

	thrdLastFM1.join()
	thrdLastFM2.join()
	thrdLastFM3.join()
	thrdLastFM4.join()
	thrdLastFM5.join()
	thrdLastFM6.join()
	return


if __name__ == "__main__":
    main()

