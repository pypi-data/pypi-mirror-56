'''
bing translate for free as in beer
'''

import sys
import logging
from typing import Callable, Any, Tuple
from time import time
from random import randint
import pytest  # type: ignore
# import mock
from ratelimit import limits, sleep_and_retry


import requests
from fuzzywuzzy import fuzz, process  # type: ignore
import coloredlogs  # type: ignore
from jmespath import search  # type: ignore

LOGGER = logging.getLogger(__name__)
FMT = '%(filename)-14s[%(lineno)-3d] %(message)s [%(funcName)s]'
coloredlogs.install(level=10, logger=LOGGER, fmt=FMT)

LANG_CODES = (
        "ar,bg,ca,cs,da,de,el,en,es,fi,fr,he,hi,hr,hu,id,"
        "it,ja,ko,ms,nl,nb,pl,pt,ro,ru,sk,sl,sv,ta,te,th,"
        "tr,vi,zh-Hans,zh-Hant,yue"
).split(',') + ['auto-detect']
URL = (
        "https://www.bing.com/ttranslatev3?"
        "isVertical=1&&"
        "IG=0AF741D4794D421EB417BC51A62B9934&IID"
        "=translator.5026.4"
)
URL = "https://www.bing.com/ttranslatev3"
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'  # noqa
HEADERS = {"User-Agent": UA}

SESS = requests.Session()
SESS.get("https://www.bing.com")


def with_func_attrs(**attrs: Any) -> Callable:
    ''' with_func_attrs '''
    def with_attrs(fct: Callable) -> Callable:
        for key, val in attrs.items():
            setattr(fct, key, val)
        return fct
    return with_attrs


@with_func_attrs(text='')
def _bing_tr(
        text: str,
        from_lang: str = 'auto',
        to_lang: str = 'zh',
        timeout: Tuple[float, float] = (55, 66),
) -> str:
    ''' bing_tr '''

    try:
        from_lang = from_lang.lower()
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        from_lang = 'auto'
    try:
        to_lang = to_lang.lower()
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        to_lang = 'zh'

    try:
        from_lang = process.extractOne(from_lang, LANG_CODES, scorer=fuzz.UWRatio)[0]  # noqa
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        from_lang = 'en'
    try:
        to_lang = process.extractOne(to_lang, LANG_CODES, scorer=fuzz.UWRatio)[0]  # noqa
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("%s", exc)
        to_lang = 'en'

    data = {
        'text': text,
        'fromLang': from_lang,
        'to': to_lang,
    }

    try:
        resp = SESS.post(
            URL,
            data=data,
            headers=HEADERS,
            timeout=timeout,
        )
        resp.raise_for_status()
    except Exception as exc:  # pragma: no cover
        LOGGER.error('%s', exc)

    try:
        jdata = resp.json()
    except Exception as exc:  # pragma: no cover
        LOGGER.error('%s', exc)
        jdata = {'error': str(exc)}

    bing_tr.text = resp.text

    try:
        res = search('[0].translations[0].text', jdata)
    except Exception as exc:  # pragma: no cover
        LOGGER.error('%s', exc)
        res = {'error': str(exc)}

    return res


@sleep_and_retry
@limits(calls=30, period=20, raise_on_limit=True)  # raise_on_limit probably superfluous
def _rl_bing_tr(*args, **kwargs):
    ''' be nice and throttle'''
    LOGGER.info(' rate limiting 3 calls/2 secs... ')
    return _bing_tr(*args, **kwargs)


@with_func_attrs(calls=0, call_tick=-1)
def bing_tr(*args, **kwargs):
    ''' exempt first 200 calls from rate limiting '''

    # increase calls unto 210
    bing_tr.calls = bing_tr.calls if bing_tr.calls > 210 else bing_tr.calls + 1

    # reset rate limit if the last call was 1 minutes again
    tick = time()
    if tick - bing_tr.calls > 120:
        bing_tr.calls = 1
    bing_tr.call_tick = tick

    if bing_tr.calls < 200:
        return _bing_tr(*args, **kwargs)

    return _rl_bing_tr(*args, **kwargs)


@pytest.mark.parametrize(
    # 'to_lang', LANG_CODES
    'to_lang', ['zh', 'de', 'fr', 'it', 'ko', 'ja', 'ru']
)
def test_sanity(to_lang):
    'sanity test'

    numb = str(randint(1, 10000))
    text = 'test ' + numb
    assert numb in bing_tr(text, to_lang=to_lang)


def test_calls():
    ''' test calls '''
    calls = bing_tr.calls
    bing_tr('test ')
    assert bing_tr.calls == calls + 1


_ = """
# https://medium.com/opsops/how-to-test-if-name-main-1928367290cb
def test_init():
    ''' test init/main '''
    bing_tr.bing_tr = bing_tr
    LOGGER.debug('__name__: %s', __name__)

    with mock.patch('bing_tr.main', return_value=42):
        LOGGER.debug('main(): %s', main())
        with mock.patch('bing_tr.bing_tr.__name__', '__main__'):
            with mock.patch('sys.exit') as mock_exit:
                LOGGER.debug('__name__: %s', __name__)
                init()
                if mock_exit.call_args:
                    assert mock_exit.call_args[0] == 42
                print('mock_exit.call_args: ', mock_exit.call_args)
# """  # cant make it work


def main():  # pragma: no cover
    ''' main '''

    text = sys.argv[1:]
    if not text:
        print(' Provide something to translate, testing with some random text\n')
        text = 'test tihs and that' + str(randint(1, 1000))
        text1 = 'test tihs and that' + str(randint(1, 1000))

    print(f'{text} translated to:')
    for to_lang in ['zh', 'de', 'fr', ]:
        print(f'{to_lang}: {bing_tr(text, to_lang=to_lang)}')
        print(f'{to_lang}: {bing_tr(text1, to_lang=to_lang)}')


def init():
    ''' attempted to pytest __name__ == '__main__' '''
    LOGGER.debug('__name__: %s', __name__)
    if __name__ == '__main__':
        sys.exit(main())


init()

# test_init()
