#!/usr/bin/python

import sys
import pathlib
from pathlib import Path
import unidecode # pip install Unidecode
import re # regex

# define files
dir_path = Path(__file__).resolve().parent
outputfile = open(dir_path/'LatexColors.incl.tex','w')

#what I dont want
bad_chars = r"[\(\)\{\}\<\>\s#'\\]"

def main():
    try:   
        ColorFile = open('colors.txt', 'r')
        colorlines = ColorFile.readlines()
        ColorFile.close()

        outputfile.write('% Input in your TEX project and use color names accoringly.\n')
        outputfile.write('% Colors from: https://github.com/Inventium/latexcolor.com\n\n')
        outputfile.write('% Usage:\n% Required Package:\n% \\RequirePackage[usenames,dvipsnames]{xcolor}\n% Input Colors:\n% \\input{LatexColors.incl.tex} \n\n')
        outputfile.write('% Then use the colors in your document like this: {\\color{airforceblue} This is Air Force Blue}\n\n')
        
        for strLine in colorlines[1:]:
        
            if len(strLine.strip()) > 0:
                ln = strLine.split('\t')
        
                # get color name and hex
                colorname = unidecode.unidecode(ln[0])
                colorname = re.sub(bad_chars, '', colorname, 0, re.MULTILINE | re.IGNORECASE)
                colorname = colorname.lower()
                colorhex  = ln[1].replace('#', '')

                # \definecolor{airforceblue}{HTML}{5d8aa8}
                outputfile.write('\\definecolor{' + colorname + '}{HTML}{' + colorhex + '}	\n')

        outputfile.write('\\endinput')

    except OSError as err:
        print("OS error: {0}".format(err))
    except:
        print('Somme silly error has occured: ' + str(sys.exc_info()[0]))
        outputfile.close()
    else:
        print('All done.')
        outputfile.close()
    


main()
