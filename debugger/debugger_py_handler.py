from minescript import *

import webbrowser
import sys
import pkgutil

### CODE HERE FROM RAZR FOR GETTING INSTALLED MODULES ###


def get_stdlib_modules():
    # Standard library modules for Python 3.x
    stdlib_modules = {
        '__future__', '_thread', 'abc', 'aifc', 'argparse', 'array', 'ast', 
        'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 
        'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'calendar', 
        'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 
        'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 
        'contextlib', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv', 'ctypes', 
        'curses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'doctest', 
        'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 
        'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 
        'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 
        'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'idlelib', 
        'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress', 
        'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 
        'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 
        'mmap', 'modulefinder', 'multiprocessing', 'netrc', 'nntplib', 'numbers', 
        'operator', 'optparse', 'os', 'ossaudiodev', 'parser', 'pathlib', 
        'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 
        'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 
        'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 
        're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 
        'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 
        'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 
        'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 
        'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 
        'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 
        'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 
        'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 
        'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 
        'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 
        'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 
        'zipfile', 'zipimport', 'zlib', 'zoneinfo'
    }
    
    # Add version-specific modules
    if sys.version_info >= (3, 8):
        stdlib_modules.update(['graphlib'])
    if sys.version_info >= (3, 9):
        stdlib_modules.update(['zoneinfo'])
    if sys.version_info >= (3, 10):
        stdlib_modules.update(['dataclasses'])
        
    return stdlib_modules

def create_module_list():
    global third_party_modules
    stdlib_modules = get_stdlib_modules()
    third_party_modules = set()
    for importer, modname, ispkg in pkgutil.iter_modules():
    	if modname not in stdlib_modules:
    		third_party_modules.add(modname)
              
def print_module_list():
    for module in sorted(third_party_modules):
                
        print(module)
    print(f"\nTotal third-party modules: {len(third_party_modules)}")
### END ###

if len(sys.argv) > 1:
    match sys.argv[1]:
        case "keys":
            webbrowser.open("https://www.glfw.org/docs/3.4/group__keys.html")
        case "minescript":
            webbrowser.open("https://minescript.net/docs")
        case "minescript-ce":
            webbrowser.open("https://sam-ple.github.io/minescript-sample/")
        case "msp":
            webbrowser.open("https://github.com/R4z0rX/minescript-scripts/tree/main/Minescript-Plus")
        case "pyjinn":
            webbrowser.open("https://minescript.net/pyjinn")
        case "mappings":
            webbrowser.open("https://mappings.dev/")
        case "discord":
            webbrowser.open("https://discord.gg/NjcyvrHTze")
        case "mapping_info":
            webbrowser.open("https://minescript.net/mappings")
        case "pyinfo":
            info = sys.version
            print(f"Python version: {sys.version}")
        case "modules":
            create_module_list()
            print_module_list()
            print("list may not be accurate, and contains minescript scripts.")
        case "calc":
            print(eval(sys.argv[2]))