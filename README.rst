===========================================
 MREP: Morpheme Regular Expression Printer
===========================================

.. image:: https://travis-ci.org/unnonouno/mrep.svg?branch=master
   :target: https://travis-ci.org/unnonouno/mrep

.. image:: https://coveralls.io/repos/unnonouno/mrep/badge.png?branch=master
   :target: https://coveralls.io/r/unnonouno/mrep?branch=master

MREP is a regular expression matcher for morpheme sequences.
You can find morpheme sub-sequences that match a given pattern, such as noun sequences.


Requirement
===========

- Python >=2.7
- mecab-python ( https://github.com/SamuraiT/mecab-python3 )


Install
=======

::

   $ pip install mrep

If you do not have a dictionary for MeCab, install `unidic-lite`.

::

   $ pip install unidic-lite

If you want to install it from its source, use `setup.py`.

::

   $ python setup.py install


Usage
=====

::

   usage: mrep [-h] [-o] [--color {never,auto,always}] [-n] [--mecab-arg MECAB_ARG]
               PATTERN [FILE [FILE ...]]

positional arguments:
  :`PATTERN`:               pattern
  :`FILE`:                  data file

optional arguments:
  -h, --help            show this help message and exit
  -o, --only-matching   print only matching
  --color COLOR         color mode. select from "never", "auto" and "always". (default: auto)
  -n, --line-number     Show line number
  --mecab-arg MECAB_ARG
                        argument to pass to mecab (ex: "-r
                        /path/to/resource/file")


Pattern
=======

`.`
  matches all morphemes

`<surface=XXX>`
  matches morphemes whose surface are `XXX`

`<pos=XXX>`
  matches morphemes whose POS are `XXX`

`<feature=XXX>`
  matches morphemes whose features are `XXX`

`<feature=~XXX>`
  matches morphemes whose features maches a RegExp pattern `XXX`

`X*`
  matches repetiion of a pattern X

`X|Y`
  matches X or Y

`(X)`
  matches X


Example
-------

`<pos=名詞>`
  matches a noun

`<pos=名詞>*`
  matches repetition of nouns

`<pos=名詞>*<pos=助詞>`
  matches repetition of nouns and a particle

`(<pos=名詞>|<pos=動詞>)*`
  matches repetition of nouns or verbs


License
-------

This program is distributed under the MIT license.


Copyright
---------

\(c) 2014, Yuya Unno.
