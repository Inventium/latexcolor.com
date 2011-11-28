#!/bin/sh

echo rsync deployment for latexcolor.com

rsync -essh -vta --cvs-exclude index.html tinoboxc@tinobox.com:public_html/latexcolor
rsync -essh -vta --cvs-exclude sitemap.xml tinoboxc@tinobox.com:public_html/latexcolor
rsync -essh -vta --cvs-exclude robots.txt tinoboxc@tinobox.com:public_html/latexcolor
rsync -essh -vta --cvs-exclude js tinoboxc@tinobox.com:public_html/latexcolor/
rsync -essh -vta --cvs-exclude css tinoboxc@tinobox.com:public_html/latexcolor/
