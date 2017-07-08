#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import begin
import json

import extractors
import retrievers


def choices(**kwargs):
    """Validate arguments values are in a set"""

    def assert_choice(_name, _options):
        def assert_wrapper(value):
            if value not in _options:
                raise TypeError("'%s' choices are: '%s'" % (_name, "', '".join(_options)))
            return value
    new_kwargs = {}
    for name, options in kwargs.items():
        new_kwargs[name] = assert_choice(name, options)
    return begin.convert(**new_kwargs)


@begin.subcommand
def isbn(filename_pdf):
    extractor = extractors.ExtractorPdf(filename_pdf=filename_pdf)

    pdf_isbn = extractor.extract_isbn()

    if not pdf_isbn:
        return None

    print(pdf_isbn)

    return pdf_isbn


@begin.subcommand
@begin.convert(api_key=str)
# @choices(corpus=['google', 'isbndb'])
def search(corpus, pdf_isbn, api_key=None):

    if corpus == "google":
        retriever = retrievers.RetrieverBookInfoGoogle()
    else:
        if not api_key:
            raise ValueError("An API key needs to be defined under `api_key` to use the `ISBNdb` corpus.")

        retriever = retrievers.RetrieverBookInfoIsbndb(api_key=api_key)

    book_info = retriever.search(isbn=pdf_isbn)

    print(json.dumps(book_info))

    return book_info


@begin.start
def main():
    pass
