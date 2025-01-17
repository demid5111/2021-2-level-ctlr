# `pdf_utils` module

The `pdf_utils` module exposes a class `PDFRawFile`that is 
used for PDF files handling. It is responsible for several aspects:

1. Downloading PDF file by the link given.
1. Extracting the content of the PDF file downloaded.

This module is functional and given to you for further usage. Feel free to 
inspect its content. In case you think you have found a mistake, contact
assistant. Those who considerably improve this module will get additional 
bonuses.

> **HINT:** for `HTMLWithPDFParser` or `PDFParser` implementations, you need the following methods:
> * `PDFRawFile.__init__(...)`
> * `PDFRawFile.download(...)`
> * `PDFRawFile.get_text(...)`
