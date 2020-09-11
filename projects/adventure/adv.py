from room import Room
from player import Player
from world import World
from util import Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "c:/Users/defaultuser/Desktop/Lambda/Graphs/projects/adventure/maps/test_line.txt"
# map_file = "c:/Users/defaultuser/Desktop/Lambda/Graphs/projects/adventure/maps/test_cross.txt"
# map_file = "c:/Users/defaultuser/Desktop/Lambda/Graphs/projects/adventure/maps/test_loop.txt"
# map_file = "c:/Users/defaultuser/Desktop/Lambda/Graphs/projects/adventure/maps/test_loop_fork.txt"
map_file = "c:/Users/defaultuser/Desktop/Lambda/Graphs/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# method returns a random unvisited direction by checking for ?
def random_unvisited_dir(room, graph):
    moves = []
    for key, value in graph[room].items():
        if value == "?":
            moves.append(key)
    if len(moves) == 0:
        return None
    else:
        return random.choice(moves)

# method returns a graph that gets rid of all None type rooms
def unneeded_dir(room, graph):
    moves = []
    for key, value in graph[room].items():
        if value == "?":
            unneeded = world.rooms[room].get_room_in_direction(key)
            if unneeded == None:
                moves.append(key)
    for i in moves:
        del graph[room][i]
    return graph

# method just returns opposites
def opposite(dir):
    if dir == "n":
        return "s"
    elif dir == "s":
        return "n"
    elif dir == "w":
        return "e"
    elif dir == "e":
        return "w"

# uses a dft to find the furthest rooms
def dft(graph, loc):
    commands = []
    current = loc
    needed_dir = unneeded_dir(loc, graph)
    next_dir = random_unvisited_dir(current, needed_dir)
    while next_dir is not None:
        player.travel(next_dir)
        new_loc = player.current_room.id
        if new_loc == current:
            del needed_dir[current][next_dir]
            next_dir = random_unvisited_dir(current, needed_dir)
        else:
            if new_loc not in needed_dir:
                needed_dir[new_loc] = {"n": "?", "s": "?", "w": "?", "e": "?"}
            commands.append(next_dir)
            needed_dir[current][next_dir] = new_loc
            needed_dir[new_loc][opposite(next_dir)] = current
            current = player.current_room.id
            next_dir = random_unvisited_dir(current, needed_dir)
    return commands, needed_dir, current

# returns possible rooms to enter for bfs
def bfs_helper(room, graph):
    moves = []
    for i in graph[room].items():
        moves.append(i[1])
    return moves

# looks through all the rooms for possible entries
def bfs(graph, starting_room):
    commands = []
    shortest_path = []
    q = Queue()
    q.enqueue([starting_room])
    visited = set()
    flag = False
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            if v == "?":
                shortest_path.append(path[:-1])
            else:
                visited.add(v)
                for n in bfs_helper(v, graph):
                    if n not in visited:
                        q.enqueue(path + [n])
    # shortest path would be the spot currently standing which means fully visited
    if len(shortest_path) == 0:
        flag = True
    else:
        # looks for the smallest room in shortest path and checks each direction travelable
        for loc in min(shortest_path, key=len):
            for key, value in graph[player.current_room.id].items():
                if value == loc:
                    commands.append(key)
                    player.travel(key)
        if player.current_room == starting_room:
            commands = []
    return commands, player.current_room.id, flag

# runs all the code
def create_path():
    commands = []
    graph = {0: {"n": "?", "s": "?", "w": "?", "e": "?"}}
    current = world.rooms[0].id
    visited = set()
    visited.add(0)
    flag = False
    while flag == False:
        dft_commands, needed_dir, current = dft(graph, current)
        commands += dft_commands
        graph = needed_dir
        bfs_commands, current, flag2 = bfs(needed_dir, current)
        if flag2 == True:
            # flag2 being true means that everything is visited. if it is not, it will add the remaining commands
            flag = True
        else:
            commands += bfs_commands
    return commands

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = create_path()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
