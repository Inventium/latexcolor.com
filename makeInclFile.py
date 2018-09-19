#!/usr/bin/python

import sys
import pathlib
from pathlib import Path
import unidecode # pip install Unidecode
import re # regex

# define files
dir_path = Path(__file__).resolve().parent
outputfile = open(dir_path/'LatexColors.incl.sty','w')
cwloutput = open(dir_path/'LatexColors.incl.cwl','w')


#what I dont want
bad_chars = r"[\(\)\{\}\<\>\s#'\\/]"

def main():
    try:
        ColorFile = open('colors.txt', 'r')
        colorlines = ColorFile.readlines()
        ColorFile.close()

        outputfile.write('% --- Usage ---\n')
        outputfile.write('% Write in your premable:\n')
        outputfile.write('% \\usepackage{LatexColors.incl}\n\n')
        outputfile.write('% Then use the colors in your document like this: {\\tcolor{airforceblue} This is Air Force Blue}\n\n')

        outputfile.write('\\NeedsTeXFormat{LaTeX2e}[1994/06/01]\n')
        outputfile.write('\\ProvidesPackage{LatexColors.incl}[2018/9/11 ver 1.0]\n')
        outputfile.write('\\PassOptionsToPackage{usenames,dvipsnames}{xcolor}\n\n')
        outputfile.write('\\newcommand{\\tcolor}[1]{\\color{#1}}\n\n')
        outputfile.write('% Colors from: https://github.com/Inventium/latexcolor.com\n\n')

        cwloutput.write('# LatexColors.incl package\n#\\tcolor{keyvals}\n#keyvals:\\tcolor\n')

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

                cwloutput.write(colorname + '\n')

        outputfile.write('\\endinput')
        cwloutput.write('#endkeyvals')

    except OSError as err:
        print('OS error: {0} in {1}\n{2}'.format(err, err.filename, err.message))
    except Exception as ex:
        print (str(ex))
        outputfile.close()
        cwloutput.close()
    else:
        print('All done.')
        outputfile.close()
        cwloutput.close()





main()
