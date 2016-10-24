#!/usr/bin/env python
# encoding: utf-8

"""
Created by Sam Howson on 2012-07-21.
"""

import sys
import os
import libxml2, libxslt
import ConfigParser
import urllib
import argparse
import requests
import re

def sampodder(podcast_dir, podcast, config, logstring):
    rss_feed = config.get(podcast, 'rss-feed')
    thispodcastdir = os.path.join(podcast_dir, podcast)
    
    if not os.path.exists(thispodcastdir):
        os.makedirs(thispodcastdir)
    
    podnumber = config.get(podcast, 'podnumber')
    if not podnumber:
        podnumber = -1
    else:
        int(podnumber)

    styledoc = libxml2.parseFile(os.path.join(os.getcwd(), "parse_enclosure.xsl"))
    style = libxslt.parseStylesheetDoc(styledoc)
    doc = libxml2.parseFile(rss_feed)
    result = style.applyStylesheet(doc, None)
    podcast_results = style.saveResultToString(result)
    podcast_episodes = podcast_results.split('\n')[:-1][:podnumber]
    
    style.freeStylesheet()
    doc.freeDoc()
    result.freeDoc()
    

    for episode in podcast_episodes:
        if episode in logstring:
            return None
        else:
            episode_title = re.split('\/|=|\?', episode)[-1]
            #If you want to do a dry-run, just comment out the line below.
            print(episode, thispodcastdir + '/'+ episode_title)
            episode_path = os.path.join(thispodcastdir, episode_title)
            response = requests.get(episode, stream=True)
            with open(episode_path, 'wb') as ep:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        ep.write(chunk)
            return episode_path



if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description='A podcast downloader script.')
    parser.add_argument('config', help='The location of the configuration file.')
    parser.add_argument('-p', '--podcast-dir', default=os.getcwd(), dest='podcast_dir', help='The location of the directory to save podcasts')
    parser.add_argument('-d', '--download-log', dest='download_log', help='The location of the directory to save podcasts')
    args = parser.parse_args()



    if not args.download_log:
        download_log = os.path.join(args.podcast_dir, 'downloads.log')

    config = ConfigParser.ConfigParser()
    config.read(args.config)
    podcasts = config.sections()
  
    if not os.path.exists(download_log):
        open(download_log, 'w+').close()
        

    with open(download_log, 'rw+') as dl:
        logstring = dl.read()
        for podcast in podcasts:
            try:
                podcast_file = sampodder(args.podcast_dir, podcast, config, logstring)
                print(podcast_file)
                dl.write(podcast_file + '\n')
            except libxml2.parserError:
                pass
        
        
