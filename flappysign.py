from pyflipdot.pyflipdot import HanoverController
from pyflipdot.sign import HanoverSign
from serial import Serial
from random import randint
from time import sleep

def flap(arguments):
    print("FLAP!")

ser = Serial('/dev/ttyUSB0')
controller = HanoverController(ser)

sign = HanoverSign(address=0, width=84, height=7)
controller.add_sign('sign', sign)

x = 32
player_x = 24
player_y = 3

digits = {
    "0": [ 
            False, False, True,  True,  True,  False, False,
            False, True,  False, False, False, True,  False, 
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  False, False, False, True,  False, 
            False, False, True,  True,  True,  False, False
         ],
    "1": [ 
            False, False, False, True,  False, False, False,
            False, False, True,  True,  False, False, False,
            False, True,  False, True,  False, False, False,
            False, False, False, True,  False, False, False,
            False, False, False, True,  False, False, False,
            False, False, False, True,  False, False, False,
            False, True,  True,  True,  True,  True,  False
         ],
    "2": [ 
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            False, False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, False,
            True,  False, False, False, False, False, False,
            True,  True,  True,  True,  True,  True,  True
         ],
    "3": [ 
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            False, False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False,
            False, False, False, False, False, False, True,
            False, False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False
         ],
    "4": [  True,  False, False, False, False, False, False,
            True,  False, False, False, False, True,  False,
            True,  False, False, False, False, True,  False,
            True,  False, False, False, False, True,  False,
            True,  True,  True,  True,  True,  True,  True,
            False, False, False, False, False, True,  False,
            False, False, False, False, False, True,  False,
         ],
    "5": [
            True,  True,  True,  True,  True,  True,  True,
            True,  False, False, False, False, False, False,
            True,  False, False, False, False, False, False,
            True,  True,  True,  True,  True,  True,  False,
            False, False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False
         ],
    "6": [ 
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, False,
            True,  True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False
         ],
    "7": [ 
            True,  True,  True,  True,  True,  True,  True,
            True,  False, False, False, False, True,  False,
            False, False, False, False, True,  False, False,
            False, False, False, True,  False, False, False,
            False, False, True,  False, False, False, False,
            False, False, True,  False, False, False, False,
            False, False, True,  False, False, False, False
         ],
    "8": [ 
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False
         ],
    "9": [ 
            False, True,  True,  True,  True,  True,  False,
            True,  False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  True,
            False, False, False, False, False, False, True,
            True,  False, False, False, False, False, True,
            False, True,  True,  True,  True,  True,  False 
         ]
}

image = sign.create_image()

def draw_digit(to_draw, start_x):
    digit_pattern = digits[to_draw]
    current_pos = 0

    for y in range(0, 7):
        for x in range(start_x, start_x + 7):
            image[y, x] = digit_pattern[current_pos]
            current_pos += 1

image[player_y, player_x] = True

while x < 84:
    gap_start = randint(0, 3)

    for n in range(0, 7):
        y = 6 - n

        if y < gap_start or y > gap_start + 2:
            image[y, x] = True
            image[y, x + 1] = True

    x += 8

controller.draw_image(image)
sleep(1)

frame_counter = 0
score = 0
just_scored = False

while True:
    # Draw the current score (always 2 digits)
    if score < 10:
        display_score = f"0{str(score)}"
    else:
        display_score = str(score)

    draw_digit(display_score[0], 3)
    draw_digit(display_score[1], 11)

    for x in range(24, 83):
        for y in range(0, 7):
            image[y, x] = image[y, x + 1]    

    if image[player_y, player_x] == True:
        print("boom")
        break

    image[player_y, player_x] = True

    # Update the score if the player just passed a pipe.
    if image[0, player_x] == True and player_y != 0:
        if not just_scored:
            just_scored = True
            score += 1

            # Keep the score to 2 digits!
            if score == 100:
                score = 0
    else:
        just_scored = False

    if frame_counter == 7:
        frame_counter = 0

        gap_start = randint(0, 3)

        for n in range(0, 7):
            y = 6 - n

            if y < gap_start or y > gap_start + 2:
                image[y, 80] = True
                image[y, 81] = True
    else:
        frame_counter += 1 

    controller.draw_image(image)
    sleep(.5)

print(f"game over, score: {score}")