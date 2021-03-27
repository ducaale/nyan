# https://youtu.be/9FJkU_NHDVw
# https://youtu.be/qoYxZfZAT6U

import math
import nyan

nyan.screen.width = 400
nyan.screen.height = 400

bird = nyan.new_image('bird0.png', is_hidden=True)
button1 = nyan.new_image('button.png', x=70, y=-100)
button2 = nyan.new_image('button.png', x=-70, y=-100)
button3 = nyan.new_image('button.png', y=-100, is_hidden=True)
game_title = nyan.new_text('Flappy bird', y=100)
leaderboard_title = nyan.new_text('Leaderboards', y=100, is_hidden=True)
animation_timer = nyan.new_timer()

@nyan.repeat_forever
async def float_bird():
    bird.y += math.cos(animation_timer.seconds * 10) * 5

@nyan.repeat_forever
async def animate_buttons():
    for button in [button1, button2, button3]:
        if nyan.mouse.is_touching(button):
            button.size += (120 - button.size)/3
        else:
            button.size = 100
        
        if nyan.mouse.is_touching(button) and nyan.mouse.is_clicked:
            button.transparency = 80
        else:
            button.transparency = 100

@button1.when_clicked
async def start_game():
    await nyan.sleep(0.1)
    navigate('main_menu', 'game')

@button2.when_clicked
async def show_leaderboard():
    await nyan.sleep(0.1)
    navigate('main_menu', 'leaderboard')

@button3.when_clicked
async def leaderboard_to_main_menu():
    await nyan.sleep(0.1)
    navigate('leaderboard', 'main_menu')

def navigate(current, next):
    if current == 'main_menu':
        button1.hide()
        button2.hide()
        game_title.hide()
        if next == 'game':
            bird.show()
        elif next == 'leaderboard':
            button3.show()
            leaderboard_title.show()
    if current == 'leaderboard':
        button3.hide()
        leaderboard_title.hide()
        if next == 'main_menu':
            button1.show()
            button2.show()
            game_title.show()

nyan.start_program()