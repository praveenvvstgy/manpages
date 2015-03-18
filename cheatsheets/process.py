#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import colors
import json
import sys
import re

from cheatsheet import CheatSheet
import markdown2
from bs4 import *


output_cheatsheet_dir = "./output"

cheatsheets = []

output_header = ""

for root, dirs, files in os.walk("./tldr/pages"):
	for directory in dirs:
		platform = directory
		directory = "./tldr/pages/" + directory
		outdir = output_cheatsheet_dir
		if not os.path.exists(outdir):
				os.makedirs(outdir)
		for file in os.listdir(directory):
			if file.endswith(".md"):
				# print "Processing " + file
				inpage = open(os.path.join(directory,file), "r")
				# Convert to HTML file
				html = markdown2.markdown_path(directory + "/" + file)
				html = '<!doctype html><html> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="style.css"> </head> <body> <article class="markdown-body"> ' + html + ' </article> </body></html>'
				soup = BeautifulSoup(html)
				for code in soup.find_all("code"):
					code.wrap(soup.new_tag("pre"))
				inpage.close()
				description = soup.blockquote.p.string
				outpage = open(os.path.join(outdir, file.split(".")[0] + ".html"), "w+")
				outpage.write(soup.prettify(formatter="html").encode('utf-8'))
				outpage.close()
				# Create a new object and add it to the list
				cheatsheets.append(CheatSheet(file.split(".")[0], file.split(".")[0] + ".html", description, platform))

# Sort the cheatsheets by name
cheatsheets.sort()
print json.dumps(cheatsheets, default=lambda o: o.__dict__)
os.system("cp style.css " + output_cheatsheet_dir)