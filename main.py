import pyautogui
import keyboard
import numpy as np
import time
import configparser
import os


def createConfig():
    config = configparser.ConfigParser()

    config['Settings'] = {
        'ActivationKey': 'p',
        'TargetColor': '255, 0, 0',
        'Smoothness': '0.2',
        'Delay': '0.05'
    }

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def loadConfig():
    config = configparser.ConfigParser()

    if not os.path.exists('config.ini'):
        print("Config file not found. Creating a new one.")
        createConfig()

    config.read('config.ini')
    
    activation_key = config.get('Settings', 'ActivationKey', fallback='p')
    target_color_str = config.get('Settings', 'TargetColor', fallback='255, 0, 0')
    target_color = [int(x) for x in target_color_str.split(',')]
    smoothness = config.getfloat('Settings', 'Smoothness', fallback=0.2)
    delay = config.getfloat('Settings', 'Delay', fallback=0.05)
    
    return activation_key, target_color, smoothness, delay

activation_key, target_color, smoothness, delay = loadConfig()
print(f"Activation Key: {activation_key}")
print(f"Target Color: {target_color}")
print(f"Smoothness: {smoothness}")
print(f"Delay: {delay}")

def findColor(target_color, tolerance=10, smoothness=0.2, delay=0.05):
    while True:
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        
        diff = np.abs(screen_np - target_color)
        match_mask = np.all(diff <= tolerance, axis=-1)

        if np.any(match_mask):
            y, x = np.unravel_index(np.argmax(match_mask), match_mask.shape)
            pyautogui.moveTo(x, y, duration=smoothness)  # Move smoothly to the target
            pyautogui.click()
            return True  # Clicked, exit the function

        time.sleep(delay)
if __name__ == "__main__":
    print(f"Hold '{activation_key}' to use Aimbot. Press 'Esc' to quit. Smoothness: {smoothness}")

    while True:
        if keyboard.is_pressed('esc'):
            print("Script stopped.")
            break

        if keyboard.is_pressed(activation_key):
            if findColor(target_color, smoothness=smoothness, delay=delay):
                print("Clicked")
