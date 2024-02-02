import RPi.GPIO as GPIO
import requests
import time
import threading
import os


# Disable GPIO warnings
GPIO.setwarnings(False)

SERVER_IP = '10.243.83.237' #my robot ip address #10.243.83.237
SERVER_PORT = 5000

# GPIO setup
GPIO.setmode(GPIO.BOARD)
motor_pwm_pin = 16 
left_button_pin = 12 
right_button_pin = 18 #
button_pin1 = 12
button_pin2 = 18
delay = 3


GPIO.setup(motor_pwm_pin, GPIO.OUT)
motor_pwm = GPIO.PWM(motor_pwm_pin, 100)  # PWM frequency: 100 Hz

#button shit
GPIO.setup(left_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to set motor speed using PWM
def set_motor_speed(speed):
    duty_cycle = speed * 1  # Adjust the multiplier based on your motor characteristics
    motor_pwm.start(duty_cycle)

def recalibrate(original_speed):
    recalibrated = (original_speed * (0.24)) + (39)
    return recalibrated

# Function to get target speed from the file
def get_target_speed():
    target_speed_file_path = 'target_speed.json'  # Adjust the path as needed

    if os.path.exists(target_speed_file_path):
        with open(target_speed_file_path, 'r') as file:
            data = json.load(file)
            return data.get('speed', 0)
    else:
        return 0



def control_loop():
    target_speed = 0  # Initial target speed
    press_count1 = 0
    press_count2 = 0  # Button 2 (commented out)
    button_state1 = GPIO.LOW
    button_state2 = GPIO.LOW
    prev_button_state1 = GPIO.input(button_pin1)
    prev_button_state2 = GPIO.input(button_pin2)

    # delay = requests.get(f'http://{SERVER_IP}:{SERVER_PORT}/start/{delay}', timeout=2)
    # if response.status_code == 200:
    #         delay_from_server = int(response.text)
    #         print(f"Received delay from server: {delay_from_server} seconds")   

    time.sleep(delay)
    drive_at_speed(recalibrate(250))  # 200
    time.sleep(3)
    while True:
        try:
            while True:
                button_state1 = GPIO.input(button_pin1)
                button_state2 = GPIO.input(button_pin2)
                if ((button_state1 == GPIO.HIGH) and (button_state2 == GPIO.HIGH)):
                    print("Button 1 and 2 is pressed")  
                    drive_at_speed(recalibrate(150))  
                    prev_button_state1 = GPIO.HIGH
                    prev_button_state2 = GPIO.HIGH

                elif ((button_state1 == GPIO.HIGH and prev_button_state1 == GPIO.LOW) and (button_state2 == GPIO.LOW and prev_button_state2 == GPIO.LOW)):
                    print("Button 1 only is pressed")  
                    drive_at_speed(recalibrate(200))  
                    prev_button_state1 = GPIO.HIGH
                    prev_button_state2 = GPIO.LOW
                
                elif ((button_state1 == GPIO.LOW and prev_button_state1 == GPIO.LOW) and (button_state2 == GPIO.HIGH and prev_button_state2 == GPIO.LOW)):
                    print("Button 2 only is pressed")  
                    drive_at_speed(recalibrate(250))  
                    prev_button_state1 = GPIO.LOW
                    prev_button_state2 = GPIO.HIGH

                elif ((button_state1 == GPIO.LOW) and (button_state2 == GPIO.LOW)):
                    print("NO BUTTONS")  
                    prev_button_state1 = GPIO.LOW
                    prev_button_state2 = GPIO.LOW

                # elif ((button_state1 == GPIO.LOW and prev_button_state1 == GPIO.HIGH) and (button_state2 == GPIO.LOW and prev_button_state2 == GPIO.HIGH)):
                #     print("Button 1 and 2 is released") 
                #     drive_at_speed(recalibrate(200))  
                #     prev_button_state1 = GPIO.LOW
                #     prev_button_state2 = GPIO.LOW

                # elif ((button_state1 == GPIO.LOW and prev_button_state1 == GPIO.HIGH) and (button_state2 == GPIO.HIGH and prev_button_state2 == GPIO.HIGH)):
                #     print("Button 1 only is released")  
                #     drive_at_speed(recalibrate(50))  
                #     prev_button_state1 = GPIO.LOW
                #     prev_button_state2 = GPIO.HIGH #supposed to low

                # elif ((button_state1 == GPIO.HIGH and prev_button_state1 == GPIO.HIGH) and (button_state2 == GPIO.LOW and prev_button_state2 == GPIO.HIGH)):
                #     print("Button 2 only is released!")  
                #     drive_at_speed(recalibrate(100))
                #     prev_button_state1 = GPIO.HIGH #supposed to be low
                #     prev_button_state2 = GPIO.LOW
                
              
                    
                   
                
                # elif ((button_state1 == GPIO.HIGH and prev_button_state1 == GPIO.LOW) and (button_state2 == GPIO.LOW and prev_button_state2 == GPIO.LOW)):
                #     print("Button 2 only is pressed")  
                #     drive_at_speed(recalibrate(230)) 
                #     prev_button_state1 = GPIO.LOW
                #     prev_button_state2 = GPIO.HIGH

                # elif ((button_state1 == GPIO.HIGH and prev_button_state1 == GPIO.HIGH) and (button_state2 == GPIO.LOW and prev_button_state2 == GPIO.HIGH)):
                #     print("Button 1 is released!")  # Print statement for terminal
                #     drive_at_speed(recalibrate(100))
                #     prev_button_state1 = button_state1  # Update the previous button state for Button 1
                #     prev_button_state2 = button_state2  # Update the previous button state for Button 1
                    
                    

                

                time.sleep(0.1)  # Small delay to avoid rapid state changes due to button bouncing


                # prev_button_state1 = GPIO.input(button_pin1)
                # prev_button_state2 = GPIO.input(button_pin2)  # Button 2 (commented out)
                # # Read button states
                # # left_button_pressed = not GPIO.input(left_button_pin)
                # # right_button_pressed = not GPIO.input(right_button_pin)
                
                
                # if button_state1 == GPIO.LOW and prev_button_state1 == GPIO.HIGH:  # Button 1 is pressed
                #     print("Button 1 is pressed!")  # Print statement for terminal
                #     drive_at_speed(recalibrate(250))  # 200

                # elif button_state1 == GPIO.HIGH and prev_button_state1 == GPIO.LOW:
                #     print("Button 1 is released!")  # Print statement for terminal
                #     stop_robot()

                # if button_state2 == GPIO.LOW and prev_button_state2 == GPIO.HIGH:  # Button 2 is pressed
                #     print("Button 2 is pressed!")  # Print statement for terminal
                #     drive_at_speed(recalibrate(-100))  # 200
                    
                # elif button_state2 == GPIO.HIGH and prev_button_state2 == GPIO.LOW:
                #     print("Button 2 is released!")  # Print statement for terminal
                #     # Add logic for adjusting the robot speed when Button 2 is released

                # prev_button_state1 = button_state1  # Update the previous button state for Button 1
                # prev_button_state2 = button_state2  # Update the previous button state for Button 2

                # time.sleep(0.5)  # Small delay to avoid rapid state changes due to button bouncing


                # # Get target speed from the file
                # target_speed = get_target_speed()

                # # Request target speed from the server
                # # response = requests.get(f'http://{SERVER_IP}:{SERVER_PORT}/target/{target_speed}', timeout=2)
            
                # if not left_button_pressed and not right_button_pressed:
                #     # Both buttons pressed, normal speed
                #     # if response.json()['status'] == 'no':
                #         # drive_as_fast_as_possible()
                #     # elif response.json()['status'] == 'ok':
                #         drive_at_speed(recalibrate(127)) #127
                # elif not right_button_pressed:
                #     # Only right button pressed, speed up
                #     # if response.json()['status'] == 'no':
                #         # drive_as_fast_as_possible()
                #     # elif response.json()['status'] == 'ok':
                #         drive_at_speed(recalibrate(250))  # 200
                # elif not left_button_pressed:
                #     # Only left button pressed, slow down
                #     # if response.json()['status'] == 'no':
                #         # drive_as_fast_as_possible()
                #     # elif response.json()['status'] == 'ok':
                #         drive_at_speed(recalibrate(42))  # 42
        except requests.exceptions.RequestException as e:
            print(f"Error 343 in communication: {e}")

        time.sleep(1)



def drive_as_fast_as_possible():
    print("Driving as fast as possible!")
    set_motor_speed(100)  # 100% duty cycle for maximum speed
    

def drive_at_speed(speed):
    print(f"Driving at speed: {speed}")
    set_motor_speed(speed)
    
def stop_robot():
    print("Stopping the robot!")
    set_motor_speed(0)  # Set the motor speed to 0 to stop the robot

if __name__ == "__main__":
    try:
        control_loop()
    except KeyboardInterrupt:
        motor_pwm.stop()
        GPIO.cleanup()
