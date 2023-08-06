import subprocess
import time


def check_usb_exists(vid, pid):
    output = subprocess.check_output(['lsusb'], universal_newlines=True)
    return '{}:{}'.format(vid, pid) in output


def remove_gpio_security():
    subprocess.check_output(['sudo', 'chmod', '-R', '777', '/sys/class/gpio'])


def try_poweron():
    """ Do the power trigger required by the 1.0 kits """
    print("Using devkit 1.0 procedure to boot the modem")

    remove_gpio_security()
    # Setup gpio
    for i in [35, 68, 232]:
        with open('/sys/class/gpio/export', 'w') as handle:
            handle.write('{}\n'.format(i))
        remove_gpio_security()
        with open('/sys/class/gpio/gpio{}/direction'.format(i), 'w') as handle:
            handle.write('out\n')
        with open('/sys/class/gpio/gpio{}/value'.format(i), 'w') as handle:
            handle.write('0\n')

    # Trigger power button
    with open('/sys/class/gpio/gpio35/value', 'w') as handle:
        handle.write('1\n')
    time.sleep(2)
    with open('/sys/class/gpio/gpio35/value', 'w') as handle:
        handle.write('0\n')

    print("Waiting for modem to boot")
    for i in range(0, 60):
        if check_usb_exists('2c7c', '0125'):
            print("Booted in {} seconds".format(i))
            return True
        time.sleep(1)
    return False


def test_eg25():
    if not check_usb_exists('2c7c', '0125'):
        if not try_poweron():
            return False
