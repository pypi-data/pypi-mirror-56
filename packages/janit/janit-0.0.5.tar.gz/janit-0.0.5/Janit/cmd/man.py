def manual(args):
    sleep = janit.time.sleep
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\nWelcome to Janit! (Just Another Nifty Interface Tool)")
    sleep(2.5)
    yield 'clear'
    sleep(1)

    #show bash/tty number
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("  <------")
    janit.print("\nThis is a running bash session.")
    sleep(3)
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\n^")
    janit.print("\nEach session is given a sequential number")
    sleep(2)
    janit.print("In this case, we are using: ")
    yield 'tty'
    sleep(3)

    #show how to enter a terminal
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\nYou can enter the bash session by:")
    sleep(2)
    janit.print("  Pressing 'Enter' on an empty menu command")
    yield '...'
    sleep(2)
    janit.print("  Pressing Ctrl + Arrow Up")
    sleep(3)
    janit.print("\nFrom here, it's just a regular terminal")
    sleep(2)
    yield 'ls'
    sleep(2)

    #show how to switch back to menu mode
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\nTo switch back to the menu:")
    sleep(2)
    janit._input_focus = "janit"
    janit.print("  Press Ctrl + Arrow Down")
    sleep(3)


    #show how to open new bash sessions
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\nTo open a new bash session:")
    sleep(2)
    janit.print("  Press Ctrl + Arrow Left")
    sleep(3)
    janit.print("\nUse 'Ctrl + Right' and 'Ctrl + Left' to switch between sessions")
    sleep(5)

    #show how run deskop apps
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\nFrom the menu, Desktop application and Janit comamnd can be run.")
    sleep(5)
    janit.print("Examples: ")
    sleep(2)
    janit.print("  firefox")
    sleep(1)
    janit.print("  kate")
    sleep(2)
    janit.print("\nYou can also enter a file path in the menu.")
    sleep(2)
    janit.print("The file will become an argument the next run command")
    sleep(2)
    janit.print("Examples")
    sleep(1)
    janit.print("  /path/to/_linux_distro.iso")
    janit.print("    make_usb (to create a live USB of linux_distro.iso)")
    sleep(4)
    janit.print("  /path/to/file.txt")
    janit.print("    kate (to TRY to edit file.txt)")
    sleep(4)
    janit.print("\nPress 'tab' for applications that can run the targeted file.")
    sleep(3)
    janit.print("Run: 'done' to deselect the file.")
    sleep(4)
    
    """
    #show how to split ttys
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("\nYou can split the screen with any open sessions")
    sleep(3)
    janit.print("<Session numbers> separated with a space, will split horizontally")
    sleep(3)
    janit.print("  Example command:")
    sleep(2)
    janit.split("0 1")
    janit.print("  0 1")
    sleep(4)
    janit.split(str(janit.out_put_screen))
    janit.print("<Session numbers> separated with a slash, will split vertically")
    sleep(3)
    janit.print("  Example command:")
    sleep(2)
    janit.split("0/1")
    janit.print("  0/1")
    sleep(3)
    janit.split(str(janit.out_put_screen))
    janit.print("Mixing is allowed, Example: 0 1/3 4")
    sleep(5)
    """
    
    yield 'clear'
    sleep(.2) #wait for clear
    janit.print("""\n#Janit GPL3
    #Copyright (C) 2019 David Hamner

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program. If not, see <http://www.gnu.org/licenses/>.
    """)

Help = manual
