# bing-tr-free

bing translate for free: be gentle and rate limit to 3 calls/2 seconds, first 200 calls exempted

### Installation

```pip install bing-tr-free```

or

* Install (pip or whatever) necessary requirements, e.g. ```
pip install requests fuzzywuzzy pytest jmespath coloredlogs``` or ```
pip install -r requirements.txt```
* Drop the file bing_tr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
* or clone the repo (e.g., ```git clone https://github.com/ffreemt/bing-tr-free.git``` or download https://github.com/ffreemt/bing-tr-free/archive/master.zip and unzip) and change to the bing-tr-free folder and do a ```
python setup.py develop```

### Usage

```
from bing_tr import bing_tr
print(bing_tr('hello world'))  # ->'世界您好'
print(bing_tr('hello world', to_lang='de'))  # ->'Hallo Welt'
print(bing_tr('hello world', to_lang='fr'))  # ->'Salut tout le monde'
print(bing_tr('hello world', to_lang='ja'))  # ->'ハローワールド'
```

Consult the official website for language pairs supported.

### Acknowledgments

* Thanks to everyone whose code was used
