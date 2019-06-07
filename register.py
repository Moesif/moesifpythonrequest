import pandoc
import os


def run():
    pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

    doc = pandoc.Document()
    doc.markdown = open('README.md').read()
    f = open('README.rst','w+')
    f.write(doc.rst)
    f.close()

run()
