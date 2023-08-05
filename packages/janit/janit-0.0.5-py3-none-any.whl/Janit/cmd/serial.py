#setup global serial info {'readable name':port}
#setup serial mode in ~/.janit/janit.cfg
def serial(args):
    if len(args) < 1:
        return

    name = " ".join(args).strip()
    #janit.debug(name, Level=3)
    if name in janit.imported_serial.keys():
        KEY = str(janit.imported_serial[name][0])
        all_keys = _read_keys()
        TTY = ""
        if KEY in all_keys:
            TTY = all_keys[KEY]
        else:
            janit.debug("\nCannot open serial device with KEY: " + KEY + "\nTry running 'serial_keys' for available devices.\n", Level=3)
            #janit.debug(f"Cannot find Key: {TTY}\nTry running 'serial_keys' for available devices." + Level=3)
            return
        yield 'clear'
        yield 'picocom ' + TTY + " -b " + str(janit.imported_serial[name][1])
        yield "..."

        janit.time.sleep(.2)
        janit.os.write(janit.masters[janit.out_put_screen], "\n\n".encode())


def tab_serial(cmd_str):
    can_return = []
    for key in janit.imported_serial.keys():
        can_return.append('serial ' + key)
    return can_return

def _read_keys():
    return_data = {}
    for tty_usb in janit.glob.glob("/dev/tty_usb*"):
        command = f"udevadm info -q path -n {tty_usb}".split()
        out,error = janit.subprocess.Popen(command, stdout=janit.subprocess.PIPE,stderr=janit.subprocess.STDOUT).communicate()
        KEY = str(out).split("/")[8]
        KEY = KEY.split('-')[-1]
        KEY = KEY.split(':')[0] #bug fix for ubuntu
        return_data[KEY] = tty_usb
        #janit.print(f"{tty_usb}: {KEY}")
    return return_data


def serial_keys(args):
    yield """
    clear;echo 'TTY: Key';for tty_usb in `ls /dev/tty_usb*`
    do
      echo -n "$tty_usb: "
      udevadm info -q path -n $tty_usb | cut -d '/' -f9 | cut -d '-' -f2 | cut -d ':' -f1
    done
    """
