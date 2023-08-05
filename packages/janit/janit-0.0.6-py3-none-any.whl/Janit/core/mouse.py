
down_click = []
def click(x=0,y=0, right=False):
    global down_click
    global highlights
    if 'M' in y:
        key_down = True
    else:
        key_down = False
    y = y[:-2]


    if key_down:
        if down_click == []:#bug fix for Konsole
            down_click = [x,y]
            debug(f'{x} {y} key Down', Level=2)
        else:
            return
    else:
        if down_click == [x,y]:
            #clicked
            highlights = []
            update_display(rerender=True)
            #update_display(interface_only=True,  rerender=True)
            debug(f'Cliked {x} {y}', Level=1)
        elif down_click != []:
            #drug
            debug(f'Drag from {down_click[0]} {down_click[1]} to {x} {y}', Level=2)
            highlight([[down_click[0],down_click[1]],[x,y]])
            #copy_clip("_test")
        down_click = []
    if right:
        debug(f'{x} {y} right cliked', Level=2)

#range = [[x1,y1],[x2,y2]]
def highlight(new_range):
    global highlights
    #TODO ... a lot. multi line, copy backwards, etc
    size = int(new_range[0][0]) - int(new_range[1][0])

    start_y = int(new_range[0][1]) - 1
    start_x = int(new_range[0][0]) - 1

    #TODO do in loop per line
    text = stdscr.instr(start_y, start_x, abs(size))
    highlights.append([start_y,start_x,size])

    copy_clip(str(text)[1:])
    debug(str(text), Level=2)

    #org_text = stdscr.instr(fishyx[0], fishyx[1], 3)
def copy_clip(text, middle_mouse=True):
    if middle_mouse:
        cmd='echo ' + text.strip() + '| xclip'
    else: #ctrl+c/ctrl+v
        cmd='echo ' + text.strip() + '| xclip -selection c'
    return subprocess.check_call(cmd, shell=True)
