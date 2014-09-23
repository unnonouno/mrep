# encoding: utf-8

import argparse
import json
import os

import tornado.ioloop
import tornado.web

import builder
import morph
import pattern
import traceback

class Database(object):
    def __init__(self, sentences):
        data = []
        for s in sentences:
            data.append({
                'original': s,
                'morphemes': morph.parse(s),
            })

        self.data = data

    def find(self, pat):
        matcher = builder.parse(pat.encode('utf-8'))

        results = []
        for datum in self.data:
            ms = datum['morphemes']
            result = pattern.find(ms, matcher)
            if len(result) > 0:
                results.append({
                    'original': datum['original'],
                    'result': result
                })

        return results

class TopHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render('find.html',
                    results=None,
                    pat='',
                    error=None,
                    trace=None)

class FindHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        pat = self.get_argument('pat')
        try:
            results = self.db.find(pat)
            self.render('find.html',
                        results=results,
                        pat=pat,
                        error=None)

        except Exception as e:
            self.render('find.html',
                        results=None,
                        pat=pat,
                        error=e,
                        trace=traceback.format_exc())


def run():
    parser = argparse.ArgumentParser(description='MIURA: morpheme i u regexp a')
    parser.add_argument("data", help="data file")
    parser.add_argument("-p", "--port", type=int, required=False, default=9555,
                        help="port number")
    args = parser.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))
    sentences = []
    with open(args.data) as f:
        for line in f:
            sentences.append(line.strip())

    db = Database(sentences)
    prop = {'db': db}
    handlers = [
        (r'/', TopHandler, prop),
        (r'/find', FindHandler, prop)
        ]
    application = tornado.web.Application(
        handlers,
        static_path=os.path.join(root, 'static'),
        template_path=os.path.join(root, 'template'),
        debug=True)

    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
