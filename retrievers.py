# -*- coding: utf-8 -*-

import requests


class RetrieverBookInfoBase(object):

    def __init__(self, url_template):

        self.url_template = url_template

    @staticmethod
    def clean_identifier(identifier):

        identifier_clean = identifier

        identifier_clean = identifier_clean.replace("-", "")

        identifier_clean = identifier_clean.replace("_", "")

        identifier_clean = identifier_clean.strip()

        return identifier_clean

    @staticmethod
    def execute(url, parameters):

        response = requests.get(url=url, params=parameters)

        if not response:
            return None

        if (not response.ok) or (not response.content):
            return None

        return response

    def query(self, url):

        response = self.execute(url=url, parameters=None)

        results = response.json()

        return results


class RetrieverBookInfoGoogle(RetrieverBookInfoBase):

    def __init__(
            self,
            url_template="https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    ):

        super(RetrieverBookInfoGoogle, self).__init__(url_template=url_template)

        self.url_template = url_template

    def assemble_url(self, isbn):

        isbn = self.clean_identifier(identifier=isbn)

        url = self.url_template.format(isbn=isbn)

        return url

    def search(self, isbn):

        url = self.assemble_url(isbn=isbn)

        return self.query(url=url)


class RetrieverBookInfoIsbndb(RetrieverBookInfoBase):

    def __init__(
            self,
            api_key,
            url_template="http://isbndb.com/api/v2/json/{api_key}/book/{isbn}",
    ):

        super(RetrieverBookInfoIsbndb, self).__init__(url_template=url_template)

        # internalise parameters
        self.api_key = api_key
        self.url_template = url_template

    def assemble_url(self, isbn):

        isbn = self.clean_identifier(identifier=isbn)

        url = self.url_template.format(api_key=self.api_key, isbn=isbn)

        return url

    def search(self, isbn):
        url = self.assemble_url(isbn=isbn)

        return self.query(url=url)