import time
import math
import heapq
import minescript
import sys

# All A* and base code from MrPropre's "Astar pathfinder"
#

# adapted to automatically walk by me :)

# feel free to use and update this however you want

# ===================================================================================
# --- START OF A* ALGORITHM ---
# ===================================================================================

# idk how else to make a blocklist but do this atrosity lol
IMPASSABLE_BLOCKS = {"minecraft:water", "minecraft:lava", "minecraft:cactus", "minecraft:fire","minecraft:wither_rose"}
PASASBLE_BLOCKS = {"minecraft:air","minecraft:torch","minecraft:sugar_cane","minecraft:rail","minecraft:detector_rail","minecraft:activator_rail","minecraft:powered_rail","minecraft:short_dry_grass","minecraft:tall_dry_grass","minecraft:tall_grass", "minecraft:short_grass","minecraft:snow","minecraft:soul_torch","minecraft:redstone_wire","minecraft:redstone_torch","minecraft:redstone_wall_torch","minecraft:repeater","minecraft:comparator","minecraft:flower_pot","minecraft:rose_bush","minecraft:poppy","minecraft:allium","minecraft:azalea_bush","minecraft:azure_bluet","minecraft:blue_orchid","minecraft:brown_mushroom","minecraft:closed_eyeblossom","minecraft:cornflower","minecraft:crimson_fungus","minecraft:crimson_roots","minecraft:dandelion","minecraft:fern","minecraft:dead_bush","minecraft:lily_of_the_valley","minecraft:open_eyeblossom","minecraft:orange_tulip","minecraft:oxeye_daisy","minecraft:pink_tulip","minecraft:red_mushroom","minecraft:red_tulip","minecraft:torchflower","minecraft:warped_fungus","minecraft:warped_roots","minecraft:white_tulip","minecraft:acacia_pressure_plate","minecraft:bamboo_pressure_plate","minecraft:birch_pressure_plate","minecraft:cherry_pressire_plate","minecraft:crimson_pressure_plate","minecraft:dark_oak_pressure_plate","minecraft:heavy_weighted_pressure_plate","minecraft:jungle_pressure_plate","minecraft:light_weighted_pressure_plate","minecraft:mangrove_pressure_plate","minecraft:oak_pressure_plate","minecraft:pale_oak_pressure_plate","minecraft:polished_blackstone_pressure_plate","minecraft:spruce_pressure_plate","minecraft:stone_pressure_plate","minecraft:stone_pressure_plate","minecraft:warped_pressure_plate"}


node_timeout = 15
main = __name__ == "__main__"


last_point = (0,0,0)
def lerp(a, b, t): #chatGPT for this stuff, I don't want to deal with tweening bro
    return a + (b - a) * t

def lerp3(p1, p2, t):
    return tuple(lerp(a, b, t) for a, b in zip(p1, p2))

def tweenpointat(location):
    global last_point
    point = last_point
    last_point = lerp3(point, location, .2)
    minescript.player_look_at(*lerp3(point, location, .2))

class Node:
    def __init__(self, parent=None, position=None):
        self.parent, self.position, self.g, self.h, self.f = parent, position, 0, 0, 0

    def __eq__(self, other): return self.position == other.position

    def __lt__(self, other): return self.f < other.f

    def __hash__(self): return hash(self.position)


def _is_walkable(pos, world_data):
    """
    Checks if a position is "walkable" for a 2-block-high entity.
    """
    block_head_pos = (pos[0], pos[1] + 1, pos[2])
    block_feet_pos = pos
    block_support_pos = (pos[0], pos[1] - 1, pos[2])

    block_head = world_data.get(block_head_pos, "air")
    block_feet = world_data.get(block_feet_pos, "air")
    block_support = world_data.get(block_support_pos, "air")

    is_head_clear = "air" in block_head
    is_feet_clear = "air" in block_feet
    is_supported = "air" not in block_support
    is_safe_support = not any(imp in block_support for imp in IMPASSABLE_BLOCKS)

    walkable = is_head_clear and is_feet_clear and is_supported and is_safe_support

    # --- DEBUG LINE ---
    # If the tested block is the destination, print its status.
    if pos == END_POS:
        if main:
            minescript.echo(f"§eDebug for destination {pos}:")
            minescript.echo(
                f"  - Head clear? {is_head_clear}, Feet clear? {is_feet_clear}, Solid support? {is_supported}, Safe support? {is_safe_support}")
            minescript.echo(f"  - Result: Walkable? {'§aYes' if walkable else '§cNo'}")

    return walkable


