import appdirs
from argparse import ArgumentParser
from cachelib import FileSystemCache

from translate_it.dictionaries.youdao import translate

CACHE_DIR = appdirs.user_cache_dir('translate_it')
CACHE_ENTRY_MAX = 128

cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)

baidu_search = 'http://www.baidu.com/s?ie=utf-8&wd=%s'
bing_dict = 'https://cn.bing.com/dict/?q=%s'
bing_search = 'https://www.bing.com/search?q=%s'
cambridge = 'http://dictionary.cambridge.org/spellcheck/english-chinese-simplified/?q=%s'
dictcn = 'https://dict.eudic.net/dicts/en/%s'
etymonline = 'http://www.etymonline.com/index.php?search=%s'
google_search = 'https://www.google.com/#newwindow=1&q=%s'
google_translate = 'https://translate.google.cn/#auto/zh-CN/%s'
guoyu = 'https://www.moedict.tw/%s'
iciba = 'http://www.iciba.com/%s'
liangan = 'https://www.moedict.tw/~%s'
longman_business = 'http://www.ldoceonline.com/search/?q=%s'
merriam_webster = 'http://www.merriam-webster.com/dictionary/%s'
oxford = 'http://www.oxforddictionaries.com/us/definition/english/%s'
sogou = 'https://fanyi.sogou.com/#auto/zh-CHS/%s'
youdao = 'http://dict.youdao.com/w/%s'
youglish = 'https://youglish.com/search/%s'


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
