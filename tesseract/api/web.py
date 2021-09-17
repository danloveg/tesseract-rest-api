from io import BytesIO

import requests

def download_file(uri: str) -> BytesIO:
    ''' Stream a file from a URI into an in-memory BytesIO structure.

    Args:
        uri (str): The URI to access the file

    Returns:
        (BytesIO): An open handle to the file streamed into memory
    '''
    file_bytes = BytesIO()
    with requests.get(uri, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            file_bytes.write(chunk)
    return file_bytes
