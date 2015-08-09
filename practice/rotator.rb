#  Author: Jaehyuk Lee
#  Date: 8/9/2015
#  Each ring of 2d array matrix rotate by one element
#
#
#  example:
#          1 2 3 4 5
#          6 7 8 9 0
#  after shift:
#          6 1 2 3 4 5
#          7 8 9 0
# after pop:
#          6 1 2 3 4
#          7 8 9 5 0
########################
path = ARGV[0]
if path.nil?
	puts "Usage: ruby rotator.rb path from current folder"
	exit
end
raise "No such file exists" if path == ""

file = File.read(path).split("\n")
n = file.shift.to_i
half = n/2
raise "the first line is either 0 or not integer" if n == 0

matrix = Array.new
# first iteration
shift = 0
pop = 0
file.each_with_index do |line, i|
	row = line.split(" ")
	shift.times do |s|
		matrix[i-1].insert(s, row.shift)
	end
	shift += i < half ? 1 : -1
	shift += 1 if n.odd? and i == half

	last_i = row.length
	pop.times do |s|
		row.insert(last_i-shift, matrix[i-1].pop)
	end
	pop += i < half ? 1 : -1
	pop += 1 if n.odd? and i == half
	matrix << row
end

n.times {|i| puts matrix[i].join(" ")}