"""MAIN! Where the magic happens"""
#!/usr/bin/python

from pathlib import Path
import re # regex
import unidecode # pip install Unidecode

# define files
DIR_PATH = Path(__file__).resolve().parent
OUTPUTFILE = open(DIR_PATH/'LatexColors.incl.tex', 'w')
OUTPUTPACKAGE = open(DIR_PATH/'LatexColors.incl.sty', 'w')
OUTPUTCWL = open(DIR_PATH/'LatexColors.incl.cwl', 'w')

# read to colors.text only once
COLORFILE = open('colors.txt', 'r')
COLORLINES = COLORFILE.readlines()
COLORFILE.close()

#what I dont want
BAD_CHARS = r"[\(\)\{\}\<\>\/\s#'\\]"

def main():
    """MAIN! Where the magic happens"""
    try:

        OUTPUTFILE.write('% Input in your TEX project and use color names accoringly.\n')
        OUTPUTFILE.write('% Colors from: https://github.com/Inventium/latexcolor.com\n\n')
        OUTPUTFILE.write('% Usage:\n% Required Package:\n% '\
            r'\RequirePackage[usenames,dvipsnames]{xcolor}' + '\n\n'\
            r'% Input Colors:' + '\n'\
            r'% \input{LatexColors.incl.tex}' + '\n\n')
        OUTPUTFILE.write('% Then use the colors in your document like this:'\
            r'{\color{airforceblue} This is Air Force Blue}' + '\n\n')

        for strline in COLORLINES[1:]:

            if strline.strip():
                # get color name and hex
                colname = colorname(strline)

                # \definecolor{airforceblue}{HTML}{5d8aa8}
                OUTPUTFILE.write(r'\definecolor{' + colname[0] + '}{HTML}{' + colname[1] + '}\n')

        OUTPUTFILE.write('\\endinput')

    except OSError as err:
        print("OS error: {0}".format(err))
    except Exception as ex:
        print(str(ex))
        OUTPUTFILE.close()
    else:
        print('Include file written.')
        OUTPUTFILE.close()


def package():
    """Writes the package file"""
    try:

        OUTPUTPACKAGE.write('% Input in your TEX project and use color names accoringly.\n')
        OUTPUTPACKAGE.write('% Colors from: https://github.com/Inventium/latexcolor.com\n\n')
        OUTPUTPACKAGE.write('% Usage:\n' + r'% \usepackage{LatexColors.incl}' + '\n\n')
        OUTPUTPACKAGE.write('% Then use the colors in your document like this: '\
            r'{\tcolor{airforceblue} This is Air Force Blue}' + '\n\n')

        OUTPUTPACKAGE.write(r'\NeedsTeXFormat{LaTeX2e}[1994/06/01]' + '\n'\
            r'\ProvidesPackage{LatexColors.incl}[2018/9/11 ver 1.0]' + '\n'\
            r'\PassOptionsToPackage{usenames,dvipsnames}{xcolor}' + '\n\n')

        OUTPUTPACKAGE.write(r'\newcommand{\tcolor}[1]{\color{#1}}' + '\n\n')

        for strline in COLORLINES[1:]:

            if strline.strip():

                # get color name and hex
                colname = colorname(strline)

                # \definecolor{airforceblue}{HTML}{5d8aa8}
                OUTPUTPACKAGE.write(r'\definecolor{' + colname[0] + '}{HTML}{' + colname[1] + '}\n')

        OUTPUTPACKAGE.write(r'\endinput')

    except OSError as err:
        print("OS error: {0}".format(err))
    except Exception as ex:
        print(str(ex))
        OUTPUTPACKAGE.close()
    else:
        print('Package file written.')
        OUTPUTPACKAGE.close()


def colorname(line):
    """Gets the color name"""
    strline = line.split('\t')

    # get color name and hex
    clname = unidecode.unidecode(strline[0])
    clname = re.sub(BAD_CHARS, '', clname, 0, re.MULTILINE | re.IGNORECASE)
    clname = clname.lower()

    hexcol = strline[1].replace('#', '')
    return (clname, hexcol.upper(), strline[0])


def cwl():
    """make the CWL file for TeXstudio"""
    try:
        OUTPUTCWL.write('# LatexColors.incl package\n')
        OUTPUTCWL.write(r'\tcolor{keyvals}' + '\n')
        OUTPUTCWL.write(r'#keyvals:\tcolor' + '\n')

        for strline in COLORLINES[1:]:

            if strline.strip():
                # get color name and hex
                colname = colorname(strline)

                # \definecolor{airforceblue}{HTML}{5d8aa8}
                OUTPUTCWL.write(colname[0]+'\n')

        OUTPUTCWL.write('#endkeyvals')

    except OSError as err:
        print("OS error: {0}".format(err))
    except Exception as ex:
        print(str(ex))
        OUTPUTCWL.close()
    else:
        print('CWL file written.')
        OUTPUTCWL.close()


main()
package()
cwl()
