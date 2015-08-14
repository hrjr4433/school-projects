path = ARGV[0]
if path.nil?
    puts "Usage: ruby rotator.rb path from current folder"
    exit
end
raise "No such file exists" if path == ""

file = File.read(path).split("\n")
t = file.shift.to_i
t.times do
    n,m = file.shift.split(" ").map! {|i| i.to_i }
    edges = Hash.new
    visited = Hash.new
    1.upto(n) {|i| edges[i] = []; visited[i] = -1 }
    m.times do |nodes|
        x,y = file.shift.split(" ").map! {|i| i.to_i }
        edges[x] << y unless edges[x].include? y
        edges[y] << x unless edges[y].include? x
    end
    start = file.shift.to_i
    
    queue = [start]
    edge = 0
    remaining_in_level = 0
    loop do
        node = queue.shift
        visited[node] = edge unless visited[node] > 0
        queue.push(*edges.delete(node)) if edges.has_key? node
        break if queue.empty?
        if remaining_in_level == 0
            edge += 1
            remaining_in_level = queue.length
        else
            remaining_in_level -= 1
        end
    end
    visited.delete(start)
    puts visited.values.map! {|i| i > 0 ? i*6 : i}.join(" ")
end