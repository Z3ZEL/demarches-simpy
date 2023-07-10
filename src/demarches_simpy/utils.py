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
    def __init__(self, header, profile, **kwargs):
        self.header = header

        # ----------------- VERBOSE -----------------
        # Low priority
        self.verbose = profile.get_verbose() if profile != None else False

        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']

        # High priority
        import sys
        #check if -v or --verbose is in the arguments
        if '-v' in sys.argv or '--verbose' in sys.argv:
            self.verbose = True


        # ----------------- WARNING DISPLAY -----------------
        
        self.displaying_warning = profile.__displaying_warning__() if profile != None else True

        if 'warning' in kwargs:
            self.displaying_warning = kwargs['warning']

        # High priority

        if '--no-warning' in sys.argv:
            self.displaying_warning = False



    def set_verbose(self, verbose):
        self.verbose = verbose
    def get_verbose(self):
        return self.verbose

    def __displaying_warning__(self):
        return self.displaying_warning


    def info(self, msg):
        msg = str(msg)
        print(f"{bcolors.OKGREEN}[{self.header}] {msg}{bcolors.ENDC}") 

    def error(self, msg):
        msg = str(msg)
        print(f"{bcolors.FAIL}[{self.header}] {msg}{bcolors.ENDC}")
        raise Exception("Error in "+self.header+": "+msg)

    def warning(self, msg):
        if not self.displaying_warning:
            return
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