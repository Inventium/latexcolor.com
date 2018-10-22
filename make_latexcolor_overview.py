#!/usr/bin/python3

"""
    MAIN! Where the magic happens
"""


from pathlib import Path
import re # regex
import unicodedata

#import last:
import unidecode # pip install Unidecode


# define files
DIR_PATH = Path(__file__).resolve().parent
OUTPUTOVERVIEW = open(DIR_PATH/'LatexColors.Overview.tex', 'w')

# read to colors.text only once
COLORFILE = open('colors.txt', 'r')
COLORLINES = COLORFILE.readlines()
COLORFILE.close()

#what I dont want
BAD_CHARS = r"[\(\)\{\}\<\>\/\s#'\\]"
BAD_CHARS_NAME = r"[\(\)\{\}\<\>\/#'\\]"

def main():
    """MAIN! Where the magic happens"""
    try:

        OUTPUTOVERVIEW.write(r'\documentclass[12pt,a4paper,twocolumn]{article}'+'\n\n'\
            r'\usepackage[utf8x]{inputenc}'+'\n'\
            r'\usepackage{graphicx}'+'\n'\
            r'\usepackage{tikz}'+'\n'\
            r'\usepackage[left=2.5cm, right=1cm, top=1.5cm, bottom=2cm]{geometry}'+'\n'\
            r'\usepackage{xcolor}'+'\n'\
            r'\usepackage{siunitx}'+'\n'\
            r'\usepackage{titlesec}'+'\n'\
            r'\titleformat{\section}{\Large\scshape}{\thesection}{1em}{}'+'\n'\
            r'\titlespacing{\section}{0pt}{12pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}'+'\n'\
            r'\setlength{\parindent}{0pt}'+'\n'\
            r'\usepackage{LatexColors.incl}'+'\n'\
            r'\begin{document}'+'\n' + '\n')

        startletter = ''
        for strline in COLORLINES[1:]:

            if strline.strip():
                # get color name and hex
                colname = colorname(strline)

                if startletter != strline[:1]:
                    startletter = strline[:1]
                    OUTPUTOVERVIEW.write(r'\section*{' + startletter +'}\n')

                # get RBG
                rcol, gcol, bcol = tuple(int(colname[1][i:i+2], 16) for i in (0, 2, 4))

                # \definecolor{airforceblue}{HTML}{5d8aa8}
                clname = strip_accents(re.sub(BAD_CHARS_NAME, '',\
                    colname[2], 0, re.MULTILINE | re.IGNORECASE)).title()

                rcol = rcol/255.
                gcol = gcol/255.
                bcol = bcol/255.

                cmyk = convert_rgb_cmyk(rcol, gcol, bcol)
                hsv = convert_rgb_hsv(rcol, gcol, bcol)
                hsl = convert_rgb_hsl(rcol, gcol, bcol)

                OUTPUTOVERVIEW.write(r'\begin{minipage}{\linewidth}\tikz[baseline=1mm]\draw [fill='\
                    + colname[0] + r', rounded corners=5pt] (0,0) rectangle (2cm,1cm); {\textbf{'\
                    + clname + r'} \\ \scriptsize{'+'RGB: {0:.0f}, {1:.0f}, {2:.0f}'\
                    .format(*tuple(int(colname[1][i:i+2], 16) for i in (0, 2, 4))) + r'; ' + \
                    r'HEX:~\#' + colname[1] + r'\\' + \
                    r'CMYK: \SI{{{0:.1f}}}{{\percent}}, \SI{{{1:.1f}}}{{\percent}}, '
                    r'\SI{{{2:.1f}}}{{\percent}}, \SI{{{3:.1f}}}{{\percent}}'\
                    .format(cmyk[0]*100, cmyk[1]*100, cmyk[2]*100, cmyk[3]*100) + r' \\' + \
                    r'HSV: \SI{{{0:.0f}}}{{\degree}}, \SI{{{1:.1f}}}{{\percent}}, '
                    r'\SI{{{2:.1f}}}{{\percent}}'\
                    .format(hsv[0], hsv[1]*100, hsv[2]*100) + r' \\' + \
                    r'HSL: \SI{{{0:.0f}}}{{\degree}}, \SI{{{1:.1f}}}{{\percent}}, '
                    r'\SI{{{2:.1f}}}{{\percent}}'\
                    .format(hsl[0], hsl[1]*100, hsl[2]*100)\
                    + '}}\n'\
                    r'\vspace{.5em}\end{minipage}' + '\n')

        OUTPUTOVERVIEW.write(r'\end{document}')

    except OSError as err:
        print("OS error: {0}".format(err))
    # except Exception as ex: #comment for pylint 10.0!
        # print(str(ex))
    else:
        print('Overview file written.')
        OUTPUTOVERVIEW.close()
