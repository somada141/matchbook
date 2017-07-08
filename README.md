# matchbook

## Introduction

`matchbook` is a very simple piece of code in the form of a CLI tool that allows one to extract the ISBN from a OCR'ed pdf (should it exist) and/or then run an ISBN against online APIs and retrieve that book's info for renaming and classification purposes.
 
I personally use this to rename and sort the free PDF books I get from the [Packt Publishing Free-Learning program](https://www.packtpub.com/packt/offers/free-learning) (no affiliation whatsoever).

## Installation

Just check out the code and install the Python requirements (possibly in a virtual-environment).

## Usage

### CLI

`matchbook` uses the [`begins` package](https://pypi.python.org/pypi/begins) to provide a very elementary CLI. Have a look at that package's doco if you like to which can be found under [http://begins.readthedocs.io/en/latest/api.html](http://begins.readthedocs.io/en/latest/api.html) but really a simple `python matchbook.py --help` will get you going just fine.

#### ISBN Extraction

`matchbook` defines the `isbn` subcommand which performs an ISBN extraction on a PDF file. It does so through the `pdfminer` package which it uses to extract all text from each PDF page which it regexes for ISBN and ISBN13 content (should it exist).

This can be invoked simply as:

    python matchbook.py isbn 9781785285486-INTERNET_OF_THINGS_WITH_ARDUINO_BLUEPRINTS.pdf

which returns `978-1-78528-548-6`.

#### Book API Lookup

`matchbook` provides some very basic integration with book APIs, specifically the [Google Books API](https://developers.google.com/books/) and [ISBNdb API](http://isbndb.com/api/v2/docs), in order to retrieve information on a given book via its ISBN (possibly extracted through `matchbook`): 

These APIs can be accessed via the `search` subcommand.

##### Google Books API

Matching against the Google Books API is performed simply with a request against [https://www.googleapis.com/books/v1/volumes](https://www.googleapis.com/books/v1/volumes) and, at least at the time of writing, does not require any authentication or API keys.

Usage is as simple as:

    python matchbook.py search google 9781449372620

where:

- `search` is the subcommand.
- `google` is the corpus/API to search under
- the last parameter is the ISBN without any hyphens (`9781449372620` above).

Upon successful execution the above command spits out a JSON document with the information available on this particular book (or whatever error Google throws should the ISBN not match).

##### ISBNdb API

Unlike Google Books, ISBNdb requires an account and API key to use their API. A free account made under [http://isbndb.com/](http://isbndb.com/) can provide you with an API key (capped to a finite number of requests I believe):
 
Usage is as follows:

    python matchbook.py search isbndb 9781449372620 --api-key=<your-api-key>

which, similarly to the Google Books case, will spit out a JSON string.

### Usage in Python scripts

While the command-line interface outlined above was put together haphazardly for my convenience the code is entirely usable as a vanilla Python package. 
 
In a nutshell:

- The `pdf.py` module provides the `generate_pdf_page_text` generator function that yields a PDF's text in a page-by-page fashion.
- The `extractors.py` module provides the `ExtractorPdf` class which can iterate over a PDF file running each page's content against a regex (which in this case is ISBN regexes but could be any other regex as well).
- The `retrievers.py` module provides the super basic API wrappers for Google Books and ISBNdb which can be easily complemented with additional classes.