def find_path(start_pos, end_pos, world_data):
    start_node = Node(None, tuple(map(int, start_pos)))
    end_node = Node(None, tuple(map(int, end_pos)))
    open_heap, closed_set, open_dict = [], set(), {}
    heapq.heappush(open_heap, start_node)
    open_dict[start_node.position] = start_node

    while open_heap:
        current_node = heapq.heappop(open_heap)
        open_dict.pop(current_node.position, None)
        if current_node.position in closed_set: continue
        closed_set.add(current_node.position)

        if current_node == end_node:
            path = [];
            current = current_node
            while current: path.append(current.position); current = current.parent
            return path[::-1]

        (x, y, z) = current_node.position
        # Check all 26 possible neighbors
        for dx, dy, dz in [(dx, dy, dz) for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if
                           not (dx == 0 and dy == 0 and dz == 0)]:
            neighbor_pos = (x + dx, y + dy, z + dz)
            if neighbor_pos in closed_set or not _is_walkable(neighbor_pos, world_data):
                continue

            move_cost = current_node.g + math.sqrt(dx ** 2 + dy ** 2 + dz ** 2) + (0.5 if dy > 0 else 0)
            if neighbor_pos in open_dict and open_dict[neighbor_pos].g <= move_cost:
                continue

            neighbor_node = Node(current_node, neighbor_pos);
            neighbor_node.g = move_cost
            neighbor_node.h = math.sqrt(sum((neighbor_pos[i] - end_node.position[i]) ** 2 for i in range(3)))
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            heapq.heappush(open_heap, neighbor_node);
            open_dict[neighbor_pos] = neighbor_node

    return []


# ===================================================================================
# --- START OF TEST SCRIPT ---
# ===================================================================================

# --- Configuration ---
#START_POS = (374, 71, 267)
END_POS = (377, 73, 257)
VISUALIZE_BLOCK = "minecraft:glowstone"
VISUALIZE_DELAY = 0.05

set_tolerance = 1.9
path = False
def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def retry_scan(START_POS,END_POS,scan_margin):
    global path
    min_x = min(START_POS[0], END_POS[0]) - scan_margin
    max_x = max(START_POS[0], END_POS[0]) + scan_margin
    min_y = min(START_POS[1], END_POS[1]) - scan_margin
    max_y = max(START_POS[1], END_POS[1]) + scan_margin
    min_z = min(START_POS[2], END_POS[2]) - scan_margin
    max_z = max(START_POS[2], END_POS[2]) + scan_margin

    # 1. Create a list of all positions to check.
    positions_to_scan = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                positions_to_scan.append([x, y, z])

    # 2. Make a SINGLE API call to get all block data at once.
    minescript.echo(f"§e[A* Pathfinder] Scanning {len(positions_to_scan)} blocks in one call...")
    block_names_list = minescript.getblocklist(positions_to_scan)

    # 3. Build the world_data dictionary from the results.
    world_data = {}
    for i in range(len(positions_to_scan)):
        block_name = block_names_list[i]
        if block_name not in PASASBLE_BLOCKS:
            # Convert position back to a tuple to use as a dictionary key.
            position_tuple = tuple(positions_to_scan[i])
            world_data[position_tuple] = block_name
    # --- END OF OPTIMISED SCAN ---
    if main:
        minescript.echo("§e[A* Pathfinder] Calculating path...")
    path = find_path(START_POS, END_POS, world_data)
