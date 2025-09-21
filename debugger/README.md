# Debugger

A debugging program for the Minecraft mod Minescript. Developed using code and information from [razrcraft](https://github.com/R4z0rX/minescript-scripts/tree/main). More commands, info, and operators are coming.

## Requirements:

[lib_ren](https://github.com/JulianIsLost5/minescript-scripts/tree/main/lib_ren) - World Rendering
## Operators
- You can call these in your chat function to substitute in for a game variable.
### %v
- Your clipboard.
### %p
- Player block position
### %s
- Accepts: %s.ATTRIBUTE
- ATTRIBUTE is optional.
- Your entity from minescript.
### %g
- accepts: %g:ENTITYTYPE.ATTRIBUTE
- ENTITYTYPE and ATTRIBUTE are both optional.
- nestled "grab" command.
- will return the closest entity to you of a specified type
- Attribute pulls from the list given through minescript's entity info. To view full list, use `?print %g`
## Commands
- Start your chat message with "?" for the debugger to intercept the message.
### copy
- Copies to your clipboard
- ex. `?copy Position: %p`
### print
- Prints to chat
- ex. `?print %g:player.name`
### uuid
- Returns the minescript info of the UUID provided.
- ex. `?uuid %v`
### dump
- Accepts: entity:ENTITYTYPE.ATTRUTE, inventory
- ENTITYTYPE and ATTRIBUTE are both optional.
- Prints every item in the selection in chat.
- ex. `?dump entity:cow.health`
### grab
- Copies the UUID of the entity selected OR prints the block info of your view in chat.
### =
- python `eval()` function in your chat.
- ex. `?= 1 + 2`
### docs
- Opens a documentation page from a list of common modules.
- Pages listed ingame through `?docs`
### info
- accepts: python, third_party_modules
- gives you the info
- ex. `?info python`
### toggle
- toggle showing information
- accepts: show_block_updates, show_chunk_updates, show_keys, show_mouse, render_through_walls + `true/false`
- ex. `?toggle show_block_updates true`
