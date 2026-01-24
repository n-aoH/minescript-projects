import dearpygui.dearpygui as dpg
from os import chdir
import threading
from time import sleep


try:
    chdir("minescript") #Maybe they'll update it in the future idk
except:
    pass


from minescript import *

FONT = "FunnelSans-Medium.ttf"
FONT_SIZE = 20
height = 900
width = 600
SLEEP_TIME = .5
TOGGLE_HOVER = True


HOSTILE_MOBCAP_MOBS = [
    "entity.minecraft.blaze",
    "entity.minecraft.creeper",
    "entity.minecraft.drowned",
    "entity.minecraft.elder_guardian",     
    "entity.minecraft.endermite",
    "entity.minecraft.evoker",
    "entity.minecraft.ghast",
    "entity.minecraft.guardian",
    "entity.minecraft.hoglin",
    "entity.minecraft.husk",
    "entity.minecraft.magma_cube",
    "entity.minecraft.phantom",
    "entity.minecraft.piglin_brute",
    "entity.minecraft.pillager",
    "entity.minecraft.ravager",
    "entity.minecraft.shulker",
    "entity.minecraft.silverfish",
    "entity.minecraft.skeleton",
    "entity.minecraft.stray",
    "entity.minecraft.vex",
    "entity.minecraft.vindicator",
    "entity.minecraft.warden",
    "entity.minecraft.witch",
    "entity.minecraft.wither_skeleton",
    "entity.minecraft.zoglin",
    "entity.minecraft.zombie",
    "entity.minecraft.zombie_villager",
    "entity.minecraft.zombified_piglin",
]


dpg.create_context()
try:
    with dpg.font_registry():
        default_font = dpg.add_font(FONT, FONT_SIZE)

    dpg.bind_font(default_font)

    dpg.create_viewport(title="Mob List",height=height,width=width)
except:
    print("This script uses a custom font. Please download it and put it in your minescript folder.")
    exit()




def resize_root():
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()

    if decorated:
        w -= 14
        h -= 39
    dpg.set_item_pos("root", (0,0))
    dpg.set_item_width("root", w)
    dpg.set_item_height("root", h)


def checkbox_cb(sender, app_data, user_data):

    change = app_data
    uuid = sender.removesuffix("-tick").removesuffix("-tick2")

    if change:

        dpg.add_tree_node(label=user_data, tag=uuid+"-pin", parent="pins")
        for e in entities():
            if e.uuid == uuid:
                entity = e

        dpg.add_text(f"Type: {entity.type.removeprefix("entity.minecraft.")}",parent=uuid+"-pin")
        dpg.add_text(f"Position: {entity.position}",parent=uuid+"-pin")
        dpg.add_text(f"Health: {entity.health}",parent=uuid+"-pin")
        dpg.add_text(f"ID: {entity.id}",parent=uuid+"-pin")
        dpg.add_text(f"UUID: {entity.uuid}",parent=uuid+"-pin")
        dpg.add_checkbox(label="Pin", default_value=True, tag=f"{entity.uuid}-tick2", callback=checkbox_cb, user_data=f"{entity.name} ({entity.type.removeprefix("entity.minecraft.")})",parent=uuid+"-pin")


    else:
        dpg.set_value(uuid+"-tick",False)
        dpg.delete_item(uuid+"-pin")
        

def update_pins():
    child_ids = dpg.get_item_children("pins", 1)
    child_tags = {
        dpg.get_item_alias(cid) for cid in child_ids if dpg.get_item_alias(cid)
    }

    for entity in entities():
        for tag in child_tags:
            if entity.uuid+"-pin" == tag:

                    property_ids = dpg.get_item_children(tag, 1)
                    for pid in property_ids:
                        if "Position: " in dpg.get_value(pid):
                            dpg.set_value(pid,f"Position: {entity.position}")
                            break

                        if "Health: " in dpg.get_value(pid):
                            dpg.set_value(pid,f"Health: {entity.health}")
                            break


def update_nodes():
        update_pins()

        
        

        child_ids = dpg.get_item_children("entity nodes", 1)
        child_tags = {
            dpg.get_item_alias(cid) for cid in child_ids if dpg.get_item_alias(cid)
        }
        
        #Update the nodes
        for entity in entities():
            if not entity.uuid in child_tags:

                with dpg.tree_node(parent="entity nodes", label=f"{entity.name} ({entity.type.removeprefix("entity.minecraft.")})", tag=entity.uuid):
                    dpg.add_text(f"Type: {entity.type.removeprefix("entity.minecraft.")}")
                    dpg.add_text(f"Position: {entity.position}")
                    dpg.add_text(f"Health: {entity.health}")
                    dpg.add_text(f"ID: {entity.id}")
                    dpg.add_text(f"UUID: {entity.uuid}")
                    dpg.add_checkbox(label="Pin", default_value=False, tag=f"{entity.uuid}-tick", callback=checkbox_cb, user_data=f"{entity.name} ({entity.type.removeprefix("entity.minecraft.")})")
                    
                    
                    
            
            else:
                
                for tag in child_tags:
                    
                    if entity.uuid == tag:
                        
                        property_ids = dpg.get_item_children(tag,1)
                        
                        for pid in property_ids:
                            if "Position: " in dpg.get_value(pid):
                                dpg.set_value(pid,f"Position: {entity.position}")
                                
                                break

                            if "Health: " in dpg.get_value(pid):
                                dpg.set_value(pid,f"Health: {entity.health}")
                                break
        


        entity_uuids = []
        for entity in entities():
            entity_uuids.append(entity.uuid)

        for tag in child_tags:
            if not tag in entity_uuids:
                dpg.delete_item(tag)


                
                
                
        
    

with dpg.window(label="Main Window", height=height, width=width, no_title_bar=True, no_move= True, tag="root"):


    with dpg.child_window(label="Info",tag="pins", height=13*FONT_SIZE):
        dpg.add_text("Entities: ",tag="entity label")

    with dpg.child_window(label="Testing"):
        with dpg.tree_node(label="Viewer",tag="entity nodes"):
            pass
                
                
                
                



dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_viewport_always_top(True)

def is_viewport_hovered():
    mx, my = dpg.get_mouse_pos(local=True)
    vw, vh = dpg.get_viewport_width(), dpg.get_viewport_height()
    
    return not (
        (mx < -30 or mx > vw + 10) and
        (my < -30 or my > vh + 10) 
    ) or not TOGGLE_HOVER

decorated = False

def update_decoration():
    global decorated

    hovered = is_viewport_hovered()

    if hovered and not decorated:
        dpg.set_viewport_decorated(True)
        decorated = True
    elif not hovered and decorated:
        dpg.set_viewport_decorated(False)
        decorated = False




def update_thread():
    while True:
        update_nodes()
        sleep(SLEEP_TIME)
        

threading.Thread(target=update_thread,daemon=True).start()

while dpg.is_dearpygui_running():
    
    cap = 0
    for entity in entities():
        if entity.type in HOSTILE_MOBCAP_MOBS:
            cap += 1
    dpg.set_value("entity label",f"Entities: {len(entities())}   Players: {len(players())}   Hostile: {cap}")
    resize_root()
    dpg.render_dearpygui_frame()

    update_decoration()
    

dpg.destroy_context()
