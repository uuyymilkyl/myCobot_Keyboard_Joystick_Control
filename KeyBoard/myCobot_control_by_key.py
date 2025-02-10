from pynput.keyboard import Listener, Key
import time
from pymycobot import MechArm270
from pymycobot import MyCobot280

mc = MyCobot280("/dev/ttyACM0", 115200)

# for recording
coords = []
current_state = 0


def print_menu():
    print("Welcome to MyCobot Control Program")
    print("Press the following keys to control the robot:")
    print("------------------------------------------------")
    print("r - Release all servos")
    print("t - Power on all servos")
    print("q - Record the current coordinates")
    print("c - Clear all recorded coordinates")
    print("g - Execute all recorded coordinates")
    print("------------------------------------------------")
    print("Press 'Ctrl+C' to exit the program.")


# main loop
def on_press(key):
    global executing
    try:
        if key.char == 'r':  # 按下r，松开所有电机关节  release all joint , you can move by your hand as needed
            mc.release_all_servos()
            current_state = 0
            time.sleep(0.1)  # 防止重复触发

        elif key.char == 't':  # 按下t，所有电机上电  tight , power on 
            mc.focus_all_servos()
            current_state = 1
            time.sleep(0.1)  # 防止重复触发

        elif key.char == 'q':  # 按下q，记录当前坐标   record the coord now 
            
            coords.append(mc.get_coords())
            print(f"Recorded coord: {coords[-1]}")
            time.sleep(0.1)  # 防止重复触发

        elif key.char == 'c':  # 按下c，清除所有记录的坐标   clear all coords recorded
            coords.clear()
            print("Cleared all recorded coordinates.")
            time.sleep(0.1)  # 防止重复触发

        elif key.char == 'g':  # 按下g，执行所有记录的坐标   run all coords recorded
            mc.focus_all_servos()
            if not executing and coords:  # 如果没有在执行并且有坐标可以执行
                executing = True
                print("Starting to execute coordinates...")
                
                
                for idx, coord in enumerate(coords):
                    print(f"Executing {coord}")
                    mc.send_coords(coord, 20, 1)  
                    
                    # changed by myself as I need a  gripper motion  -------
                    time.sleep(1)
                    if idx == 0:
                        mc.set_gripper_state(0, 80)      
                        time.sleep(1)
                    if idx == 1:
                        time.sleep(1)
                        mc.set_gripper_state(1, 80)
                   

                    time.sleep(1)
                time.sleep(2)
                mc.set_gripper_state(0, 80)
                time.sleep(1)
                mc.set_gripper_state(1, 80)
                
                # changed by myself as I need a  gripper motion--------
                
                print("All coordinates executed.")
                executing = False
            elif not coords:
                print("No coordinates to execurggrte.")
            else:
                print("Already executing. Please wait for the current operation to complete.")
        else:
            print("Invalid key pressed. Please follow the menu instructions.")
        
        time.sleep(0.1)  # 防止重复触发

    except AttributeError:
        # 处理特殊键（例如ESC、Ctrl等）
        pass


# Print the menu when the program starts
print_menu()

# 启动键盘监听器
with Listener(on_press=on_press) as listener:
    listener.join()
