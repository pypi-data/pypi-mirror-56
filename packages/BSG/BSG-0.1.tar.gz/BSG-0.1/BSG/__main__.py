'''BSG - BullShitGenerator.
Original from https://github.com/menzi11/BullshitGenerator
Under anti 996 license.
Distributed and modulized by mvfki.
This is just a practice of writing a module/package. Please DO NOT use this 
tool in any formal scenario.
'''
import argparse
import sys, os
import logging
from .core import *
from .core import _getNotNone

def main():
    parser = argparse.ArgumentParser(description = __doc__, 
                    formatter_class = argparse.RawDescriptionHelpFormatter, 
                    usage = argparse.SUPPRESS)
    parser.add_argument('-t', '--theme', metavar = 'STR', type = str, 
                        required = True, 
                        help = 'The theme you want to talk about.')
    parser.add_argument('-j', '--jsonDataBase', metavar = 'JSON', type = str, 
                    help = 'Optional. By default we load the original data.')
    parser.add_argument('-d', '--bsDataBase', metavar = 'NAME', type = str, 
                    help = 'The name of an existing BSDB. Optional, By \n\
default we load the original data')
    parser.add_argument('-p', '--bsDataBasePath', metavar = 'PATH', type = str, 
                    default = '', 
                    help = 'The path of the existing BSDB, can be included \n\
into NAME.')
    parser.add_argument('-w', '--wordLimit', metavar = 'INT', type = int, 
                        default = 1000, 
                        help = 'Around how many characters you want to get.')
    parser.add_argument('-r', '--repeatLevel', metavar = 'INT', type = int, 
                        default = 2)
    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        raise

    bs = bullShit(args.theme, JSON = args.jsonDataBase, 
                  BSDB = args.bsDataBase, BSDBPath = args.bsDataBasePath, 
                  wordLimit = args.wordLimit, repeatLevel = args.repeatLevel)
    logging.basicConfig(level = logging.INFO, 
                        format = '%(levelname)s::%(message)s')
    logging.info('THEME: %s' % args.theme)
    logging.info('WORD NUMBER: %d' % args.wordLimit)
    logging.info('USING %s: %s' % (bs.dbType, bs.dbName))
    logging.info('STARTING')
    sys.stdout.write(str(bs)+'\n')
    logging.info('FINISHED')

if __name__ == '__main__':
    main()
