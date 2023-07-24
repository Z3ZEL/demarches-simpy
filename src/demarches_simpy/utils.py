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

class DemarchesSimpyException(Exception):
    def __init__(self,message="There was an error", header="[MAIN]",*args: object) -> None:
        super().__init__(message, *args)
        self.header = header
        self.message = message
    def __str__(self) -> str:
        return f"{bcolors.FAIL} [ERROR] [{self.header}] {super().__str__()}{bcolors.ENDC}"
