#!/usr/bin/ruby
# Quick and dirty template processing script. It takes
# as an argument the name of the first template script
# and then executes it to standard output.

require "erb"


class QuickTemplate
   attr_reader :args, :text
   def initialize(file)
      @text = File.read(file)
   end
   def exec(args={})
      b = binding
      template = ERB.new(@text, 0, "%<>")
      result = template.result(b)
      # Chomp the trailing newline
      result.gsub(/\n$/,'')
   end
end

def erb(file, args={})
   QuickTemplate.new(file).exec(args)
end

puts erb(ARGV[0])


