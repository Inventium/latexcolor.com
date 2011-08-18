#!/usr/bin/env ruby

require 'shellwords'

# 1. Pulled the information from wikipedia as 
# copy and paste into a text file colors.txt
#
# 2. Poked and prodded at the file with Ruby.
# Found most things I wanted to do astoundingly easy.
# Ruby "just works."  Even stuff that's a little odd,
# once I use it, it seems to make perfect sense.
# 
# 3. Figured out the regular expression using rubular.
# 
# 4. Tested various labels for the definecolor 
# command LaTeX.  LaTeX will take some very strange
# looking strings as valid labels.  Also tested the 
# labels in my preferred source code formatting package,
# lstlisting.
# 
# 5. Created the output html page. Simple stuff
# which I've been doing a long time.  
#
# 6. Used Blueprint CSS and Typekit to gussy it all up.
# 
# todo: learn if Blueprint can be stripped, and if so, 
# figure out how to strip it.
#
# Total time on the project: 3-4 hours.  Had to learn
# a few new things about Ruby.
# 
# Blog post or standalone website for final table.
# Check out http://jonraasch.com/ 

## Here's how to get rid of the "%" sign:
## a = "83%"
## b = a.gsub(/%/,'').to_i
## You can do math on b now.

# Try this: gsub(/[^A-Za-z\(\)]/,'') 
# "Amy's (hoo/ha)".gsub(/[^A-Za-z\(\)\/]/,'').downcase


def line_empty?(line)
  true
end

print "<table class=\"colors\">", "\n"
print "<th>Swatch</th>", "\n"
print "<th>Color name</th>", "\n"
print "<th>Hex Triplet</th>", "\n"
print "<th><span class=\"latex\">L<sup>a</sup>T<sub>e</sub>X</span></th>", "\n"

colors = File.open("colors.txt")

colors.lines.each do |line|
 
#  if line_empty?(line)
#   puts "Empty line..."
# end
  line.gsub!(/^#.*/, '') # remove comments
  next if line =~ /^\s*$/ # skip blank lines

  # match newline at beginning of line:
  # gsub(/^./m,''), but we want to continue without processing
  # Consider using chomp  


    print "<tr>", "\n"
    tokens = Shellwords.split(line)
    vals = line.split("\t")

    #print vals[0], "\t\t\t", vals[1], "\t", vals[2], "\n"
    #print vals[0].gsub(/'\s/,'').downcase, "\n"
    # From rubular... hideous... probably going to need to 
    # do this in stages... don't care about performance here...

    # First, a nice web 2.0-ey roundey thingey...
    print "<td> <div class=\"swatch\" style=\"background-color: #{vals[1]};\"></div></td>", "\n"
    print "<td>", vals[0], "</td>", "\n"
    #print "<td style=\"background-color: #{vals[1]};\">", vals[1], "</td>", "\n"
    print "<td>", vals[1], "</td>", "\n"
    colorname = vals[0].gsub(/.\W.\s\(.*\/.*\)/,'').gsub(/\s/,'').downcase

    # Wikipedia gives these in percents, we want them in 
    # decimals between 0.0 and 1.0.
    red = vals[2].gsub(/%/,'').to_i / 100.0
    green = vals[3].gsub(/%/,'').to_i / 100.0
    blue = vals[4].gsub(/%/,'').to_i / 100.0
    colorvalue = "#{red}, #{green}, #{blue}" 


    latexcolor = "\\definecolor{#{colorname}}%<br />{rgb}{#{colorvalue}}"
    print "<td class=\"latex-definition;\">", latexcolor, "</td>","\n"


    #print "<td class=\"latex-definition;\">\\definecolor{#{colorname}}%<br />"
    #print "{rgb}{#{colorvalue}}", "</td>","\n"




  print "</tr>", "\n"

  # parse the token out...
end

print "</table>", "\n"



colors.close
