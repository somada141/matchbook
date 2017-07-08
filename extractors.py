# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

import pdf

regex_isbn = re.compile(
    ("(?:ISBN(?:-1[03])?:? )?((?=[-0-9 ]{17}$|[-0-9X ]{13}$|[0-9X]{10}$)"
     "(?:97[89][- ]?)?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X])"),
    re.MULTILINE
)
regex_isbn_13 = re.compile("(\d+-\d+-\d+-\d+-\d+)")


class ExtractionMode(object):

    first_result = 0
    first_page = 1
    all_results = 2


class ExtractorPdf(object):

    def __init__(self, filename_pdf):

        self.filename_pdf = filename_pdf

    def create_generator(self):

        generator = pdf.generate_pdf_page_text(filename=self.filename_pdf)

        return generator

    def extract(self, regex, mode=ExtractionMode.first_result):

        generator = self.create_generator()

        entries = []
        for page in generator:
            matches = re.findall(regex, page)
            if matches:
                if mode == ExtractionMode.first_result:
                    return matches[0]
                elif mode == ExtractionMode.first_page:
                    return matches
                elif mode == ExtractionMode.all_results:
                    entries += matches
                else:
                    raise ValueError

        return entries

    def extract_isbn(self, mode=ExtractionMode.first_page, filter_extra=regex_isbn_13):

        matches = self.extract(regex=regex_isbn, mode=mode)

        if not matches:
            return None

        if isinstance(matches, list):
            # convert the list of matches to a set and back to a list to remove duplicates
            matches = list(set(matches))
            for match in matches:
                if re.search(filter_extra, match):
                    return match
        else:
            return matches
