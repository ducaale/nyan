import nyan

PIPE_GAP = 115
FLAP_STRENGTH = 12.0
GRAVITY = 1.6

background = nyan.new_image('background.png', size=75)
pipe_top = nyan.new_image('top.png')
pipe_bottom = nyan.new_image('bottom.png')
bird = nyan.new_image('bird0.png')

nyan.screen.width = 300
nyan.screen.height = 531
bird.dead = False

@nyan.when_program_starts
def do():
    bird.vy = FLAP_STRENGTH
    bird.x = -(nyan.screen.width/3)
    reset_pipes()

@nyan.repeat_forever
def move_pipes():
    pipe_bottom.x -= 5
    pipe_top.x -= 5
    if pipe_top.right < nyan.screen.left:
        reset_pipes()

@nyan.repeat_forever
async def animate_bird():
    if bird.dead:
        bird.image = 'birddead.png'
        return

    for image in ['bird0.png', 'bird1.png', 'bird2.png']:
        bird.image = image
        await nyan.sleep(0.1)

@nyan.repeat_forever
async def do():
    bird.vy -= GRAVITY
    bird.y += bird.vy
    bird.angle = bird.vy * 3

    if bird.is_touching(pipe_top) or bird.is_touching(pipe_bottom):
        bird.dead = True
    if bird.y > nyan.screen.top or bird.y < nyan.screen.bottom:
        bird.dead = True

@nyan.repeat_forever
async def control_bird():
    if not bird.dead and nyan.key_is_pressed('space'):
        bird.vy = FLAP_STRENGTH

def reset_pipes():
    pipe_top.left = nyan.screen.right
    pipe_bottom.left = nyan.screen.right

    bottom_pipe_top = nyan.random_number(
        -nyan.screen.height/2,
        (nyan.screen.height/2) - PIPE_GAP
    )
    pipe_bottom.top = bottom_pipe_top
    pipe_top.bottom = bottom_pipe_top + PIPE_GAP

nyan.start_program()