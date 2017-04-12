#!/usr/bin/env ruby

require 'shellwords'
require 'rspec'

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

print '<table class="colors sortable">', "\n"
print '<col width="15%"><col width="20%"><col width="15%"><col width="50%">'

print '<tr>'
print '<th class="sorttable_nosort">Swatch</th>', "\n"
print '<th class="clickable">Color name</th>', "\n"
print '<th id="hex" class="hidden">'    # fake column for colors

print '<th class="sorttable_nosort clickable">', "\n"
print   "<span title='Sort by triplet' onclick='sortcol(\"hex\")'>Hex Triplet</span>", "\n"
print   "<img id=\"arrow\" src='css/images/arrow-both.png'/>", "\n"
%w[R G B].each do |letter|
  print "<span title='Sort by #{letter} value' onclick='sortcol(\"#{letter}\")'>#{letter}</span>", "\n"
end
print '</th>', "\n"

print '<th class="sorttable_nosort"><span class="latex">L<sup>a</sup>T<sub>e</sub>X</span></th>', "\n"
print '<th id="R" class="hidden"></th>'
print '<th id="G" class="hidden"></th>'
print '<th id="B" class="hidden"></th>'
print '</tr>'

def to_html(vals)
  print '<tr>', "\n"
  print "<td> <div class=\"swatch\" style=\"background-color: #{vals[1]};\"></div></td>", "\n"
  print '<td>', vals[0], '</td>', "\n"
  print '<td>', vals[1], '</td>', "\n"
  print '<td class="hidden"></td>', "\n" # fake column for colors counterpart

  colorname = vals[0].gsub(%r{.\W.\s\(.*\/.*\)}, '').gsub(/\s/, '').downcase
  # Wikipedia gives these in percents, we want them in
  # decimals between 0.0 and 1.0.
  red = vals[2].gsub(/%/, '').to_i / 100.0
  green = vals[3].gsub(/%/, '').to_i / 100.0
  blue = vals[4].gsub(/%/, '').to_i / 100.0
  colorvalue = "#{red}, #{green}, #{blue}"
  latexcolor = "\\definecolor{#{colorname.tr('#', '')}}{rgb}{#{colorvalue}}"

  print '<td class="latex-definition">', latexcolor, '</td>', "\n"
  print "<td class=\"hidden\">#{red}</td>", "\n"
  print "<td class=\"hidden\">#{green}</td>", "\n"
  print "<td class=\"hidden\">#{blue}</td>", "\n"
  print '</tr>', "\n"
end

def process(line)
  line.gsub!(/^#.*/, '') # remove comments
  return if line =~ /^\s*$/ # skip blank lines
  _tokens = Shellwords.split(line)
  vals = line.split("\t")
  to_html(vals)
end

# Main executable code is the following block
colors = File.open('colors.txt')
colors.each do |line|
  process(line)
end
print '</table>', "\n"
colors.close

class Color
  attr_reader :vals

  def initialize(line)
    @vals = line.split "\t"
  end

  def name
    @vals[0]
  end

  def latex_name
    @vals[0].gsub(%r{.\W.\s\(.*\/.*\)}, '').gsub(/\s/, '').downcase
  end

  def triplet
    @vals[1]
  end

  def red
    @red = vals[2].gsub(/%/, '').to_i / 100.0
  end

  def green
    @red = vals[3].gsub(/%/, '').to_i / 100.0
  end

  def blue
    @red = vals[4].gsub(/%/, '').to_i / 100.0
  end

  def to_html
  end

  def to_haml
  end
end

# TODO: figure out how to handle errors, for example, when
# an empty line or incomplete line is passed in.
RSpec.describe Color do
  it 'instantiates' do
    line = ''
    expect(Color.new(line)).not_to be nil
  end

  let(:line) { 'Air Force blue	#5D8AA8	36%	54%	66%	204°	30%	51%	45%	66%' }
  subject(:color) { Color.new(line) }

  describe 'name' do
    it { expect(color.name).to eq 'Air Force blue' }
  end

  describe 'latex_name' do
    it { expect(color.latex_name).to eq 'airforceblue' }
  end

  describe 'triplet' do
    it { expect(color.triplet).to eq '#5D8AA8' }
  end

  describe 'red' do
    it { expect(color.red).to eq 0.36 }
  end

  describe 'green' do
    it { expect(color.green).to eq 0.54 }
  end

  describe 'blue' do
    it { expect(color.blue).to eq 0.66 }
  end
end
