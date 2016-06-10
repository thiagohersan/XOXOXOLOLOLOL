#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, system
from os.path import join, isdir
from time import sleep
from re import sub

if __name__ == "__main__":
    DATA_DIR = "./texts"
    HTML_TEMPLATE = "template.html"
    BOOK_NAME = "xoxoxolololol"
    TOC_TAG = "<!-- !!! TOCTOCTOC !!! -->"
    BODY_TAG = "<!-- !!! BODYBODY !!! -->"

    BODY = ""
    TOC = ""
    idx = 0

    for txtDir in [f for f in sorted(listdir(DATA_DIR)) if isdir(join(DATA_DIR, f))]:
        thisDir = join(DATA_DIR, txtDir)
        thisHeading = sub(r"[0-9]+", "", txtDir).title()

        #TOC += "            <h3>%s</h3>\n"%thisHeading
        TOC += "            <ul class=\"toc\">\n"


        for filename in [f for f in sorted(listdir(thisDir)) if f.endswith(".txt")]:
            fullPath = join(thisDir, filename)
            print "PROCESSING: %s"%fullPath

            cHtml = ""
            cTitle = ""
            cAuthor = ""

            # expand the html and add to TOC list
            with open(fullPath) as txt:
                for line in txt.read().splitlines():
                    if cTitle is "":
                        titleAuthor = line.split(":")
                        cTitle = titleAuthor[0].strip()
                        cAuthor = titleAuthor[-1].strip()
                        TOC += "				<li><a href=\"#ch%s\">%s</a></li>\n"%(str(idx), cTitle)
                    elif "images/" in line:
                        if cHtml is "":
                            cHtml += "        <div id=\"ch%s\" class=\"projcover\">\n"%str(idx)
                            cHtml += "            <img src=%s />\n"%line
                            cHtml += "            <h2>%s<br /><span id=\"author\">%s</span></h2>\n"%(cTitle, cAuthor)
                            cHtml += "        </div>\n"
                            cHtml += "        <div class=\"chapter\">\n" 
                            cHtml += "        <h1 class=\"chapter-title\">%s</h1>\n"%cTitle
                        else:
                            cHtml += "        <div class=\"projcover\">\n"
                            cHtml += "            <img src=%s />\n"%line
                            cHtml += "        </div>\n"
                    else:
                        cHtml += "        %s\n"%line
                txt.close()

            if cHtml is not "":
                cHtml += "        </div>\n"
                BODY += cHtml
                
            idx += 1

        # close TOC
        TOC += "            </ul>\n"

    # write output file
    with open(BOOK_NAME+".html", 'w') as out, open(HTML_TEMPLATE) as temp:
        for line in temp.readlines():
            if TOC_TAG in line:
                line = TOC
            if BODY_TAG in line:
                line = BODY
            out.write(line)
        out.close()
        temp.close()

    # make pdf
    system("prince -s style.css %s.html -o %s.pdf"%(BOOK_NAME,BOOK_NAME))
    #system("pdf2ps %s.pdf %s.ps"%(BOOK_NAME,BOOK_NAME))
    #system("rm -rf %s.pdf"%(BOOK_NAME))
    #system("ps2pdf %s.ps %s.pdf"%(BOOK_NAME,BOOK_NAME))
    #system("rm -rf %s.ps"%(BOOK_NAME))
