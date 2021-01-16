import sys
import os
import importlib
sys.path.append(os.path.abspath(''))

script = 'orb'

def main():
    importlib.import_module('scripts.' + script)

if __name__ == '__main__':
    main()