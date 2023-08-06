from pynput import keyboard


def on_press(key):
    try:
        print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'special key {key} pressed')


def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def main():
    print('This is io.rec')
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()


if __name__ == '__main__':
    main()
