''' __main__, to run:
python -m bing_tr
'''
import sys
from random import randint

from bing_tr import bing_tr


def main():
    '''main'''
    if not sys.argv[3:]:
        to_lang = 'zh'

    if not sys.argv[2:]:
        from_lang = 'en'

    if not sys.argv[1:]:
        print('Provide some English text, testing with some random text')
        text = 'test ' + str(randint(0, 10000))

    resu = bing_tr(text, from_lang, to_lang)

    print(f'[{text}] translated to: [{resu}]')


if __name__ == '__main__':
    main()
