from collections import namedtuple

import pytesseract
from PIL import Image

from api.web import download_file
from api.pdf import convert_to_ppm

TesseractLeptonicaVersion = namedtuple('TesseractLeptonica', 'tesseract,leptonica')


def get_version():
    ''' Get Tesseract and Leptonica version info.

    Returns:
        (TesseractLeptonicaVersion): A named tuple containing the tesseract version and the
            leptonica version
    '''
    loose_version = pytesseract.get_tesseract_version()
    lines = [s.strip() for s in str(loose_version).split('\n')]
    tesseract_version = lines[0]
    leptonica_version = '?'
    for line in lines[1:]:
        if 'leptonica' in line.lower():
            leptonica_version = line
            break
    return TesseractLeptonicaVersion(tesseract_version, leptonica_version)


def download_and_ocr(uri, lang='eng'):
    ''' Download an image or a PDF from a URI and extract the text from the image with OCR.

    Args:
        uri (str): A URI to an image or a PDF file

    Returns:
        (list): The textual content of the image(s) for each page. If only one page, the list will
            only have one item.
    '''
    supported_langs = pytesseract.get_languages()
    if lang not in supported_langs:
        lang_list = ', '.join(supported_langs)
        if not lang_list:
            lang_list = '[no traineddata files available!]'
        raise ValueError(
            f'Tesseract is not configured to use the language "{lang}", supported languages are '
            f'{lang_list}'
        )

    extension = uri.split('.')[-1]
    ocr_pages = []
    images = []
    with download_file(uri) as file_handle:
        if extension == 'pdf':
            images = convert_to_ppm(file_handle)
        else:
            images.append(Image.open(file_handle))

    for index, image in enumerate(images, 1):
        print(f'Running OCR on page {index}')
        ocr_content = pytesseract.image_to_string(image, lang=lang)
        ocr_pages.append(ocr_content.replace('\f', ''))
        image.close()

    return ocr_pages
