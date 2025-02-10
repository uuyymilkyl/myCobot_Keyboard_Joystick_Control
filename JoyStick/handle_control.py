import pygame
import sys
from pymycobot import MyCobot,utils
mc=MyCobot(utils.get_port_list()[0])
init_angles=[0, 0, 0, 0, 0, 0]
mc.sync_send_angles(init_angles,50)
pygame.init()


init_angles2=[0, 0, -90, 0, 0, 60]
pygame.joystick.init()

button_pressed = False
hat_pressed=False
previous_state = [0,0,0,0,0,0]

def joy_handler():
    global button_pressed
    global hat_pressed
    global previous_state
    if event.type == pygame.JOYAXISMOTION:
        axis = event.axis

        # get the respone value from joystick and rounded to three decimal 
        value = round(event.value, 3)

        # only respone when joystick value >0.5, can be changed as needed 
        if abs(value) > 0.5:
            print("axis")
            print(axis)
            print("value")
            print(value)
            flag = True

            # joystick axis   LEFT : [0:Y  1:X ]   RIGHT[3:J6  4:Z]
            previous_state[axis] = value
            
            # AXIS0 for longitudinally control value of Y
            if axis==0 and value==-1.00:
                mc.jog_coord(2,1,50)
            elif axis==0 and value==1.00:
                mc.jog_coord(2,0,50)
                
            if axis==1 and value==1.00:
                mc.jog_coord(1,0,50)
            elif axis==1 and value==-1.00:
                mc.jog_coord(1,1,50)

            if axis==3 and value==1.00:
                mc.jog_angle(6,0,30)
            elif axis==3 and value==-1.00:
                mc.jog_angle(6,1,30)
                
            # AXIS4 for longitudinally control value of Z
            if axis==4 and value==1.00: 
                mc.jog_coord(3,0,30)
            elif axis==4 and value ==-1.00:
                mc.jog_coord(3,1,30)

            
        else:
            if previous_state[axis] != 0:
                mc.stop()
                previous_state[axis] = 0
# change gripper state 
    if event.type == pygame.JOYBUTTONDOWN:
        if joystick.get_button(3)==1:
            mc.set_gripper_state(0,100)
        if joystick.get_button(0)==1:
            mc.set_gripper_state(1,100)

        # push X to decrease value of Joint 1
        if joystick.get_button(1)==1:
            mc.jog_angle(1,0,50)
        # push B to increase value of Joint 1
        if joystick.get_button(2)==1:
            mc.jog_angle(1,1,50)

        #if joystick.get_button(4) == 1:  # L1 通常是按钮 4
        #    mc.jog_angle(6, 0, 50)

            # R1 按钮：控制关节1正方向运动
        #if joystick.get_button(5) == 1:  # R1 通常是按钮 5
        #    mc.jog_angle(6, 1, 50)

        if joystick.get_button(7) == 1:  # botton 7 set init 
            mc.send_angles(init_angles2)

    if event.type == pygame.JOYBUTTONUP:
        if joystick.get_button(1) == 0:  # X button released
            mc.stop()  # Stop Joint 1 movement if X is released
        if joystick.get_button(2) == 0:  # B button released
            mc.stop()  # Stop Joint 1 movement if B is released


    if event.type == pygame.JOYHATMOTION:
        hat_value = joystick.get_hat(0)
        if hat_value ==(0,-1):
            mc.jog_coord(5,1,50)
        elif hat_value ==(0,1):
            mc.jog_coord(5,0,50)
        elif hat_value ==(-1,0):
            mc.jog_coord(4,0,50)
        elif hat_value ==(1,0):
            mc.jog_coord(4,1,50)
        if hat_value != (0, 0):
            hat_pressed = True
        else:
            if hat_pressed:
                mc.stop()
                hat_pressed = False

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("没有检测到手柄")
    pygame.quit()
    sys.exit()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        joy_handler()
pygame.quit()
