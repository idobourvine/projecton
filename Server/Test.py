import keyboard

if __name__ == "__main__":

    car_working = True
    pressed_hotkey = False  # flag if hotkey of ctrl+enter was pressed


    def update_pressed_hotkey():
        """
        Function that is called by keyboard to update the flag if the hotkey
        was pressed
        """
        global pressed_hotkey
        pressed_hotkey = True

    keyboard.add_hotkey('ctrl+enter', update_pressed_hotkey)
    # Starts tracking if hotkey was pressed

    while True:

        if pressed_hotkey:
            pressed_hotkey = False
            print("Changing car_working to " + str(not car_working))
            car_working = not car_working