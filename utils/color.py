color_table = {
    'yellow' : ['\x1b[33m', '\x1b[39m']
}

def colorFont(color, text):
    return color_table[color][0] + text + color_table[color][1]