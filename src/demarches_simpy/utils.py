class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ILog(object):
    def __init__(self, header, verbose = False):
        self.header = header
        self.verbose = verbose
        if verbose is None:
            self.verbose = False
    def set_verbose(self, verbose):
        self.verbose = verbose

    def info(self, msg):
        msg = str(msg)
        print(f"{bcolors.OKGREEN}[{self.header}] {msg}{bcolors.ENDC}") 

    def error(self, msg):
        msg = str(msg)
        print(f"{bcolors.FAIL}[{self.header}] {msg}{bcolors.ENDC}")
        raise Exception("Error in "+self.header+": "+msg)

    def warning(self, msg):
        msg = str(msg)
        print(f"{bcolors.WARNING}[{self.header}] {msg}{bcolors.ENDC}")

    def debug(self, msg):
        if not self.verbose:
            return
        msg = str(msg)
        print(f"{bcolors.OKBLUE}[{self.header}] {msg}{bcolors.ENDC}")

    def bold(self, msg):
        msg = str(msg)
        print(f"{bcolors.BOLD}[{self.header}] {msg}{bcolors.ENDC}") 