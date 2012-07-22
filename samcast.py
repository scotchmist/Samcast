#!/usr/bin/env python
# encoding: utf-8

"""
Created by Sam Howson on 2012-07-21.

This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/"""

import sys
import os
import libxml2, libxslt
import re, ConfigParser
import urllib


def sampodder(podcast):
	title = podcast
	rss_feed = config.get(podcast, 'rss-feed')
	
	try:
		podnumber = int(config.get(podcast, 'podnumber'))	
	except:
		podnumber = -1
	
	try:
		styledoc = libxml2.parseFile("parse_enclosure.xsl")
		style = libxslt.parseStylesheetDoc(styledoc)
		doc = libxml2.parseFile(rss_feed)
		result = style.applyStylesheet(doc, None)
		podcast_episodes = style.saveResultToString(result)
		podcast_episodes = podcast_episodes.split('\n')[:-1][:podnumber]
		style.freeStylesheet()
		doc.freeDoc()
		result.freeDoc()
		
	except: print '''Couldn't get the podcasts using libxslt :('''
		#Perhaps could try using wget here instead, as with the bashpodder script.

	for episode in podcast_episodes:
		if re.search(episode, logstring):
			pass
		else:
			episode_title=re.split('\/|=|\?', episode)[-1]
			#If you want to do a dry-run, just comment out the line below.
			urllib.urlretrieve(episode, podcast_dir + title + '/'+ episode_title)
			download_log.write(episode + '\n')


if __name__ == "__main__":
	
	home='/Users/sam/'
	podcast_dir= home + 'podcasts/'
	config_file= './sp.conf'
	config = ConfigParser.ConfigParser()
	config.read(config_file)
	podcasts=config.sections()
	download_log = open('./downloads.log', 'a+')
	
	logstring = download_log.read()
	
	for p in podcasts:
		sampodder(p)
		
	download_log.close()