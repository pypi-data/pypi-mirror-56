import sys
import colorama
from termcolor import colored


class Logger(object):
    log_table = {
        "info"    : colored('[*] ', 'blue', attrs=['bold']),
        "warn"    : colored('[!] ', 'yellow', attrs=['bold']),
        "failure" : colored('[-] ', 'red', attrs=['bold']),
        "success" : colored('[+] ', 'green', attrs=['bold']),
    }

    def __init__(self):
        colorama.init()

    def info(self, message):
        print(self.log_table['info'] + message, file=sys.stderr)

    def warn(self, message):
        print(self.log_table['warn'] + message, file=sys.stderr)

    def failure(self, message):
        print(self.log_table['failure'] + message, file=sys.stderr)

    def success(self, message):
        print(self.log_table['success'] + message, file=sys.stderr)