def convert_rgb_hsl(rcol, gcol, bcol):
    """
        Convert RGB% to HSL
        see https://www.rapidtables.com/convert/color/rgb-to-hsl.html
        and http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
    """

    mxi = max(rcol, gcol, bcol)
    mni = min(rcol, gcol, bcol)

    lcol = (mxi+mni)/2
    d_f = mxi-mni
    if mxi == mni:
        hcol = 0
    elif mxi == rcol:
        hcol = (60 * ((gcol-bcol)/d_f) + 360) % 360
    elif mxi == gcol:
        hcol = (60 * ((bcol-rcol)/d_f) + 120) % 360
    elif mxi == bcol:
        hcol = (60 * ((rcol-gcol)/d_f) + 240) % 360
    if d_f == 0:
        scol = 0
    else:
        scol = d_f/(1-abs(2*lcol-1))

    return hcol, scol, lcol


def convert_rgb_hsv(rcol, gcol, bcol):
    """
        Convert RGB% to HSV
        see http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
        for more information
    """

    mxi = max(rcol, gcol, bcol)
    mni = min(rcol, gcol, bcol)

    d_f = mxi-mni
    if mxi == mni:
        hcol = 0
    elif mxi == rcol:
        hcol = (60 * ((gcol-bcol)/d_f) + 360) % 360
    elif mxi == gcol:
        hcol = (60 * ((bcol-rcol)/d_f) + 120) % 360
    elif mxi == bcol:
        hcol = (60 * ((rcol-gcol)/d_f) + 240) % 360
    if mxi == 0:
        scol = 0
    else:
        scol = d_f/mxi
    vcol = mxi
    return hcol, scol, vcol


def convert_rgb_cmyk(rcol, gcol, bcol):
    """
        Converts RGB% to CMYK
        See https://www.rapidtables.com/convert/color/rgb-to-cmyk.html
        for more information
    """
    if (rcol == 0) and (gcol == 0) and (bcol == 0):
        # black
        return 0, 0, 0, 1

    kcol = 1-max(rcol, gcol, bcol)
    ccol = (1-rcol-kcol)/(1-kcol)
    mcol = (1-gcol-kcol)/(1-kcol)
    ycol = (1-bcol-kcol)/(1-kcol)

    return ccol, mcol, ycol, kcol


def strip_accents(text):
    """
        Strip accents from input String.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


# function takes in a hex color and outputs it inverted
def invert(color_to_convert):
    """
        Inverts hex color
        see https://stackoverflow.com/a/31607735/827526
    """
    table = str.maketrans('0123456789abcdef', 'fedcba9876543210')
    return color_to_convert[0:].upper().translate(table).upper()


def colorname(line):
    """
        Gets the color name
    """
    strline = line.split('\t')

    # get color name and hex
    clname = unidecode.unidecode(strline[0])
    clname = re.sub(BAD_CHARS, '', clname, 0, re.MULTILINE | re.IGNORECASE)
    clname = clname.lower()

    hexcol = strline[1].replace('#', '')
    return (clname, hexcol.upper(), strline[0])


main()
