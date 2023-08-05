# -*- coding: utf-8 -*-

#     __                        __      __             _ __
#    / /__________ _____  _____/ /___ _/ /____        (_) /_
#   / __/ ___/ __ `/ __ \/ ___/ / __ `/ __/ _ \______/ / __/
#  / /_/ /  / /_/ / / / (__  ) / /_/ / /_/  __/_____/ / /_
#  \__/_/   \__,_/_/ /_/____/_/\__,_/\__/\___/     /_/\__/

import appdirs
from argparse import ArgumentParser
from cachelib import FileSystemCache

from translate_it.dictionaries.youdao import translate

CACHE_DIR = appdirs.user_cache_dir('translate_it')
CACHE_ENTRY_MAX = 128

cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)


def get_parser():

    parser = ArgumentParser(description='To help you translate')
    parser.add_argument('words', metavar='WORDS', type=str,
                        nargs='*', help='the words to translate')

    return parser


def printf(result):

    print('\033[1;44m网络释义\033[0m')
    for content in result.get('contents', ''):
        print(content)

    print(result.get('additionals', ''))
    examples = result.get('examples', [])
    print('\033[1;44m双语例句\033[0m')
    for index, example in enumerate(examples):
        print('{}. {}'.format(index + 1, example[0]))
        print(example[1])


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if not args['words']:
        parser.print_help()
        return

    result = translate(args['words'])
    printf(result)


if __name__ == '__main__':
    command_line_runner()
