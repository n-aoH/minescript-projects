#!python
"""
Made with code from JulianIsLost and razrcraft.
"""
from system.pyj.minescript import *
Minecraft = JavaClass("net.minecraft.client.Minecraft")
RenderSystem = JavaClass("com.mojang.blaze3d.systems.RenderSystem")
HudRenderCallback = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback")
ARGB = JavaClass("net.minecraft.util.ARGB")

mc = Minecraft.getInstance()

show = True

render_list = []



def on_press_key(event):
    global show

    if event.action == 0 and event.key == 301:  # F12
        show = not show
        #print(f'show = {show}')

class textObject:
    def __init__(self, text:str, color: int, x: int, y:int, px:int, py:int, justifyX:int, justifyY:int, screens):
        self.text = str(text)
        self.color = int(color)
        self.x = int(x)  #
        self.y = int(100-y) 
        self.px = int(px)
        self.py = int(py)
        self.jx = justifyX
        self.jy = justifyY
        self.type = "textObject"
        self.screens = screens

    def render(self,guiGraphics,winx,winy): #razrcraft
        x = int(self.x * winx / 100) + self.px
        y = int(self.y * winy / 100) - self.py
        
        width: int = mc.font.width(self.text)
        height: int = mc.font.lineHeight
        x -= int(width * ((self.jx/2) +.5))
        y -= int(height * ((self.jy/2) +.5))
        guiGraphics.drawString(
        mc.font, 
        self.text,
        x,
        y,
        self.color)



class buttonObject: # all code here from JulianIsLost
    def __init__(self, x, y, px, py, justifyX, justifyY, width, height, text, text_color, button_color, click_callback, screens): 
        self.x = x
        self.y = (100-y)
        self.px = px
        self.py = py
        self.jx = justifyX
        self.jy = justifyY
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.text_width = mc.font.width(text)
        self.text_height = mc.font.lineHeight
        self.type = "buttonObject"
        self.screens = screens
        self.click_callback = click_callback 

    def render(self, guiGraphics, winx, winy):
        xp = int(self.x * winx / 100) + self.px - int(self.width * ((self.jx/2) +.5)) 
        yp = int(self.y * winy / 100) - self.py - int(self.height * ((self.jy/2) +.5)) 
        guiGraphics.fill(xp + self.px, yp - self.py, xp + self.width + self.px, yp + self.height - self.py, self.button_color)
        guiGraphics.drawString(mc.font, self.text, int(xp +self.px + (self.width-self.text_width)/2), int(yp -self.py+ (self.height-self.text_height/2)/2), self.text_color, False)
    
    def lighten_color(self):
        factor = 1/0.7
        
        a = ARGB.alpha(self.button_color)
        r = ARGB.red(self.button_color)
        g = ARGB.green(self.button_color)
        b = ARGB.blue(self.button_color)
        
        self.button_color = ARGB.color(a, int(r*factor), int(g*factor), int(b*factor))
        
    def darken_color(self):
        factor = 0.7
        
        a = ARGB.alpha(self.button_color)
        r = ARGB.red(self.button_color)
        g = ARGB.green(self.button_color)
        b = ARGB.blue(self.button_color)
        
        self.button_color = ARGB.color(a, int(r*factor), int(g*factor), int(b*factor))
    
    def button_clicked(self):
        self.darken_color()
        
        self.click_callback()
        set_timeout(self.button_unclicked, 250)
    
    def button_unclicked(self):
        self.lighten_color()
    
    def check_for_click(self, event):
        winx = int(mc.getWindow().getGuiScaledWidth())
        winy = int(mc.getWindow().getGuiScaledHeight())
        xp = int(self.x * winx / 100) + self.px - int(self.width * ((self.jx/2) +.5)) + self.px
        yp = int(self.y * winy / 100) - self.py - int(self.height * ((self.jy/2) +.5)) - self.py
        scale = mc.getWindow().getGuiScale()
    
        x = event.x / scale
        y =  event.y / scale        

        if xp <= x and x <= xp + self.width and yp <= y and y <= yp + self.height:

            self.button_clicked()
            

def updateButtons(event):
    screen = screen_name()
    if event.action == 1:
        for i in render_list:
            if i.screens == "all" or screen in i.screens:
                if i.type == "buttonObject":
                    i.check_for_click(event)

def on_hud_render(guiGraphics, tickDeltaManager):
    if not show:
        return
    
    gpuDevice = RenderSystem.tryGetDevice()
    renderDebug = gpuDevice is not None and gpuDevice.isDebuggingEnabled()

    
    # FROM RAZRCRAFT
    winx = int(mc.getWindow().getGuiScaledWidth())
    winy = int(mc.getWindow().getGuiScaledHeight())
    screen = screen_name()
    for i in render_list:
        if i.screens == "all" or screen in i.screens:
            i.render(guiGraphics,winx,winy)



HudRenderCallback.EVENT.register(HudRenderCallback(on_hud_render))


