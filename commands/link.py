import gdb
from utils.color import colorFont

class Link(gdb.Command):
    bits = 32
    x_wide = ''
    arch = ''

    def initArch(self):
        arch = gdb.execute('show architecture', to_string=True)
        self.arch = arch
        if '64' in arch:
            self.bits = 64
        else:
            self.bits = 32

        if self.bits == 32:
            self.x_wide = 'w'
        elif self.bits == 64:
            self.x_wide = 'g'

    def __init__(self):
        super(self.__class__, self).__init__('link', gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        self.initArch()
        argv = gdb.string_to_argv(args)
        max_length = 5
        link_offset = 0
        if len(argv) < 1:
            raise gdb.GdbError('Wrong args, length of args is at least 1')
        
        try:
            max_length = int(argv[1])
        except:
            max_length = 5
        
        try:
            link_offset = int(argv[2])
        except:
            link_offset = 0

        result = argv[0]
        head_list = argv[0]
        for _ in range(max_length):
            try:
                raw_out = gdb.execute('x/1x{} {} + {}'.format(self.x_wide, head_list, link_offset), to_string=True)
                #contains <name>
                name = raw_out[raw_out.index('<') + 1:raw_out.index('>')]
                if name != '':
                    name = colorFont('yellow', '<{}>'.format(name))
                value = raw_out[raw_out.index(':') + 1:]
                value = value[value.index('0'):]
                value = hex(int(value, 16))
                result += name + ' —▸ ' + value
                head_list = value
            except Exception as e:
                break
        print(result)

Link()