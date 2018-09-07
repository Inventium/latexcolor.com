#!/usr/bin/python

import sys
import pathlib
from pathlib import Path
import unidecode # pip install Unidecode


# define files
dir_path = Path(__file__).resolve().parent
outputfile = open(dir_path/'LatexColors.incl.tex','w')


def main():
    try:   
        ColorFile = open('colors.txt', 'r')
        colorlines = ColorFile.readlines()
        ColorFile.close()

        outputfile.write('% Input in your TEX project and use color names accoringly.\n')
        outputfile.write('% Colors from: https://github.com/Inventium/latexcolor.com\n')
        outputfile.write('% Usage:\n% Required Package: \\RequirePackage[usenames,dvipsnames]{xcolor}\n% Input Colors:     \\input{LatexColors.incl.tex} \n\n')

        for strLine in colorlines[1:]:
        
            if len(strLine.strip()) > 0:
                ln = strLine.split('\t')
        
                # get color name and hex
                colorname = unidecode.unidecode(ln[0].replace(' ', '').replace("\\'","").replace('#','No').lower())
                colorhex  = ln[1].replace('#', '')

                # \definecolor{airforceblue}{rgb}{0.36, 0.54, 0.66} % Air Force blue #5D8AA8
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