def pathfind_to(pos1, pos2, pos3, sprint):
    global path
    END_POS = (pos1, pos2, pos3)
    global last_point
    if main:
        minescript.echo("§a[A* Pathfinder] Starting demonstration...")
    #minescript.echo(f"§7Start: {START_POS}, End: {END_POS}")

    #print(minescript.player)
    START_POS = minescript.player_position()
    START_POS = [math.floor(n) for n in START_POS]
    # --- OPTIMISED WORLD SCAN ---
    if main:
        minescript.echo("§e[A* Pathfinder] Preparing list of coordinates to scan...")
    scan_margin = 10
    min_x = min(START_POS[0], END_POS[0]) - scan_margin
    max_x = max(START_POS[0], END_POS[0]) + scan_margin
    min_y = min(START_POS[1], END_POS[1]) - scan_margin
    max_y = max(START_POS[1], END_POS[1]) + scan_margin
    min_z = min(START_POS[2], END_POS[2]) - scan_margin
    max_z = max(START_POS[2], END_POS[2]) + scan_margin

    # 1. Create a list of all positions to check.
    positions_to_scan = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                positions_to_scan.append([x, y, z])

    # 2. Make a SINGLE API call to get all block data at once.
    minescript.echo(f"§e[A* Pathfinder] Scanning {len(positions_to_scan)} blocks in one call...")
    block_names_list = minescript.getblocklist(positions_to_scan)

    # 3. Build the world_data dictionary from the results.
    world_data = {}
    for i in range(len(positions_to_scan)):
        block_name = block_names_list[i]
        if block_name not in PASASBLE_BLOCKS:
            # Convert position back to a tuple to use as a dictionary key.
            position_tuple = tuple(positions_to_scan[i])
            world_data[position_tuple] = block_name
    # --- END OF OPTIMISED SCAN ---
    if main:
        minescript.echo("§e[A* Pathfinder] Calculating path...")
    path = find_path(START_POS, END_POS, world_data)

    if not path:
        retry_margin = scan_margin+20
        minescript.echo("§c[A* Pathfinder] Failure: No path could be found.")
        minescript.echo("§e[A* Pathfinder] Retrying with an increased margin.")
        retry_scan(START_POS,END_POS,retry_margin)
        if not path:
            return

    minescript.echo(f"§a[A* Pathfinder] Path found! walking across {len(path)} points...")
    # Note: Visualization is still one command per block and can be slow for long paths.
    #for position in path[1:]:
    #    cmd = f"setblock {position[0]} {position[1]} {position[2]} {VISUALIZE_BLOCK}"
    #    minescript.execute(cmd)
    #    time.sleep(VISUALIZE_DELAY)
    
    for position in path[1:]:
        last_point = (position[0]+.5,position[1]+1.6,position[2]+.5)
        minescript.player_look_at(position[0]+.5,position[1]+1.6,position[2]+.5)
        

        pos_raw = minescript.player_position()



        if path.index(position) == len(path) -1: #last point
            tolerance = .75
        else:
            tolerance = set_tolerance
        last_checkin = 0
        forcequit = False
        while ((abs(pos_raw[0]-position[0]) > tolerance) or not (abs(pos_raw[1]- position[1]) <= 1) or (abs(pos_raw[2] - position[2]) > tolerance)) and not forcequit:
                last_checkin += 1
                pos_raw = minescript.player_position()
                player = minescript.player()

                tweenpointat((position[0]+.5,position[1]+1.6,position[2]+.5))

                #print(pos[0] == position[0])
                #print(pos[1] == position[1])
                #print(pos[2] == position[2])
                #print(pos)
                #print(position[2])
                minescript.player_press_forward(True)
                if sprint:
                    minescript.player_press_sprint(True)

                if player.pitch < -.1:
                    minescript.player_press_jump(True)
                else:
                    minescript.player_press_jump(False)
                if last_checkin > node_timeout: #retry if we're in an infinite loop
                    minescript.player_press_jump(True)
                    minescript.player_press_jump(False) #do this just in case it's a small bit of foliage like leaves ( most  common in my testing)
                    minescript.echo(f"§e[A* Pathfinder] Detected as stuck! Retrying!")
                    pathfind_to(pos1,pos2,pos3,sprint)
                    forcequit = True
                    break
                #time.sleep(0.01)
        if forcequit:
            break
                
                
    minescript.player_press_forward(False)
        
    if sprint:
        minescript.player_press_sprint(False)
    if not forcequit:
        minescript.echo("§a[A* Pathfinder] Arrived at destination!")


if __name__ == "__main__":

        pathfind_to(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]), True)
