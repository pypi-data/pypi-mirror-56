class style():
    BLACK = lambda x: '\033[30m' + str(x) + '\033[0m'
    RED = lambda x: '\033[31m' + str(x) + '\033[0m'
    GREEN = lambda x: '\033[32m' + str(x) + '\033[0m'
    YELLOW = lambda x: '\033[33m' + str(x) + '\033[0m'
    BLUE = lambda x: '\033[34m' + str(x) + '\033[0m'
    MAGENTA = lambda x: '\033[35m' + str(x) + '\033[0m'
    CYAN = lambda x: '\033[36m' + str(x) + '\033[0m'
    WHITE = lambda x: '\033[37m' + str(x) + '\033[0m'
    UNDERLINE = lambda x: '\033[4m' + str(x) + '\033[0m'
