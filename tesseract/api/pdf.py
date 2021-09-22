import os
import re

from pathlib import Path
from subprocess import run, PIPE, STDOUT
from io import BytesIO
from tempfile import TemporaryDirectory, NamedTemporaryFile

from PIL import Image

PAGE = re.compile(r'page-?(?P<index>\d+).ppm')

def _extract_page(file_name: str) -> int:
    match = PAGE.match(file_name)
    if match:
        return int(match.group('index'))
    else:
        return 1

def _read_file_bytes(file_name: str) -> BytesIO:
    bytes_io = None
    with open(file_name, 'rb') as fp:
        bytes_io = BytesIO(fp.read())
    return bytes_io

def convert_to_ppm(pdf_file: BytesIO) -> list:
    ''' Convert a PDF to a list of PIL.Image. Uses temporary files and
    temporary directories to interact with pdftoppm. All files and directories
    created during this function's execution are removed post-conversion.

    Args:
        pdf_file (BytesIO): An open BytesIO file handle for a PDF

    Returns:
        (list): A list of PIL.Image objects representing each page of the PDF
    '''
    images = []

    with NamedTemporaryFile(suffix='.pdf') as fp:
        temp_file_path = Path(fp.name).resolve()
        fp.write(pdf_file.read())

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir).resolve()
            root_path = temp_dir_path / 'page'

            result = run(
                ['pdftoppm', str(temp_file_path), str(root_path)],
                stdout=PIPE,
                stderr=STDOUT,
                text=True
            )
            if result.returncode != 0:
                raise ChildProcessError(
                    f'pdftoppm failed with exit code {result.returncode} and '
                    f'output: {result.stdout}'
                )

            output_files = sorted(
                temp_dir_path.glob('*.ppm'),
                key=lambda path: _extract_page(path.name)
            )

            # Load each file into an in-memory Image and remove the files
            for output_file in output_files:
                bytes_io = _read_file_bytes(output_file)
                os.remove(output_file)
                images.append(Image.open(bytes_io))

    return images
