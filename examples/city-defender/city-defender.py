import math
import nyan
import animation

points = []
lines = []

player = nyan.new_image('player-1.png', y=-100, size=60)
animation.add_animations(
    player,
    images = [
        'player-1.png', 'player-2.png', 'player-3.png',
        'player-4.png', 'player-5.png', 'player-6.png'
    ],
    animations = {
        'stable': [3, 4, 5],
        'acceleration': [0,1,2,2,2,3,4],
        'deaccelation': [4,3,1,0]
    }
)
animation_timer = nyan.new_timer()

@nyan.when_program_starts
async def do():
    NUMBER_OF_POINTS = 9

    for i in range(NUMBER_OF_POINTS):
        points.append(nyan.new_circle(color="red", radius=2))

    for i in range(NUMBER_OF_POINTS-1):
        lines.append(nyan.new_line(color='black', thickness=4, z=-1))

@nyan.repeat_forever
async def animate_player():
    player.set_animation('stable')
    player.next_frame()
    await nyan.sleep(0.01)

@nyan.repeat_forever
async def control_player():
    player.y += math.cos(animation_timer.seconds * 10) * 1

    player.point_towards(nyan.mouse)

    if nyan.key_is_pressed('w'):
        if player.y < 0:
            player.y += 10
    elif nyan.key_is_pressed('s'):
        player.y -= 10

    if nyan.key_is_pressed('d'):
        player.x += 10
    elif nyan.key_is_pressed('a'):
        player.x -= 10

@nyan.repeat_forever
async def do():
    def spawn_bullet(offset_x, offset_y):
        bullet = nyan.new_rect('red', width=10, height=15, x=player.x, y=player.y, angle=player.angle)
        bullet.move(offset_y)
        bullet.move(offset_x, player.angle + 90)
        bullet.add_tag('bullet')

    if nyan.mouse.is_clicked:
        spawn_bullet(15, 25)
        spawn_bullet(-15, 25)
        await nyan.sleep(0.1)

@nyan.repeat_forever
@nyan.foreach_sprite(tag='bullet')
async def move_bullet(bullet):
    if bullet.y > 1000:
        bullet.remove()

    if bullet.width != 5:
        await nyan.sleep(0.01)
        bullet.width = 15
        bullet.height = 5

    bullet.move(10)

@nyan.repeat_forever
async def spawn_missiles():
    x = nyan.random_number(nyan.screen.left, nyan.screen.right)
    y = nyan.screen.top
    missile = nyan.new_line(x1=x, y1=y, x2=x, y2=y+10, thickness=2)
    missile.add_tag('missile')

    random_angle = nyan.random_number(265, 275)
    missile.vx = -1 * math.cos(random_angle) * 5
    missile.vy = -1 * math.sin(random_angle) * 5

    await nyan.sleep(seconds=1)

@nyan.repeat_forever
@nyan.foreach_sprite(tag='missile')
async def move_missile(missile):
    if missile.y1 < -1000:
        missile.remove()

    missile.x1 += missile.vx
    missile.y1 += missile.vy

@nyan.repeat_forever
async def animate_player_power_wire():
    STIFFNESS = 5
    GRAVITY = -9

    def conntect_points(points, lines):
        for point1, point2, line in zip(points, points[1:], lines):
            line.x1, line.y1 = point1.x, point1.y
            line.x2, line.y2 = point2.x, point2.y

    for i in range(len(points)):
        point = points[i]
        point_to_follow = points[i-1]

        if i == 0:
            point.go_to(player)
            point.y += 2
        else:
            point.x += (point_to_follow.x - point.x) / STIFFNESS
            point.y += ((point_to_follow.y - point.y) / STIFFNESS) + GRAVITY

    conntect_points(points, lines)


nyan.start_program()