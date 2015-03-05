#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import colors
import json
import sys
import re

from manpage import ManPage

from bs4 import *

processed_pages_dir = "../processed-pages"

manpages = dict.fromkeys([1, 2, 3, 4, 5, 6, 7, 8], [])

for root, dirs, files in os.walk("./"):
	for directory in dirs:
		dirlist = []
		outdir = os.path.join(processed_pages_dir, directory)
		if not os.path.exists(outdir):
				os.makedirs(outdir)
		for file in os.listdir(directory):
			if file.endswith(".html"):
				# print "Processing " + directory + "/" + file
				inpage = open(os.path.join(directory,file), "r")
				soup = BeautifulSoup(inpage.read())
				# Remove navheader
				try:
					soup.find_all("div", class_="navheader")[0].extract()
				except Exception, e:
					print >> sys.stderr, colors.error(directory + "/" + file + " does not have header")
					pass
				# Remove license
				try:
					soup.find_all("div", class_="license")[0].extract()
				except Exception, e:
					print >> sys.stderr, colors.error(directory + "/" + file + " does not have license")
				# Extract Description
				cmd, description = soup.select(".refnamediv p")[0].string.split(u"—")
				description = re.sub("\s\s+" , " ", description)
				description = re.sub("\n" , "", description)
				# Remove onload attr
				del soup.find("body")['onload']
				inpage.close()
				outpage = open(os.path.join(outdir, file), "w+")
				outpage.write(soup.prettify(formatter="html").encode('utf-8'))
				outpage.close()
				# Create a new object and add it to the list
				dirlist.append(ManPage(file.split(".")[0], directory, directory[-1], file[:-5], description))
		if directory.startswith("html"):
			manpages[int(directory[-1])] = dirlist

# Sort the manpages by name
# print [len(manpage) for section, manpage in manpages.items()]
[manpage.sort() for section, manpage in manpages.items()]
print json.dumps(manpages, default=lambda o: o.__dict__)