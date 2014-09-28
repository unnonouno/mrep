==============================
 MIURA: Morpheme I U Regexp A
==============================

.. image:: https://travis-ci.org/unnonouno/miura.svg?branch=master
   :target: https://travis-ci.org/unnonouno/miura

.. image:: https://coveralls.io/repos/unnonouno/miura/badge.png?branch=master
   :target: https://coveralls.io/r/unnonouno/miura?branch=master

MIURA is a regular expression matcher for morpheme sequences.
You can find morpheme sub-sequences that match a given pattern, such as noun sequences.


Requirement
===========

- Python >=2.7
- tornado
- mecab


Install
=======

Use `setup.py`.

::

   $ python setup.py install


Usage
=====

miura
-----

usage: miura [-h] pattern file

MIURA: morpheme i u regexp a

positional arguments:
  pattern     pattern
  file        data file

optional arguments:
  -h, --help  show this help message and exit


miuraserver
-----------

MIURA: morpheme i u regexp a

positional arguments:
  data                  data file

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port number


Pattern
=======

`.`
  matches all morphemes

`<surface=XXX>`
  matches morphemes whose surface are `XXX`

`<pos=XXX>`
  matches morphemes whose POS are `XXX`

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

(c) 2014, Yuya Unno.
