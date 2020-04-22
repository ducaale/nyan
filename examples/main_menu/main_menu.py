# https://youtu.be/9FJkU_NHDVw
# https://youtu.be/qoYxZfZAT6U

import math
import nyan

nyan.screen.width = 400
nyan.screen.height = 400

bird = nyan.new_image('bird0.png')
button = nyan.new_image('button.png', y=-100)
animation_timer = nyan.new_timer()

@nyan.repeat_forever
async def float_bird():
    bird.y += math.cos(animation_timer.seconds * 10) * 5

@nyan.repeat_forever
async def animate_button():
    if nyan.mouse.is_touching(button):
        button.size += (120 - button.size)/3
    else:
        button.size = 100
    
    if nyan.mouse.is_touching(button) and nyan.mouse.is_clicked:
        button.transparency = 80
    else:
        button.transparency = 100

nyan.start_program()