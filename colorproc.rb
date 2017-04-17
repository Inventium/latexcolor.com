#!/usr/bin/env ruby
# frozen_string_literal: true

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

# rubocop:disable Metrics/AbcSize
# rubocop:disable MethodLength
def table_header
  print '<table class="colors sortable">', "\n"
  print '<col width="15%"><col width="20%"><col width="15%"><col width="50%">'

  print '<tr>'
  print '<th class="sorttable_nosort">Swatch</th>', "\n"
  print '<th class="clickable">Color name</th>', "\n"
  print '<th id="hex" class="hidden">' # fake column for colors

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
end
# rubocop:enable Metrics/AbcSize
# rubocop:enable MethodLength

def process(line)
  line.gsub!(/^#.*/, '') # remove comments
  return if line.match?(/^\s*$/) # skip blank lines
  color = Color.new line
  color.to_html
end

# Color class takes a line from tab-delimited color data
# and produces the appropriate html output.
# TODO: rename to HtmlColorTable
class Color
  attr_reader :vals

  def initialize(line)
    @vals = line.split "\t"
  end

  def name
    @name ||= @vals[0]
  end

  def latex_name
    @latex_name ||= name.gsub(%r{.\W.\s\(.*\/.*\)}, '').gsub(/\s/, '').downcase
  end

  def triplet
    @triplet ||= @vals[1]
  end

  def red
    @red ||= vals[2].delete('%').to_i / 100.0
  end

  def green
    @green ||= vals[3].delete('%').to_i / 100.0
  end

  def blue
    @blue ||= vals[4].delete('%').to_i / 100.0
  end

  def colorvalue
    @colorvalue ||= "#{red}, #{green}, #{blue}"
  end

  def latex_color
    @latex_color ||= "\\definecolor{#{latex_name.tr('#', '')}}{rgb}{#{colorvalue}}"
  end

  # rubocop:disable Metrics/AbcSize MethodLength
  def to_html
    print '<tr>', "\n"
    print "<td> <div class=\"swatch\" style=\"background-color: #{triplet};\"></div></td>", "\n"
    print '<td>', name, '</td>', "\n"
    print '<td>', triplet, '</td>', "\n"
    print '<td class="hidden"></td>', "\n" # fake column for colors counterpart
    print '<td class="latex-definition">', latex_color, '</td>', "\n"
    print "<td class=\"hidden\">#{red}</td>", "\n"
    print "<td class=\"hidden\">#{green}</td>", "\n"
    print "<td class=\"hidden\">#{blue}</td>", "\n"
    print '</tr>', "\n"
  end
  # rubocop:enable Metrics/AbcSize MethodLength

  def to_haml; end
end

# Main executable code is the following block
# TODO: move this to a script in a bin directory
table_header
colors = File.open('colors.txt')
colors.each do |line|
  process(line)
end
print '</table>', "\n"
colors.close

# TODO: figure out how to handle errors, for example, when
# an empty line or incomplete line is passed in.
# rubocop:disable BlockLength
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

  describe 'colorvalue' do
    it { expect(color.colorvalue).to eq '0.36, 0.54, 0.66' }
  end

  describe 'latex_color' do
    it { expect(color.latex_color).to eq '\\definecolor{airforceblue}{rgb}{0.36, 0.54, 0.66}' }
  end
end
# rubocop:enable BlockLength
