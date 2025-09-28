from minescript import *
from minescript_plus import *
from time import sleep
import rotation

### REQUIRES:
# https://github.com/Koteukin69/minescript/blob/main/rotation.py
### Camera lib, replace with another if you want.



def magnitude(x,y,z):
    return ((x**2)+(y**2)+(z**2))**.5

def launch():


    rotation.look_at_block(get_player().position[0],305,get_player().position[2])
    press_key_bind("key.jump",True)
    sleep(0.05)
    press_key_bind("key.jump",False)
    while get_player().velocity[1] > -.1:
        sleep(0.05)
    press_key_bind("key.jump",True)
    sleep(0.1)
    press_key_bind("key.use",True)
    sleep(.2)
    press_key_bind("key.jump",False)
    press_key_bind("key.use",False)
    sleep(0.1)
    press_key_bind("key.jump",True)

    while get_player().position[1] < 302:
        if get_player().velocity[1] < 0.7:
            press_key_bind("key.use",True)
            sleep(0.01)
            press_key_bind("key.use",False)
            sleep(0.1)
        else:
            press_key_bind("key.use",False)
    press_key_bind("key.use",False)

def fly_onward():
    while Util.get_distance(get_player().position,[xpos,350,zpos]) > 50:
        if (magnitude(*get_player().velocity)) < 1:
            press_key_bind("key.use",True)
            sleep(0.01)
            press_key_bind("key.use",False)
            sleep(0.1)
        else:
            press_key_bind("key.use",False)
        player_look_at(xpos,get_player().position[1]+50+(magnitude(get_player().position[0]-xpos,0,get_player().position[2]-zpos)*.05),zpos)
        
    press_key_bind("key.use",False)

if __name__ == "__main__":
    xpos = float(sys.argv[1])
    zpos = float(sys.argv[2])
    
    launch()
    rotation.look_at_block(xpos,355,zpos)
    fly_onward()
    Util.play_sound(Util.get_soundevents().PLAYER_LEVELUP)
    print("Done!")