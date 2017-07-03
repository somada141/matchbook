# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import cStringIO

import pdfminer
import pdfminer.pdfinterp
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfpage


def generate_pdf_page_text(filename):
    """Generator that yields the text content of a PDF in a page-by-page fashion"""

    # create a `pdfminer.pdfinterp.PDFResourceManager` object
    resource_manager = pdfminer.pdfinterp.PDFResourceManager()

    # create a `cStringIO.StringIO` object which will be used by the
    # `TextConverter` (see below) to store the decoded text content
    # of the PDF pages
    str_return = cStringIO.StringIO()

    # create a new `pdfminer.converter.TextConverter` that will process
    # and decode the content of the PDF pages
    device = pdfminer.converter.TextConverter(
        resource_manager,
        str_return,
        codec="utf-8",
        laparams=pdfminer.layout.LAParams()
    )

    # create a new `pdfminer.pdfinterp.PDFPageInterpreter` which will perform the
    # actual processing via the `device` object
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
        resource_manager, device)

    # open the define PDF file
    fid = open(filename, str("rb"))

    # get a PDF-page generator on the opened PDF file
    generator_pages = pdfminer.pdfpage.PDFPage.get_pages(fid)

    # iterate through all PDF pages
    for page in generator_pages:
        # use the `interpreter` to extract the actual text content of the PDF
        # page
        interpreter.process_page(page)
        # retrieve the content from the `cStringIO.StringIO` object
        text = str_return.getvalue()
        # truncate the `cStringIO.StringIO` file object because the
        # `interpreter` appends the new content to the previous one.
        # This way, every iteration will only yield the current page
        # instead of gradually appending the new content.
        str_return.truncate(0)

        # yield the content of the current page
        yield text
