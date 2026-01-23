import dearpygui.dearpygui as dpg
import os

try:
    os.chdir("minescript") #Maybe they'll update it in the future idk
except:
    pass


from minescript import *

FONT = "FunnelSans-Medium.ttf"
FONT_SIZE = 20
height = 900
width = 600


dpg.create_context()
try:
    with dpg.font_registry():
        default_font = dpg.add_font(FONT, FONT_SIZE)

    dpg.bind_font(default_font)

    dpg.create_viewport(title="Mob List",height=height,width=width)
except:
    pass




def resize_root():
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()
    dpg.set_item_pos("root", (0,0))
    dpg.set_item_width("root", w-14)
    dpg.set_item_height("root", h-39)


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


                
                
                
        last_entities = entities()
    

with dpg.window(label="Main Window", height=height, width=width, no_title_bar=True, no_move= True, tag="root"):


    with dpg.child_window(label="Info",tag="pins", height=13*FONT_SIZE):
        dpg.add_text("Entities: ",tag="entity label")

    with dpg.child_window(label="Testing"):
        with dpg.tree_node(label="Viewer",tag="entity nodes"):
            pass
                
                
                
                


dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_viewport_always_top(True)



tick = 0
while dpg.is_dearpygui_running():
    tick += 1
    dpg.set_value("entity label",f"Entities: {len(entities())}")
    resize_root()
    dpg.render_dearpygui_frame()

    if tick > 60:
        update_nodes()
        tick = 0
    
    # resizing the top window part

dpg.destroy_context()
