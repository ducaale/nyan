import nyan

prompt = nyan.new_text('Enter amount in Pounds', y=100, font='AldotheApache.ttf')
user_input = nyan.new_text('', font='AldotheApache.ttf')
cursor = nyan.new_box(y=2, width=20, height=46)
dollar_text = nyan.new_text('', y=-100, font='AldotheApache.ttf')

@nyan.repeat_forever
async def blink_cursor():
    cursor.show()
    await nyan.sleep(seconds=0.5)
    cursor.hide()
    await nyan.sleep(seconds=0.5)

@nyan.when_any_key_pressed
def handle_input(key):
    if key == 'space':
        user_input.text += ' '
    elif key == 'backspace':
        user_input.text = user_input.text[:-1]
    else:
        user_input.text += key
    
    try:
        dollars = float(user_input.text) * 1.39
        dollar_text.text = f'You will receive ${dollars:.2f}'
    except:
        dollar_text.text = ''

    cursor.left = user_input.right + 4

nyan.start_program()